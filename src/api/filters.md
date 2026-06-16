# Filters & storefronts

Filters decide *which* events a hook receives. They gate **delivery**, never dedupe — a
review that a filter excludes is still recorded as seen, so widening a filter later never
replays the back-catalogue.

## `review.created` — star band

Set `min_stars` and `max_stars` (each `1`–`5`, with `min ≤ max`). Defaults to `1`–`5` (every
review).

```jsonc
{ "event_type": "review.created", "min_stars": 1, "max_stars": 2 }  // only 1–2★ reviews
```

## `rating.dropped` — threshold & delta

Set a `threshold` (`1`–`5`) and/or a `delta` (`0`–`4`); **at least one is required**.

- `threshold` — fire when the aggregate rating crosses below this value.
- `delta` — fire when the rating falls by at least this much versus the last observation.

```jsonc
{ "event_type": "rating.dropped", "threshold": 4.5 }            // dips below 4.5
{ "event_type": "rating.dropped", "delta": 0.2 }               // drops by 0.2+
{ "event_type": "rating.dropped", "threshold": 4.0, "delta": 0.3 } // either rule
```

## Storefronts

A watch targets one storefront via `country` (lowercase ISO-3166 alpha-2; defaults to `us`).
The catalogue is curated — these are the supported codes:

| Code | Storefront | Code | Storefront |
|------|------------|------|------------|
| `us` | United States | `se` | Sweden |
| `gb` | United Kingdom | `br` | Brazil |
| `ca` | Canada | `mx` | Mexico |
| `au` | Australia | `jp` | Japan |
| `ie` | Ireland | `kr` | South Korea |
| `fr` | France | `in` | India |
| `de` | Germany | `nl` | Netherlands |
| `es` | Spain | `it` | Italy |

The same list serves both stores. A `country` outside this set returns `400`. To watch one
app across several storefronts, register one hook per storefront.

## The baseline

Every hook is **forward-looking**: it only receives events that occur at or after it was
created. There is no lookback — a brand-new hook does not replay reviews already sitting in a
store's feed, and `rating.dropped` seeds its baseline silently on first observation.
