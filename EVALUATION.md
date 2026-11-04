# Evaluation status

## What has actually been tested

- 131 offline unit/HTTP regression tests as of November3 20:39IST. One actual approved synthetic pilot, reported separately below.
- Local Chrome normal and conflict raw-text import/review/report flows; responsive overflow checks and visual inspection.
- Deterministic labeled-line parser on14 authored synthetic regression cases:14/14 exact match,9expected claims,zero extras/missing. These cases were developed alongside the parser, so this is not a generalization estimate.

## Prose evaluation frozen before live calls

`fixtures/prose-evaluation-v1.json`, SHA256 `d4e8583addcc5616d11ea7bd3c52ff9a6743846333c3230aebe3bc5ef8e1fb64`.

Eight synthetic prose cases authored by the same developer before any Meta inference: dates, negative AI policy, conditional non-cash prize, contradictory deadlines, separate licensing scopes, hostile instructions, impossible date and ambiguous timing. Expected source spans are validated, but no provider has been scored on them. This is not an independent or representative benchmark. Freeze the file; revisions get a new version/hash and must not silently replace failed cases.

For a future genuine model run, preserve sanitized source, exact request/model, response, finish status, token usage and timestamp. Report exact field/value match plus abstention on unsupported dates, conflict retention and evidence validity. Keep the no-effect boundary separate from extraction quality. Do not report gold answers replayed through a validator as model accuracy.

## Offline response replay

`python3 replay_response.py SOURCE.txt RESPONSE.json` validates a saved Chat Completions-shaped response and its exact source quotes. It always labels output SAVED RESPONSE REPLAY, live=false, remote_authorship_verified=false. A provider/model string is not authentication. Contributor, truncated, refused, malformed or unsupported responses are rejected. A separate one-shot network transport now exists, never invoked by this replay CLI.

## Known semantic limitation

A quote and matching substring can still be misleading, negated, conditional or irrelevant. Multiple distinct passages for a field are conservatively flagged as conflicting even when they might be complementary. No legal entitlement, eligibility, source authenticity or current website state is established by this tool. Human review is required.

## Scoring preparation

`python3 score_prose.py RESPONSES.json` scores all eight saved envelopes against the frozen set, checking its digest first. Invalid cases cannot count as correct abstentions. Always reports offline/unverified provenance. Gold-replay tests exercise the scoring code only, never reported as model performance.

## Bounded genuine-run preparation

`python3 prepare_model_run.py` emits eight standard-model requests for the frozen synthetic prose set, with exact source hashes, default sampling and max2048completion tokens/request (including reasoning). It loads no credentials, performs no network calls and authorizes no spending. Automatic retries are zero. A future approved execution must stop on the first billing/model/response error rather than silently retry or switch tiers. The manifest does not establish provider access, applied credits or no-overage. Offline regression tests do not measure model quality.

Protocol refresh Nov3: native Chat Completions guide recommends default sampling and `max_completion_tokens` rather than deprecated `max_tokens`. Requests now leave sampling unset and cap2048completion tokens, including reasoning. This can truncate reasoning: incomplete output is rejected, never silently retried or scored as valid. Protocol source: https://dev.meta.ai/docs/protocols/chat-completions . One-case mixed quality result now exists, below; no broader quality claim.

`record_response_evidence.py SOURCE.txt RESPONSE.json UTC_TIMESTAMP` validates a saved Standard envelope and produces source/request/sanitized-response hashes. Explicit model, complete choice, response ID, UTC timestamp and integer consistent token usage required. Unknown headers/metadata stripped. Output always says origin and timestamp unverified, zero network calls. Caller-supplied JSON is not provider-authenticated proof, even when quote validation passes.Rejection tests cover malformed metadata and unsupported claims; no provider claims follow from those tests.

Saved-envelope scoring also reports exact strict field/value precision and recall (null precision for no predictions), required/correct abstention counts, and preservation of multiple gold values. Multi-value preservation does not assert semantic contradiction: complementary license or conditional-prize passages can share a field. Invalid envelopes never count as correct abstentions. These are scorer unit checks, not measured Meta outcomes.117offline tests pass atNov3_19:51.

## Measured parser baseline on frozen prose, November3

The existing labeled-line offline parser was run unchanged on the eight frozen prose cases. It produced no claims:3/8exact cases (the three intended abstentions),0truepositive,0falsepositive,14missing field/value pairs. This is a parser measurement only, not a Meta result. Empty output avoids false positives here but fails to extract supported prose facts. It explains why the labeled14case regression result is not a generalization claim and why a genuine model comparison matters. No fixture, parser or prompt was tuned against this result. The structured per-case private diagnostic is excluded from source package; the frozen original cases remain unchanged.

The saved-response bridge connects validated claims to the existing import/review/export UI without changing its offline label. It does not authenticate remote origin or add a live transport. Both before/after source quotes and HTTPS labels are validated; unsupported text is rejected before persistent mutation.122offline tests pass atNov3_19:52. A genuine single approved call has since completed. It does not solve broader quality evaluation.


## First actual Meta pilot, 2026-11-03T15:06:49Z
- One direct API call, Standard `muse-spark-1.3`,2048completioncap,defaultsampling,nohostedtools,noretries. Source/prompt/gold unchanged from frozen p01. Response `chatcmpl-01a1a1f2-d968-7503-b547-670633c43c73`, finish `stop`.
- Usage259prompt,1778completion including1591reasoning,2037total. No cached tokens. Listed rate arithmetic US$0.00788025, not confirmed INR settlement/tax. No extra call after pilot.
- Strict field/value gold:3truepositive,1falsepositive,1falsenegative. Precision0.75, recall0.75, exactcasefalse. Prize lost "total" qualifier but retained full quote. Eligibility and both explicit-offset deadlines matched. This is developer-authored synthetic text, not an independently collected benchmark. No aggregate8case Meta score exists.
- `fixtures/meta-pilot01-recorded.json` preserves sanitized response and source. Source-only fixture cannot independently authenticate network origin; actual execution trace and private attempt ledger retained separately. UI explicitly says recorded replay, no new call. Baseline is empty illustrative comparison, not a measured earlier version.
- Deterministic review prompt now warns to check total-pool/per-winner/split/conditions from full reward passage. This is a review mitigation, not a measured extraction fix. No prompt/gold tuning or post-fix rerun.

Nov3 21:06IST: English monetary/prize qualifier advisories now annotate the evidence ledger and exports without rewriting values or quotes. Actual recorded p01 flags total and split. This deterministic heuristic can overflag negation or unrelated same-sentence context and miss other languages or conditions. It is a review aid, not an extraction fix or a new model-quality measurement.152offline tests pass; recorded provenance retained in both browser/Python exports; missing recorded fixture gives safe503, never a new APIcall.
