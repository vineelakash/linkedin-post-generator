---
name: Linkedin_notemaker
description: Generate ultra-concise, personalized LinkedIn connection request notes (under 200 characters) for independent insurance agencies and mortgage brokerages.
version: 1.0.0
tags:
  - linkedin
  - connection-request
  - b2b-outreach
  - personalization
---

# LinkedIn Connection Request Skill

Generate personalized LinkedIn connection requests for insurance agencies and mortgage companies.

## Required Format

```text
Hey {{first_name}} — noticed {{pain_point_signal}}. Sent you a quick note on how {{service_system}} helps {{measurable_outcome}}. Nice to connect.
```

## Character Limit

* Target: **180–200 characters**
* Hard maximum: **200 characters**
* If over 200 characters, shorten the wording.
* Never sacrifice the core personalization to add unnecessary words.

## Variables

### `{{first_name}}`

Prospect's first name.

### `{{pain_point_signal}}`

A very short, prospect-specific observation that indicates a pain our service can solve.

Examples:

* `your quote process relies heavily on inbound calls`
* `your agency is handling multiple insurance lines`
* `your site drives prospects to call`
* `your team handles a high-touch borrower process`
* `your site is generating mortgage inquiries`

Do not say the prospect is definitely losing money unless verified.

### `{{service_system}}`

One relevant service only.

Examples:

* `AI quote follow-up`
* `AI renewal follow-up`
* `AI lead recovery`
* `AI borrower follow-up`
* `AI pipeline recovery`
* `AI document follow-up`

### `{{measurable_outcome}}`

A concise measurable result.

Examples:

* `faster lead response`
* `recover missed quotes`
* `reduce manual follow-up`
* `recover cold leads`
* `recover stalled files`
* `speed up document collection`

## Selection Logic

Determine:

```text
Prospect evidence
→ Pain signal
→ Relevant AI system
→ Measurable outcome
```

Use only **one** pain, one service, and one outcome.

## Example

```text
Hey Jason — noticed your site drives prospects to call. Sent you a quick note on how AI lead recovery helps recover missed inquiries. Nice to connect.
```

## Rules

* Do not use generic compliments.
* Do not mention multiple services.
* Do not use AI buzzwords unnecessarily.
* Do not fabricate pain points.
* Do not include links.
* Do not include a meeting request.
* Do not use emojis.
* Keep it conversational.
* Stay at or below **200 characters**.

## Final Check

Before output:

```text
[ ] Prospect-specific pain signal
[ ] Relevant service
[ ] Measurable outcome
[ ] Natural wording
[ ] ≤200 characters
[ ] No fabricated information
[ ] No sales pitch
```
