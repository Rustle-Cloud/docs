# Endpoints

The REST Hook API lets a program register and remove webhook callbacks. Base URL
`https://app.rustle.cloud`, all under `/api/v1`, all [bearer-authenticated](./authentication.md).

For the exhaustive, machine-readable schema, see the [API reference](./reference.md)
(generated from the code).

## POST /api/v1/hooks

Create a hook: a callback URL + the matching watch. The app enters the poll set immediately.

**Body**

| Field | Required | Default | Notes |
|-------|----------|---------|-------|
| `target_url` | yes | — | The URL events are delivered to (http/https). |
| `store` | yes | — | `apple` or `google`. |
| `app_id` | yes | — | Store-native app id. |
| `event_type` | yes | — | `review.created` or `rating.dropped`. |
| `country` | no | `us` | Storefront — see [storefronts](./filters.md#storefronts). |
| `min_stars` / `max_stars` | no | `1` / `5` | `review.created` star band (each 1–5). |
| `threshold` | no | — | `rating.dropped` threshold (1–5). |
| `delta` | no | — | `rating.dropped` delta (0–4). At least one of `threshold`/`delta` is required. |
| `source` | no | `api` | Provenance hint: `zapier` / `make` / `n8n` / `api`. |
| `external_ref` | no | — | Your own correlation crumb (≤ 256 chars). |

```bash
curl -X POST https://app.rustle.cloud/api/v1/hooks \
  -H "Authorization: Bearer rsk_your_token" \
  -H "Content-Type: application/json" \
  -d '{"target_url":"https://example.com/hook","store":"google",
       "app_id":"com.acme.notes","event_type":"rating.dropped","threshold":4.5}'
```

**Response `200`** — returns the hook `id` and the signing `secret` (**shown once**):

```json
{ "id": "api-1a2b3c4d5e6f7a8b", "secret": "…", "store": "google",
  "app_id": "com.acme.notes", "country": "us", "event_type": "rating.dropped" }
```

Invalid input (bad store, URL, event type, star band, or rating rule) returns `400` with
`{ "error": "…" }`.

## GET /api/v1/hooks

List every hook this account owns.

```bash
curl https://app.rustle.cloud/api/v1/hooks -H "Authorization: Bearer rsk_your_token"
```
```json
[ { "id": "api-1a2b…", "source": "api",
    "target_url": "https://example.com/hook", "external_ref": null } ]
```

## DELETE /api/v1/hooks/&#123;id&#125; {#delete-apiv1hooksid}

Remove a hook and its watch (and drop the app from the poll set if nothing else watches it).

```bash
curl -X DELETE https://app.rustle.cloud/api/v1/hooks/api-1a2b3c4d5e6f7a8b \
  -H "Authorization: Bearer rsk_your_token"
```

Returns `204 No Content` on success, or `404` if no hook with that id belongs to you.

## GET /api/v1/apps

The apps this account already watches — handy for populating a dropdown. (Subscribe also
accepts free-text app ids.)

```bash
curl https://app.rustle.cloud/api/v1/apps -H "Authorization: Bearer rsk_your_token"
```

## GET /api/v1/sample

A synthetic, representative event — for a platform's "test trigger" step. It never touches
your data, so any valid token works. Returns a **one-element array**.

```bash
curl "https://app.rustle.cloud/api/v1/sample?event_type=review.created" \
  -H "Authorization: Bearer rsk_your_token"
```

`event_type` is `review.created` (default) or `rating.dropped`. See the
[event reference](../events/review-created.md) for the exact shape.
