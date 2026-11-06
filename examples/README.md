# Synthetic local report walkthrough

Input: [fictional Atlas requirements](input/Project_Atlas/requirements.md). Output: [comprehensive report](output/input_COMPREHENSIVE_AI_18_56_06_11_26.md), [overview](output/input_OVERVIEW_AI_18_56_06_11_26.md), [project report](output/input_Project_Atlas_PROJECT_18_56_06_11_26.md), and [cross-project report](output/input_CROSS_PROJECT_ANALYSIS_18_56_06_11_26.md).

Run on 2026-11-06 with Python 3.9.6. Result: one Markdown file analyzed, one project detected, four Markdown reports generated, exit status 0. The existing basic test runner also passed five tests. This is a narrow Markdown demonstration; PDF, Excel, HTML, legacy DOC, and AI behavior were not validated.

## Reproduce in an isolated environment

Use a fresh environment with no provider credentials, no `.env`, and no AI SDKs installed:

```bash
python3 -m venv .venv-example
source .venv-example/bin/activate
python -m pip install chardet==5.2.0 pyyaml==6.0.3 python-dotenv==1.2.1
python docguru.py examples/input
```

The command generates a timestamped folder under `Reports/`. The minimal environment is for this Markdown example, not all file types. The checked run also had python-docx, lxml, Pillow, and click installed for the separate conversion example; format analyzers absent from the environment reported limited availability.

## AI limitation discovered during validation

Although the CLI prints `AI Analysis: Disabled` without `--ai`, the report generator initializes AI independently and can request project/cross-project analysis when configured. The flag alone is not a reliable way to prevent AI calls. This example had no available provider and made no AI request. A follow-up fix should pass the explicit AI choice through report generation and test it with a provider stub that fails on any unexpected call.

Generated filenames and some headings still contain `AI` even in this run; those labels do not prove AI use. Reports say AI analysis was unavailable. Trailing whitespace was normalized and the absolute input path was replaced with `examples/input` in the published copies; content and counts remain generated output.
