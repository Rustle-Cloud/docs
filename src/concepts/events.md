# Events & delivery

Every event Rustle delivers shares one **store-agnostic envelope**. The store of origin is a
*field* (`store`), never something your code has to branch on — a review from Apple and a
review from Google arrive in exactly the same shape.

## The envelope

These fields are present on every event, regardless of type:

| Field | Type | Notes |
|-------|------|-------|
| `event_id` | string | Identity of **this delivery to this subscriber**. Deterministic (not random). **[Dedupe on it](./exactly-once.md).** Also sent as the `x-radar-event-id` header. |
| `occurrence_id` | string | Identity of the underlying occurrence, **shared** across every subscriber it fans out to. Lets you recognise "the same review, delivered to me." |
| `event_type` | enum | `review.created` or `rating.dropped`. |
| `store` | enum | `apple` or `google`. A field, not a code branch. |
| `app_id` | string | Store-native app id (Apple numeric id, Google package name). |
| `subscriber_id` | string | The hook this was delivered to (your hook `id`). |
| `occurred_at` | RFC 3339 | When the change happened at the source. |
| `observed_at` | RFC 3339 | When Rustle detected it (poll time). |
| `schema_version` | integer | Starts at `1`; bumped only on a breaking payload change. |

The type-specific fields (`review_id`, `rating`, `body`, … for reviews;
`current_rating`, `delta`, … for rating drops) sit **at the top level** alongside the
envelope — the payload is flattened, not nested. See each event's reference:
[`review.created`](../events/review-created.md), [`rating.dropped`](../events/rating-dropped.md).

## Delivery

Rustle POSTs the event as a JSON body to your hook's `target_url`, with two headers:

| Header | Purpose |
|--------|---------|
| `x-radar-event-id` | The event's `event_id` — [dedupe on it](./exactly-once.md). |
| `x-radar-signature` | `sha256=<hex>` HMAC of the exact body — [verify it](../webhooks/signatures.md). |

A `2xx` response means you accepted the event. Any other response (or a timeout) is treated
as a failure and retried with backoff; events that exhaust their retries land in a
dead-letter queue rather than being dropped.

## Forward-looking by default

A new hook only receives events that occur **at or after** it was created — it does not
replay the back-catalogue already sitting in a store's feed. (The same is true for rating
drops: the first observation seeds the baseline silently.)
