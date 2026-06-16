# Quickstart

From zero to your first event in three steps.

## 1. Get an API token

Sign in to the console at [app.rustle.cloud](https://app.rustle.cloud), open **Integrations**,
and issue a token. It looks like `rsk_…` and is shown **once** — store it somewhere safe.

You authenticate every API call with it, as either header:

```http
Authorization: Bearer rsk_your_token
```
```http
X-API-Key: rsk_your_token
```

## 2. Register a webhook

Point Rustle at a URL you control. This example fires on new **1–2★** reviews of an App
Store app in the US storefront:

```bash
curl -X POST https://app.rustle.cloud/api/v1/hooks \
  -H "Authorization: Bearer rsk_your_token" \
  -H "Content-Type: application/json" \
  -d '{
        "target_url": "https://example.com/webhooks/rustle",
        "store": "apple",
        "app_id": "284882215",
        "country": "us",
        "event_type": "review.created",
        "min_stars": 1,
        "max_stars": 2
      }'
```

The response returns the hook `id` and a **signing secret** (shown once — keep it to
[verify signatures](./webhooks/signatures.md)):

```json
{
  "id": "api-1a2b3c4d5e6f7a8b",
  "secret": "<webhook signing secret — shown once>",
  "store": "apple",
  "app_id": "284882215",
  "country": "us",
  "event_type": "review.created"
}
```

That's it — the app is now in the poll set. See [Filters & storefronts](./api/filters.md)
for the full set of options, and [`rating.dropped`](./events/rating-dropped.md) for rating
alerts.

## 3. Receive an event

When a matching review appears, Rustle POSTs a JSON body to your `target_url`, with two
headers:

```http
POST /webhooks/rustle HTTP/1.1
x-radar-event-id: 6f1c…                      # dedupe on this
x-radar-signature: sha256=9a0b…              # verify this
Content-Type: application/json
```
```json
{
  "event_id": "6f1c…",
  "occurrence_id": "…",
  "event_type": "review.created",
  "store": "apple",
  "app_id": "284882215",
  "subscriber_id": "api-1a2b3c4d5e6f7a8b",
  "occurred_at": "2026-06-02T14:08:11Z",
  "observed_at": "2026-06-02T14:09:03Z",
  "schema_version": 1,
  "review_id": "10982334771",
  "fingerprint": "…",
  "content_hash": "…",
  "rating": 2,
  "title": null,
  "body": "Crashes on launch since 4.2.",
  "author": "tess_w",
  "app_version": "4.2.0",
  "country": "us"
}
```

Two rules make this safe to consume:

1. **[Dedupe on `event_id`](./concepts/exactly-once.md)** — delivery is at-least-once, so a
   rare redelivery is possible by design.
2. **[Verify `x-radar-signature`](./webhooks/signatures.md)** — confirm the body really came
   from Rustle.

To stop receiving events, [remove the hook](./api/endpoints.md#delete-apiv1hooksid):

```bash
curl -X DELETE https://app.rustle.cloud/api/v1/hooks/api-1a2b3c4d5e6f7a8b \
  -H "Authorization: Bearer rsk_your_token"
```
