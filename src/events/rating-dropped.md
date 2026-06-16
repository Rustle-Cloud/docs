# `rating.dropped`

Fires when an app's aggregate rating crosses **below a threshold** you set, **or** falls by a
**delta** versus the last observed aggregate. Carries the [common envelope](../concepts/events.md)
plus the fields below.

## Payload fields

| Field | Type | Notes |
|-------|------|-------|
| `transition_id` | string | `hash(store + app_id + current_rating + rating_count)` — identity. This is the event's `occurrence_id`. Deterministic, so re-observing the same aggregate dedupes. |
| `previous_rating` | float | Last observed aggregate. |
| `current_rating` | float | Newly observed aggregate. |
| `delta` | float | `current − previous` (negative on a drop). |
| `rating_count` | integer | Total ratings backing the current aggregate. |
| `trigger` | enum | `threshold` or `delta` — which rule fired. |
| `threshold` | float \| null | The configured threshold, when `trigger` is `threshold`. |

## Rules

A hook can set a `threshold` (1–5) and/or a `delta` (0–4); at least one is required.

- **threshold** — fire when `current_rating` crosses below the threshold.
- **delta** — fire when the rating falls by at least that much versus the last observation.

The first time Rustle observes an app's rating it **seeds the baseline silently** (no event),
so you only hear about movement from there on. Re-observing an unchanged aggregate never
re-fires. See [Filters & storefronts](../api/filters.md).

## Example

```json
{
  "event_id": "sample-rating-event-id",
  "occurrence_id": "sample-transition",
  "event_type": "rating.dropped",
  "store": "google",
  "app_id": "com.example.app",
  "subscriber_id": "zapier-sample",
  "occurred_at": "2026-06-01T12:00:00Z",
  "observed_at": "2026-06-01T12:05:00Z",
  "schema_version": 1,
  "transition_id": "sample-transition",
  "previous_rating": 4.2,
  "current_rating": 3.9,
  "delta": -0.3,
  "rating_count": 12345,
  "trigger": "threshold",
  "threshold": 4.0
}
```

You can fetch a synthetic example any time from
[`GET /api/v1/sample?event_type=rating.dropped`](../api/endpoints.md#get-apiv1sample).
