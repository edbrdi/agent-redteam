# Security assessment — {{target_name}}

**Engagement:** {{engagement_id}} · **Date:** {{date}} · **Tester:** {{tester}}
**Environment:** {{environment}} · **Model:** {{model}}

## Executive summary

{{exec_summary}}

## Findings

{{findings_table}}

{{findings}}

## What held

{{Significant attempted classes that did not break — useful for the owner and for retests.}}

## Recommendations (defence in depth)

1. Enforce a trust boundary: retrieved documents, emails, web pages, tool results and memory are data, never instructions.
2. Move authorisation into code: scoped credentials, allowlists, amount/recipient limits, confirmation tokens issued by the user turn.
3. Add provenance and tenancy to retrieval; strip hidden text and metadata before indexing.
4. Sanitise model output before rendering; do not auto-open links or images.
5. Log every tool call with the triggering message and the authorisation source; add rate and cost limits.

## Limitations

- {{what could not be observed}}
- {{cases skipped and why}}
- {{environment differences vs production}}

## Regression

Run `regression/` after fixes (see `regression/README.md`). A finding is closed only when its case holds and the benign baseline is unchanged.