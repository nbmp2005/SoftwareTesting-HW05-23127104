# Report artifact contract

Use this reference whenever a HW05 skill is asked to create, fill, or revise a Markdown deliverable.

## Managed files and ownership

| Artifact | Canonical file | May be updated when |
| --- | --- | --- |
| Main report | `report/MAIN_REPORT.md` | a reviewed design, verified execution evidence, or parsed analysis changes the corresponding section |
| AI critique | `report/AI_CRITIQUE.md` | a real, numeric misinterpretation finding is available |
| AI audit | `report/AI_AUDIT_REPORT.md` | the user explicitly invokes the audit logger or a design gate requires its audit entry |
| Submission checklist | `report/SUBMISSION_CHECKLIST.md` | artifact inventory or verification status changes |
| Repository summary | `README.md` | an evidence-backed scenario summary, threshold, issue count, or video/repository link changes |

The existing report files are canonical templates. Update the smallest relevant section; do not replace the whole document, erase prior audit history, or convert a real value back to a placeholder.

## Safe update protocol

1. Read the target file and locate its named heading/table before editing.
2. Build a field-to-source map: every non-placeholder fact needs a path, command output, screenshot, raw JTL/JSON location, or explicit user-provided value.
3. Preserve unresolved fields as `TODO (REAL EVIDENCE REQUIRED)` (or the more specific existing TODO). Never infer a missing result.
4. Apply an idempotent update: replace only the row, table cell, or paragraph for the current scenario/attempt. Keep historical attempts in run notes rather than overwriting them.
5. Update cross-links and the artifact index/checklist in the same change when a new file is created or verified.
6. Re-read the edited Markdown and verify headings, table separators, links, filenames, and scenario names. Report exactly which files and sections changed.

## Required provenance by content

| Content written | Required provenance |
| --- | --- |
| Workflow, contract, correlation, candidate workload | reviewed source/API contract and human approval; label candidates as not measured |
| JMX/CSV/JTL/HTML path and run configuration | inspected artifact plus matching run notes |
| Metrics | parser JSON path plus raw JTL identity; stage/phase claims also need real time windows |
| CPU/RAM/hardware | inspected same-frame resource/hardware evidence; do not derive peaks from a single unrelated image |
| Threshold/conclusion | stable run evidence, raw JTL analysis, and resource observations |
| AI critique | frozen AI claim and a real numeric correction with file/label/window provenance |
| AI audit timestamp | actual clock/tool timestamp at append time; prompt must remain verbatim |

## Scenario update map

For each Load, Stress, or Spike attempt, maintain one traceable chain in `report/MAIN_REPORT.md`: final configuration, evidence paths, raw JTL/JSON metrics, resource observation, verdict, and limitations. Mirror only the concise verified summary in `README.md`; retain detail in the main report. When an expected artifact is absent, update `report/SUBMISSION_CHECKLIST.md` with the missing item instead of manufacturing a report row.

