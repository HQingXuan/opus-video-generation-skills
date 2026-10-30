---
name: educational-video
description: Create, extend, or draft prompts for code-rendered educational explainer videos with source-backed storyboards, consistent visual style, and render checks. Use for science, engineering, and other knowledge explainers, including short previews and longer episodes. English by default; 中文 or --lang zh selects Chinese. Not for unrelated cinematic footage or automatic publishing.
---

# Educational video

Turn a question into a visual explanation: purpose → mechanism → concrete example → limitation → takeaway. Work in the user's current project and reuse its renderer when appropriate. This skill supplies a workflow, not a renderer or hosted service. It works with Opus in a coding environment; it does not select or require a particular model version.

## Route the request

1. **Language.** For a new video, default to English even when the surrounding request is Chinese. An explicit output-language request overrides this default. `--lang zh`, a standalone `中文` selector, or “make the video in Chinese” selects Chinese; `--lang en` or `English` selects English. A quoted title containing 中文 is not a selector. For revisions, retain the project's saved language unless explicitly changed. If the current request contradicts itself, ask one focused question before writing localized content. Treat these as instructions interpreted by the model, not executable CLI flags.
2. **Mode.** “Write a prompt” selects `prompt-only`; “sample/preview/样片” selects `preview`; extending an existing video selects `extend`; otherwise select `full`. An explicit request overrides these hints. If the user asks for a preview first and a full video afterward, follow that sequence and pause only when the user requested review before continuation. For “preview only”, stop after the preview.
3. **Context.** Read available source/reference assets and existing project instructions. Preserve established style when accessible. When a referenced earlier video is unavailable, say so, use stated preferences, and request the asset only if essential. Never claim to have inspected missing material.
4. Read only the selected workflow: [English](references/workflow.en.md) or [中文](references/workflow.zh.md). [中文 skill instructions](SKILL.zh.md) are a translated view of this same skill, not a second command.
5. For AWS episodes, also read the selected [English case library](references/aws-cases.en.md) or [中文案例库](references/aws-cases.zh.md). Treat its scenarios as examples, verify current primary docs, and adapt scope to the topic. Do not load AWS cases for unrelated subjects.

## Defaults and scope

User instructions and existing project conventions take priority. Otherwise use:

- Full video: 120 seconds. Preview: render 10 seconds within a proposed 30-second episode. Extension: requested total duration, or 120 seconds total if unspecified. State assumptions.
- 1920×1080, 16:9, 30 fps; off-white background, dark text, orange emphasis; simple labeled shapes, restrained motion, generous spacing. These are editable series defaults, not universal requirements.
- Short readable captions, no narration. Use authorized/generated audio when available; if audio is unavailable, deliver a silent preview and state that limitation. Do not silently add paid services.
- One audience, one central question, one traceable example. Explain terms before using them. Labels, subtitles, narration if requested, and human-facing deliverables use the selected language; preserve API names, source titles, code identifiers, and requested bilingual terms.
- Educational simulations need no live cloud credentials or infrastructure. Render locally where tools permit. Do not provision resources, send messages, or publish the video as an incidental part of this workflow.

## Completion contract

- **Prompt-only:** deliver a self-contained, paste-ready prompt with language, duration, audience, visual rules, timed scenes, verified facts/caveats, renderer fallback, and acceptance checks. Include relevant instructions inline so the recipient does not need this skill installed. No rendering or setup unless requested.
- **Preview:** deliver the agreed sample, full-episode outline, editable sources, sampled frames, and honest QA notes. Do not label a 10-second preview as a completed two-minute video.
- **Full / extend:** deliver the final video, editable project, shared timeline, storyboard, factual sources, asset provenance, reproduction command, and QA report. Reuse existing filenames/conventions where practical.
- If tools block rendering, complete the storyboard and runnable project as far as possible, report the exact missing capability and unexecuted checks, and label the result unrendered. Never substitute a success claim for a missing artifact.

Follow the workflow through the requested deliverable. Review gates exist only when the user requests one or essential information is missing.
