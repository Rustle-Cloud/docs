# `review.created`

Fires once per newly-seen review that passes your [star filter](../api/filters.md). Carries
the [common envelope](../concepts/events.md) plus the fields below.

## Payload fields

| Field | Type | Notes |
|-------|------|-------|
| `review_id` | string | Store-native, stable review id. |
| `fingerprint` | string | `hash(store + app_id + review_id)`: identity only. This is the event's `occurrence_id`. |
| `content_hash` | string | Hash of title + body. **Non-key**, for your own edit detection; it never affects identity. |
| `rating` | integer | 1–5. |
| `title` | string \| null | May be absent. |
| `body` | string | The review text. |
| `author` | string \| null | Store-provided display name. |
| `app_version` | string \| null | Version reviewed, when the source provides it. |
| `country` | string | Storefront/locale the review was polled from (lowercase ISO-3166 alpha-2). |

## The `enrichment` object

An optional `enrichment` object may accompany a review with extra context — overall
sentiment, topic tags, and a short English summary. It **may be `null`**, so treat it as
optional and code defensively.

| Field | Type | Notes |
|-------|------|-------|
| `language` | string | Detected language of the review text (ISO 639-1), independent of the storefront. |
| `sentiment` | enum | `positive`, `neutral`, `negative`, or `mixed`. |
| `themes` | array | One or more topic tags from the vocabulary below. |
| `is_feature_request` | bool | The review asks for a feature. |
| `feature_slug` | string \| null | Stable key for the requested feature — the same feature maps to the same slug across languages. `null` unless `is_feature_request`. |
| `feature_phrase` | string \| null | Short label for the requested feature. `null` unless `is_feature_request`. |
| `is_bug_report` | bool | The review reports a bug. |
| `severity` | enum | `low`, `medium`, or `high`. `high` = crash, data loss, payment failure, security, or explicit churn. |
| `mentions_competitor` | bool | The review names another product. |
| `competitor_named` | string \| null | The named product. `null` unless `mentions_competitor`. |
| `other_topic` | string \| null | Short phrase for a topic outside the vocabulary. Set only when `themes` includes `other`; `null` otherwise. |
| `summary_en` | string | A short English summary of the review (≤~20 words), written in English whatever the review's language. |

`themes` is drawn from a fixed vocabulary:

`stability_crash`, `performance`, `battery`, `data_loss`, `sync`, `login_account`,
`billing_payment`, `refund`, `pricing_value`, `ads`, `ui_ux`, `onboarding`, `bug_general`,
`notifications`, `privacy_security`, `customer_support`, `content_quality`, `compatibility`,
`localization`, `update_regression`, `praise_general`, `comparison`, `other`.

`sentiment`, `themes`, `is_feature_request`, `is_bug_report`, and `severity` are independent
axes — a review can be positive, about `sync`, and a feature request at once.

## Filtering

A hook configures `min_stars` / `max_stars` (each 1–5, default 1–5). The filter gates
**delivery**, never dedupe. A filtered-out review is still recorded as seen, so widening the
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
  "rating": 2,
  "title": "Crashes and lost my notes",
  "body": "Loved the redesign, but it crashes after the latest update and I lost my notes. Please add an offline mode like Evernote.",
  "author": "jane",
  "app_version": "3.2.1",
  "country": "us",
  "enrichment": {
    "language": "en",
    "sentiment": "mixed",
    "themes": ["stability_crash", "update_regression", "data_loss"],
    "is_feature_request": true,
    "feature_slug": "offline_mode",
    "feature_phrase": "Offline mode",
    "is_bug_report": true,
    "severity": "high",
    "mentions_competitor": true,
    "competitor_named": "Evernote",
    "other_topic": null,
    "summary_en": "Crashes and loses notes after the update; wants an offline mode."
  }
}
```

> Editing a review's body does **not** re-fire `review.created`; identity excludes content.
> Use `content_hash` if you want to detect edits yourself.

You can fetch a synthetic example of this shape any time from
[`GET /api/v1/sample?event_type=review.created`](../api/endpoints.md#get-apiv1sample).
