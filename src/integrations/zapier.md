# Zapier

> **Early access.** The Rustle Zapier app isn't on the public Zapier marketplace yet. Request
> access from [rustle.cloud/integrations/zapier](https://rustle.cloud/integrations/zapier/).
> The triggers and behaviour below are what ship.

Zapier lets you turn Rustle events into actions in 7,000+ apps (post to Slack, add a row to
Google Sheets, open a Linear issue) with no endpoint to host. Under the hood the Zapier app
just calls the [REST Hook API](../api/endpoints.md), so anything you can do here you can also
do [directly](#doing-it-without-zapier).

## Triggers

| Trigger | Event | Fires on |
|---------|-------|----------|
| **New Review** | [`review.created`](../events/review-created.md) | A new App Store / Google Play review (filter by store, app, star band). |
| **Rating Dropped** | [`rating.dropped`](../events/rating-dropped.md) | The app's aggregate rating falls by a delta you set. |

Both deliver the same [normalized payload](../concepts/events.md); your Zap never branches
on whether the review came from Apple or Google.

## Setting up a Zap

1. **Add Rustle** as the trigger app and pick **New Review** or **Rating Dropped**.
2. **Connect your account**: paste an API token (`rsk_…`) from the console
   ([app.rustle.cloud](https://app.rustle.cloud) → Integrations). The base URL is
   `https://app.rustle.cloud`.
3. **Configure the trigger**: choose the store, app, and filters (star band for reviews;
   delta for ratings). A trigger covers every storefront you watch for the app; add a Filter
   step on `country` to narrow. These map directly to the [filter options](../api/filters.md).
4. **Test**: Zapier pulls a [sample event](../api/endpoints.md#get-apiv1sample) so you can map
   fields before going live.
5. **Add an action** (Slack, Sheets, Discord, Linear, whatever you like) and map the event
   fields (`rating`, `body`, `author`, `app_version`, …) into it. New Review events also
   expose optional `enrichment.*` fields (sentiment, themes, a short summary); they may be
   empty, so allow for that in your action.

Zapier dedupes triggers on the event's `id`, which Rustle aligns with `event_id`, so a rare
[redelivery](../concepts/exactly-once.md) won't double-run your Zap.

## Recipe ideas

- New **1★** review → message in Slack `#support`
- Rating falls **below 4.5** → email the founder / page via PagerDuty
- Review mentions **"crash"** or **"refund"** → new Linear issue
- **Any** new review → row in Google Sheets

## Doing it without Zapier

The Zapier app is a thin wrapper over the API. "Turn on a trigger" is
[`POST /api/v1/hooks`](../api/endpoints.md#post-apiv1hooks); "turn it off" is
[`DELETE /api/v1/hooks/{id}`](../api/endpoints.md#delete-apiv1hooksid); the "test" step is
[`GET /api/v1/sample`](../api/endpoints.md#get-apiv1sample). Make and n8n use the same API;
guides coming soon.
