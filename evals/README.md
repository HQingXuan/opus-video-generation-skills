# Evaluation

[中文](README.zh.md)

## Offline package checks

Run `python3 scripts/validate.py` from the repository root. It checks local links, portable skill references, English/Chinese file pairs, the eight case timelines (including continuity and final duration), and coverage in [cases.json](cases.json).

This validates packaging, not semantic translation quality or model behavior. Review paired instructions for equivalent routing, defaults, overrides, and completion rules. Review factual examples against their primary sources before production.

## Behavioral checks with Opus

Install the skill in a disposable test project. Use a fresh conversation per case in [cases.json](cases.json), with the stated context/fixtures. Record the actual model version, date, tools available, prompt, output files, and each check's pass/fail/unverified result. Use a model configured by the evaluator; the skill does not select it.

Planning/prompt-only cases can be evaluated without rendering. Rendering cases require a local engine, browser where relevant, and encoder. Run requests as written if testing the complete behavior. A plan-only dry run of a full-mode case can check routing, but cannot count as passing its rendering criteria.

For the extension fixture, first create an actual preview project and save `language: zh` in its brief; then provide that directory. For the missing-renderer scenario, enforce the described restriction. For the unrelated-request case, make the skill discoverable but do not explicitly invoke it.

The twelve cases cover default English, Chinese triggers, explicit overrides, retained project language, conflicting selectors, prompt-only scope, preview stopping, extensions, non-AWS content, unavailable tools, missing references, and unrelated requests. A failed factual or output-language check requires fixing both language versions where applicable, then rerunning affected cases.

For a real rendered sample, inspect key/transition frames, confirm deterministic repeated seeks, check metadata, and play/listen when available. Record which checks were actually performed. A contact sheet alone cannot pass the playback/audio checks.

## Current evidence

This repository includes structural validation and behavioral test specifications. It does not include an Opus evaluation transcript or newly rendered sample. Do not report the behavioral scenarios as passed merely because the JSON parses. The historical SQS preview result is user-reported, as explained in [the provenance record](../docs/history.en.md).
