# Changelog

## Event schema

The delivered event payload carries a `schema_version`. It is bumped only on a **breaking**
change to the payload; additive, backward-compatible fields do not bump it.

| `schema_version` | Status | Notes |
|------------------|--------|-------|
| `1` | Current | `review.created` and `rating.dropped`, the store-agnostic envelope, HMAC-SHA256 signatures. |

The optional [`enrichment`](../events/review-created.md#the-enrichment-object) object on
`review.created` was added under `schema_version` `1` — an additive, backward-compatible
field, so it did not bump the version. Write your consumer defensively: ignore unknown
fields, treat `enrichment` as optional (it may be `null`), and key your idempotency on
[`event_id`](../concepts/exactly-once.md).

## API

The REST Hook API lives under `/api/v1`. The authoritative, versioned contract is the
[OpenAPI reference](../api/reference.md), generated from the code.

## Coming

- Make and n8n integration guides (the API already supports them via `source`).
- Additional events and a public roadmap.
