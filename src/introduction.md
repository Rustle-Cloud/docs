# Rustle docs

**Rustle is an app-review radar.** It watches the Apple App Store and Google Play for new
reviews and rating movements on the apps you care about, and delivers each change to your
webhook as a structured event, **reliably, exactly once, and politely**.

It is a plumbing product. The entire value is correctness:

- **It never double-fires.** A given review or rating drop produces at most one delivered
  event, ever, even under re-polling and at-least-once redelivery.
- **It never silently dies.** Parser breakage and scraper blocks fail loudly; they are
  never swallowed.
- **It is a good citizen.** Conservative, jittered, backed-off request rates against both
  stores.

## The mental model

```text
   App Store ─┐
              ├─►  poll  ─►  normalize  ─►  deliver exactly-once  ─►  your webhook
 Google Play ─┘             (one schema)      (signed, deduped)
```

You never run a scraper, never poll a store, and never branch on which store a review came
from. You register a callback URL, and Rustle POSTs you a small JSON event when something
happens.

## Two events

| Event | Fires when |
|-------|------------|
| [`review.created`](./events/review-created.md) | A new review lands on either store (filter by star rating, locale, keyword). |
| [`rating.dropped`](./events/rating-dropped.md) | An app's aggregate rating falls by a delta you set. |

Both share one [store-agnostic envelope](./concepts/events.md) and carry a `schema_version`
(currently `1`).

## How you'll use it

- **Directly, via the [REST Hook API](./api/endpoints.md)**: register and remove webhook
  callbacks with an API token.
- **Through [Zapier](./integrations/zapier.md)** *(early access)*: trigger Zaps on new
  reviews and rating drops, no endpoint to host.

> **Not real-time, on purpose.** Reviews fire as soon as the stores publish them, typically
> within hours for Apple and about a day for Google. Rustle is not real-time because the
> stores aren't; it would rather be exactly-once than pretend to be instant.

Start with the [Quickstart](./quickstart.md).
