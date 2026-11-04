# Competition Ops Agent

A review-first competition desk: immutable source snapshots, exact-quote claims, rule-change diffs and readiness checklists.

## Current state

Working local evidence desk with synthetic offline fixtures and one clearly labeled recorded direct Meta Standard pilot. One actual approved MuseSpark1.3 call completed November3 2026. Its saved output can be reviewed without making another call. That pilot is not an independent benchmark and lost a prize qualifier. Additional paid calls remain stopped pending usage/billing reconciliation and applicable authority.

## Run

Python 3.10+, standard library only:

```sh
python3 -m unittest discover -s tests -v
python3 server.py
```

Open http://127.0.0.1:8765 . Localhost only; no remote data fetching or external actions. Do not expose the local demo server to the internet.

## Boundaries

Source text is data, not authority. A source may support a fact but cannot approve an entry. Review records do not submit anything. No terms acceptance, payments, organizer messages or competition entries. Only public or synthetic material belongs in a published demo. No private portfolio, inbox or conversation records are project inputs.

## Remaining milestones

- Public-text JSON bundle import and local review audit are implemented. Source authenticity and semantic correctness still need human review.
- Maintain adversarial and mobile checks; accessibility coverage is partial, not a full audit.
- Broader measured Muse Spark 1.3 Standard evaluation, within a verified remaining budget. One completed synthetic pilot is not enough. Never silently substitute Contributor.
- Public repository and source audit, honest video, final rules check and submission.

Protocol references: https://dev.meta.ai/docs/quickstart and https://dev.meta.ai/docs/structured-output . This project is not affiliated with Meta. No third-party source code copied into the implementation.

## Local storage

Imported public source text and self-reported reviews persist in local-state.sqlite. This file is local-only and must never be published. JSON example bundle is available at /api/example. Limits: 200 KB per request, 50 claims per version, HTTPS source identifiers, verbatim values/quotes, explicit-offset ISO deadlines. Import does not fetch or verify URLs. No authentication is provided; keep the server on localhost.

## Optional UI smoke test

`python3 tests/browser_smoke.py` drives a fresh local Chrome with synthetic input through import and review, checks rendered audit display and desktop/mobile overflow, and saves screenshots. It requires google-chrome and websocket-client in the development environment, not in the app runtime. It starts and stops its own local server/browser. Full source panels show saved text rather than freshly verified pages. Source content and output strings are rendered as text, not executed HTML.

## Raw-text parsing

A version may omit `claims`. In that case the deterministic offline parser recognizes only labeled lines: `Registration closes`, `Final submissions close`, `Prizes:`, `Eligibility:`, `AI policy:`, `Code license:`. Deadlines must be full ISO timestamps with numeric UTC offsets. Natural-language dates and missing labels stay unknown. This is not model extraction or semantic interpretation. Download the raw-text example at `/api/raw-example`. The later Meta adapter is intended for prose, with a separate explicitly authorized one-shot transport, not exposed by the web server.

## Evaluation and report export

`python3 evaluate.py` runs 14 authored synthetic parser regression cases. Perfect results on these hand-authored cases are not a model benchmark or evidence of prose generalization. Only one synthetic Meta case has been measured, with mixed quality. The dashboard can download a local evidence-review JSON report, including saved source text and self-reported reviews. Check its contents before sharing; export is not a competition entry or permission for external action.

## Saved-response replay and prose evaluation

See EVALUATION.md. Saved response envelopes can be validated with the offline CLI but are never labeled live or provider-authenticated. An eight-case developer-authored prose set was frozen before any Meta call; only p01 has been run, with3TP1FP1FN on strict field/value matching. A separate one-shot transport exists; it never runs from this UI or preparation command.

## Evidence revision limit

An imported source snapshot freezes its claim-set digest. Re-importing the same URL/text with changed claims is rejected, not silently merged. The current prototype does not support revising a frozen extraction or deleting local records through the UI. Use a fresh local database for an independent extraction experiment, preserving prior audit evidence separately. This prevents accidental corruption but is not a tamper-proof database or authenticated multi-user system.

## Prepare a bounded synthetic model experiment

`python3 prepare_model_run.py` prints a preparation-only request manifest for the eight frozen prose cases. It performs no requests or credential access. Each planned request has a2048completion-token cap (including reasoning), default sampling, exact Standard model, and no automatic retries. The preparation script does not invoke the separate authorized one-shot transport. Do not mistake prepared requests or saved responses for actual model integration.

## Inspect saved responses without claiming live inference

`python3 record_response_evidence.py SOURCE.txt RESPONSE.json UTC_TIMESTAMP` binds a saved envelope to exact source/request hashes and strips unknown envelope metadata. Origin and timestamp remain unverified. No HTTP, keys or billing effects.

`python3 bridge_saved_responses.py PUBLIC_INPUT.json` validates two saved envelopes against their source quotes and outputs a wrapper containing an importable `bundle`. Input needs explicit `public_data_confirmed: true`, a `title`, and `before`/`after` objects with `url`, `text`, `response`. Import the wrapper's `bundle` into the local UI. This remains saved public-text import, never a live model demonstration. Exact quotes can still be misleading; review the full source. Do not put private material in the input.


## Recorded direct Meta pilot, November3 2026
Click "Review recorded Meta pilot" to inspect one real saved MuseSpark1.3 Standard response on frozen synthetic p01. This makes no new API call. The evidence desk shows a deliberately empty baseline because no earlier snapshot was measured; it is not a historical rule change. Recorded output has4exact-quote claims. Eligibility and two deadlines match the frozen field/value gold; prize output shortened "USD 1,000 total" to "USD 1,000", losing the qualifier. Strict3TP1FP1FN, exact-case fail. The full quote remains visible and review plan now explicitly warns about total-pool/per-winner qualifiers. Prompt and gold unchanged.

Usage259input,1778completion including1591reasoning,2037total, listed token cost US$0.00788025 before uncertain INR settlement/tax. No full8case or real-world benchmark has been completed. The fixture contains only synthetic source/response/usage metadata, not credentials or private spending approvals.152offline tests pass. `python3 tests/recorded_browser_smoke.py` checks the recorded replay UI and saves desktop/mobile screenshots. New network calls require separate explicit authority and durable reservations; no automatic retries.

Nov3 21:06IST: English monetary/prize qualifier advisories now annotate the evidence ledger and exports without rewriting values or quotes. Actual recorded p01 flags total and split. This deterministic heuristic can overflag negation or unrelated same-sentence context and miss other languages or conditions. It is a review aid, not an extraction fix or a new model-quality measurement.152offline tests pass; recorded provenance retained in both browser/Python exports; missing recorded fixture gives safe503, never a new APIcall.

## License

Original project code is released under the MIT License. See LICENSE. Meta model access and other third-party services remain subject to their own terms.
