# `review.created`

Fires once per newly-seen review that passes your [star filter](../api/filters.md). Carries
the [common envelope](../concepts/events.md) plus the fields below.

## Payload fields

| Field | Type | Notes |
|-------|------|-------|
| `review_id` | string | Store-native, stable review id. |
| `fingerprint` | string | `hash(store + app_id + review_id)` — identity only. This is the event's `occurrence_id`. |
| `content_hash` | string | Hash of title + body. **Non-key** — for your own edit detection; it never affects identity. |
| `rating` | integer | 1–5. |
| `title` | string \| null | May be absent. |
| `body` | string | The review text. |
| `author` | string \| null | Store-provided display name. |
| `app_version` | string \| null | Version reviewed, when the source provides it. |
| `country` | string | Storefront/locale the review was polled from (lowercase ISO-3166 alpha-2). |

## Filtering

A hook configures `min_stars` / `max_stars` (each 1–5, default 1–5). The filter gates
**delivery**, never dedupe — a filtered-out review is still recorded as seen, so widening the
filter later never replays it. See [Filters & storefronts](../api/filters.md).

## Example

```json
{
  "event_id": "sample-review-event-id",
  "occurrence_id": "sample-fingerprint",
  "event_type": "review.created",
  "store": "apple",
  "app_id": "284882215",
  "subscriber_id": "zapier-sample",
  "occurred_at": "2026-06-01T12:00:00Z",
  "observed_at": "2026-06-01T12:05:00Z",
  "schema_version": 1,
  "review_id": "rev-1",
  "fingerprint": "sample-fingerprint",
  "content_hash": "sample-content-hash",
  "rating": 5,
  "title": "Great app",
  "body": "I love it",
  "author": "jane",
  "app_version": "3.2.1",
  "country": "us"
}
```

> Editing a review's body does **not** re-fire `review.created` — identity excludes content.
> Use `content_hash` if you want to detect edits yourself.

You can fetch a synthetic example of this shape any time from
[`GET /api/v1/sample?event_type=review.created`](../api/endpoints.md#get-apiv1sample).
