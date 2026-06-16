# Exactly-once & idempotency

Rustle's core promise is that a given review or rating drop produces **at most one delivered
event** — no double-fires — and that nothing is silently dropped. Here's the contract you
consume against.

## Delivery is at-least-once; you dedupe on `event_id`

Committing a database row and making an external HTTP POST can never be made atomic (the
two-generals problem). So exactly-once delivery to an arbitrary endpoint is impossible, and
Rustle makes the honest choice: **at-least-once delivery, deduped by the consumer.**

In practice you will almost always receive each event once. But a delivery whose confirmation
was lost (we POSTed, your `2xx` came back, but our confirm write didn't land) is **re-attempted**
rather than risk dropping it. That's the rare redelivery the contract warns about.

> **The rule:** treat `event_id` as an idempotency key. If you've already processed an
> `event_id`, ignore the redelivery. It's also sent as the `x-radar-event-id` header so you
> can dedupe before even parsing the body.

`event_id` is **deterministic** — the same occurrence delivered to the same hook always
produces the same `event_id` — which is exactly what makes consumer-side dedupe reliable.

```python
# Pseudocode for an idempotent receiver
event_id = request.headers["x-radar-event-id"]
if seen.contains(event_id):
    return 200  # already handled — ack and move on
process(request.json)
seen.add(event_id)
return 200
```

## What you don't have to worry about

- **Re-polling.** Rustle re-reads the stores constantly; an already-seen review is never
  re-emitted. The dedupe happens server-side, before fan-out.
- **An author editing their review.** Review identity excludes the review's content, so an
  edit does not re-fire `review.created`. (A separate `content_hash` is provided for your own
  edit detection, but it never affects identity.)
- **Ordering.** Events are not guaranteed to arrive in occurrence order. Each event is
  self-describing (`occurred_at`, `observed_at`); don't rely on delivery order.

## Occurrence vs. delivery

Two ids, two jobs:

- `event_id` — *this delivery to this hook*. Your idempotency key.
- `occurrence_id` — *the underlying review or rating drop*, shared if you have several hooks
  watching the same app. Use it to recognise "the same thing, delivered to more than one of
  my hooks."
