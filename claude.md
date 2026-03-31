# vlm-research

## Purpose
Long-term repository for VLM practice and research.
Assume work here may be uploaded to GitHub.

## Structure
- `practice/`: implementations, prototypes, hands-on experiments
- `research/`: notes, comparisons, investigation, paper-oriented work

Before adding new work:
- inspect the existing repo structure first
- place new work intentionally
- avoid creating random top-level folders

## GitHub Rules
This repo should stay publishable.

Do not commit:
- secrets or tokens
- `.env` with real values
- private data
- local absolute paths
- cache files
- model weights
- large outputs or temporary artifacts
- machine-specific configs

If needed:
- update `.gitignore`
- use sample config files such as `.env.example`

## New Project Rule
For a new project in this repo:
- choose the right location first
- use a short GitHub-friendly folder name
- explain why that location fits
- check whether `.gitignore` needs updates

## Working Preference
Prefer:
- clean baselines
- readable structure
- small modular projects
- practical implementation order

Avoid:
- over-engineering
- unnecessary UI-first work
- silent repo restructuring

## Progress Visibility
When working in this repository, make progress easy to follow.

Briefly show:
- what was implemented
- why it was implemented that way
- current progress toward the goal
- what remains next

Do not leave the work as a black box.
Make it easy to understand where the project currently stands.