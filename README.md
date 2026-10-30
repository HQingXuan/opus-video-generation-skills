# Opus video generation skills

[中文说明](README.zh.md)

Reusable skills for code-rendered educational videos with Claude Opus: make a sample, produce an episode, extend a video, or draft a prompt. **English by default; add `中文` to switch.**

This release contains one skill with four modes, generalized from AWS explainers to other knowledge topics. It supplies instructions, not a bundled renderer, model subscription, or MCP server. Rendering requires a coding environment with file/command access and a suitable renderer.

## Install in Claude Code

Copy the entire skill directory, including its references:

```sh
git clone https://github.com/HQingXuan/opus-video-generation-skills.git
cd opus-video-generation-skills
mkdir -p ~/.claude/skills
test ! -e ~/.claude/skills/educational-video && cp -R educational/educational-video ~/.claude/skills/educational-video
```

An existing destination is left unchanged; review and back it up before replacing it. For one project, copy to that project's `.claude/skills/educational-video/` instead. On Windows, copy to `%USERPROFILE%\.claude\skills\educational-video\`. These locations follow the [official skills documentation](https://code.claude.com/docs/en/skills). Open Claude Code and invoke `/educational-video`.

Select Opus in your own environment if desired; the skill does not change models. Other agents supporting `SKILL.md` use their own installation conventions. Without skill support, paste the [common prompt base and one case](educational/educational-video/references/aws-cases.en.md); rendering still requires tools.

## Use

```text
/educational-video Create a 10-second preview explaining why the sky is blue.
/educational-video Create a 2-minute video about Amazon SQS.
/educational-video 中文 制作一个 3 分钟的 AWS Lambda 科普视频。
/educational-video --lang zh 只写一个 3 分半钟的 Amazon Bedrock 视频 prompt。
/educational-video Extend ./my-video to 3 minutes; preserve the opening and style.
/educational-video --lang en Create a 60-second vertical video about photosynthesis with narration.
```

These are prompts, not shell commands. `--lang` is interpreted by the model; there is no custom argument parser.

| Request | Mode | Result |
| --- | --- | --- |
| Sample / preview | `preview` | Short MP4, episode outline, editable project |
| Make a video | `full` | Complete MP4 and reproducible project |
| Extend an existing video | `extend` | Deeper explanation preserving available style/assets |
| Write a prompt | `prompt-only` | Self-contained prompt; no rendering or setup |

New videos default to English even when the request is Chinese. Explicit output-language requests override this: `中文` / `--lang zh` select Chinese; `English` / `--lang en` select English. Revisions retain the saved project language unless changed. The choice controls the workflow reference, captions, optional narration, and human-facing deliverables. API names and code identifiers remain intact. The Chinese instruction file is a translation of the same skill, not a second command.

Defaults: full video 120 seconds; preview 10 seconds within a 30-second outline; 1080p/30 fps; off-white/dark/orange diagrams; short captions; no narration. User instructions and existing project conventions override these. Preview-only requests stop at the preview; full production does not add an unsolicited approval round.

## Contents

```text
educational/educational-video/
  SKILL.md                         # discovered entry, English default
  SKILL.zh.md                      # matching Chinese instructions
  references/
    workflow.en.md / workflow.zh.md
    aws-cases.en.md / aws-cases.zh.md
docs/history.en.md / history.zh.md # earlier prompts and tool inventory
evals/cases.json                   # behavioral scenarios for an agent
scripts/validate.py                # offline package/link/timeline checks
```

The case library reconstructs eight prompt versions across six topics: SQS preview and extension, OpenSearch, DynamoDB, NLB, Bedrock at two durations, and Lambda. Each has timed scenes, data, caveats, and primary links. These are adaptations, not verbatim transcripts. The [history](docs/history.en.md) distinguishes discussed tools, actual use, and user-reported results.

## Validation and contributions

```sh
python3 scripts/validate.py
```

Requires Python 3.9+ with no third-party dependencies. Checks local links, self-contained packaging, translation pairs, bilingual timelines, and evaluation coverage. This does **not** run Opus, render video, or prove model compliance. See [behavioral evaluation instructions](evals/README.md). No historical videos are bundled; this release has not been end-to-end render-tested in Opus.

New skills belong in a topic category with English `SKILL.md` and Chinese `SKILL.zh.md`. Keep routing, constraints, references, and user docs equivalent; preserve API identifiers. Add behavioral cases for new modes. Load only relevant references at runtime.

## Why a skill first?

The reusable part is the workflow: evidence, explanation, timing, rendering, and review. A skill uses existing tools. A shared rendering service, asset store, or render-job API could justify MCP later; this package does not need a server.

## License and attribution

The existing [MIT license](LICENSE) is preserved. Third-party engines, fonts, music, and skills retain their own licenses and are not bundled. Inspiration and references are credited in the [history](docs/history.en.md). No affiliation with Anthropic or AWS is implied.
