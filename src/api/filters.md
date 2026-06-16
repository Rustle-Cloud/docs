# Filters & storefronts

Filters decide *which* events a hook receives. They gate **delivery**, never dedupe. A
review that a filter excludes is still recorded as seen, so widening a filter later never
replays the back-catalogue.

## `review.created`: star band

Set `min_stars` and `max_stars` (each `1`–`5`, with `min ≤ max`). Defaults to `1`–`5` (every
review).

```jsonc
{ "event_type": "review.created", "min_stars": 1, "max_stars": 2 }  // only 1–2★ reviews
```

## `rating.dropped`: delta

Set a `delta` (`0`–`4`); it is **required**.

- `delta`: fire when the rating falls by at least this much versus the last observation.

```jsonc
{ "event_type": "rating.dropped", "delta": 0.2 }  // fires on a 0.2+ drop
```

## Storefronts

A hook does not pick a storefront. It covers **every** storefront you watch for the app in
the console (console → Apps → add), and each delivered event carries the storefront it came
from in its `country` field. To act on one storefront only, add a Filter step on `country`
downstream (lowercase ISO-3166 alpha-2, e.g. `us`, `fr`).

Which storefronts an app is polled in is chosen once, in the console, when you watch the app.

## The baseline

Every hook is **forward-looking**: it only receives events that occur at or after it was
created. There is no lookback. A brand-new hook does not replay reviews already sitting in a
store's feed, and `rating.dropped` seeds its baseline silently on first observation.
