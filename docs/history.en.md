# History, prompts, and tool provenance

This document separates the earlier conversation from the reusable skill created on 2026-10-29. The case library is a reconstruction, not an exact transcript archive. No third-party skill code or original social-media prompt text has been copied into this package.

## What the prompts converged on

The sequence progressed from a 10-second style test to two-minute service explanations, then to longer videos when the mechanism required more room. The shared format became: one practical question, one continuing example, causal diagrams, short captions, a consistent visual identity, and explicit technical limits.

| Prompt version | Duration | Distinct contribution |
| --- | --- | --- |
| SQS preview | Render 10 s; plan 30 s | Validate style; accepted is different from completed |
| SQS extension | About 120 s | Add lifecycle, visibility, duplicates, capacity, DLQ |
| OpenSearch | About 120 s | Documents → terms → candidates → filters → freshness |
| DynamoDB | About 120 s | Access patterns, composite keys, Query/Scan, GSI |
| NLB | About 120 s | Connection routing, health delay, cross-zone scope |
| Bedrock original | About 120 s | Application, model, retrieval, generation |
| Bedrock expanded | About 210 s | Separate ingestion from queries; insufficient evidence and authorization |
| Lambda | About 180 s | Events, execution environments, retries, two permission boundaries |

The [English case library](../educational/educational-video/references/aws-cases.en.md) and [Chinese case library](../educational/educational-video/references/aws-cases.zh.md) preserve the key scenes, example data, and caveats. The original prompts were Chinese; English versions are new adaptations. Prior duration ranges are recorded as history, while the reusable workflow uses a stated target and tolerance.

## Inspiration from the two posts

- [laobaishare: repository collection](https://x.com/laobaishare/status/2108533494725103926): a map of design skills, render engines, and animation libraries. It is a collection from multiple maintainers, not a single unified product.
- [Tom CC: production experience](https://x.com/Tom_CC_9986/status/2108512799517450287): repeatable style, an engaging question, short previews, synchronization of captions/motion/music, and factual review. The paper-and-ink style and a particular 17-second music cue belong to that example, not this generic workflow.

The earlier research notes recorded that the post bodies and selected repositories were read on 2026-10-10. Embedded videos and claimed audience/revenue outcomes were not independently verified. Neither viral performance nor model superiority is a promise of this skill. The third post about multi-model teams is outside the video package; no team orchestration dependency was added.

## Referenced engines and skills

These were reviewed as documentation, not installed or run during the earlier research:

| Project | Idea retained |
| --- | --- |
| [claude-motion](https://github.com/whaleyxbt/claude-motion) | A shared timeline coordinates scenes, sound, and review; contact sheets sample beats |
| [claude-motion-design](https://github.com/howseen-ai/claude-motion-design) | HTML/Playwright/ffmpeg and deterministic seek(t); iterative visual review |
| [HyperFrames](https://github.com/heygen-com/hyperframes) | HTML/CSS animation rendered through browser tools |
| [Remotion](https://github.com/remotion-dev/remotion) | React and frame-based programmatic video |
| [Remotion skills](https://github.com/remotion-dev/skills) | Engine-specific guidance when Remotion is selected |

Other links recorded from the original collection are listed below for completeness. Their names do not constitute endorsement, current availability checks, installation, or compatibility testing:

- [charlie947/motion-graphics-skills](https://github.com/charlie947/motion-graphics-skills)
- [haidrrrry/claude-remotion-skill](https://github.com/haidrrrry/claude-remotion-skill)
- [t3knobox/klik-anim-skill-creation](https://github.com/t3knobox/klik-anim-skill-creation)
- [Sunwood-ai-labs/hyperframes-motion-reel-skill](https://github.com/Sunwood-ai-labs/hyperframes-motion-reel-skill)
- [AbubakrChan/product-launch-motion](https://github.com/AbubakrChan/product-launch-motion)
- [cth9191/animate](https://github.com/cth9191/animate)
- [iart-ai/motion-design-skills](https://github.com/iart-ai/motion-design-skills)
- [nateherkai/hyperframes-student-kit](https://github.com/nateherkai/hyperframes-student-kit)
- [greensock/GSAP](https://github.com/greensock/GSAP)
- [LottieFiles/motion-design-skill](https://github.com/LottieFiles/motion-design-skill)
- [frankxai/awesome-motion-design-agent-skills](https://github.com/frankxai/awesome-motion-design-agent-skills)
- [Barty-Bart/motion-graphics](https://github.com/Barty-Bart/motion-graphics)
- [199-biotechnologies/motion-dev-animations-skill](https://github.com/199-biotechnologies/motion-dev-animations-skill)
- [motiondivision/motion](https://github.com/motiondivision/motion)
- [airbnb/lottie-web](https://github.com/airbnb/lottie-web)

## What was actually used

- The earlier research used the local `research` workflow, web/browser inspection, and a research helper agent. These organized source gathering; they were not video-rendering dependencies.
- Earlier prompt drafting used `writing-for-agents` guidance. This package was authored with `skill-creator` and `writing-for-agents` guidance. These authoring aids are not required for people installing this skill.
- The user reported that the SQS 10-second sample looked good. The sample was produced outside this repository; its source, render command, and media are unavailable here. No equivalent success is claimed for every later topic.
- This repository contributes a new `educational-video` skill with English and Chinese instructions. Its packaging can be validated locally; actual Opus behavior and end-to-end video quality require the separate evaluation procedure.

## What became generic

Keep the workflow, not the accidental details: source-backed facts; explicit scenario boundaries; timed storyboards; deterministic rendering; readability; deeper content when extending; reproducible outputs; truthful verification status. Defaults such as color, aspect ratio, duration, audio, and language can be overridden. AWS-specific semantics live in optional case references, not in the core skill.

A skill is the first delivery because these are model instructions and workflow knowledge. MCP is deferred until there is a concrete remote rendering, asset-management, or job-control capability to expose.
