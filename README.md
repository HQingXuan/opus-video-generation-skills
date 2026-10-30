<div align="center">

# Opus Video Generation Skills

**Turn a question into an educational video — with editable code, clear explanations, and a repeatable workflow.**

**English** · [简体中文](README.zh.md)

[Quick start](#quick-start) · [Usage](#choose-your-task) · [Language](#choose-your-language) · [Examples](#example-library) · [Documentation](#documentation)

</div>

---

Give Claude Opus a topic, an audience, and a target duration. The skill guides it through research, storyboarding, animation, and review, keeping the explanation grounded in sources and the video project editable.

The first skill, **`educational-video`**, grew out of a series of AWS explainers. You can also use it for science, engineering, and other knowledge topics. Start with a short sample, build a full episode, expand an existing video, or ask for a prompt to use elsewhere.

> **English by default.** Add `中文` or `--lang zh` for Chinese output. Both language versions are included in the same installation.

## Quick start

You need Claude Code to use the slash command below. To render video, the agent also needs file and command access plus a suitable renderer, such as Remotion or an HTML/browser-based pipeline. The skill provides the workflow; it does not bundle a renderer or model subscription.

### 1. Get the repository

```sh
git clone https://github.com/HQingXuan/opus-video-generation-skills.git
cd opus-video-generation-skills
```

### 2. Install the skill

Copy the **whole folder**, including its references, into your personal skills directory:

```sh
mkdir -p ~/.claude/skills

if [ -e ~/.claude/skills/educational-video ]; then
  echo "Skill already exists. Review and back it up before replacing it."
else
  cp -R educational/educational-video ~/.claude/skills/educational-video
fi
```

This makes the skill available across your local Claude Code projects. An existing installation is left unchanged.

<details>
<summary><strong>Project-only installation or Windows</strong></summary>

For a single project, copy the folder into that project's `.claude/skills/educational-video/` instead.

On Windows, copy it to:

```text
%USERPROFILE%\.claude\skills\educational-video\
```

In either case, keep `SKILL.md`, `SKILL.zh.md`, and the entire `references/` directory together. Installation locations follow the [official Claude Code skills documentation](https://code.claude.com/docs/en/skills).

</details>

### 3. Make a small first video

Open Claude Code in the project where you want to create the video. Select Opus in your environment if desired, then enter:

```text
/educational-video Create a 10-second preview explaining why the sky is blue.
```

The agent should produce a short sample, an outline for the episode, and editable project files. If rendering tools are unavailable, it should identify the missing capability and clearly label the work as unrendered.

The skill does not change your model selection. All `/educational-video` examples in this README are prompts entered in Claude Code, not shell commands.

## Choose your task

### Preview a concept

Check the visual direction and readability before investing in a longer video. Ask explicitly if you want the agent to wait for your review.

```text
/educational-video Make only a 10-second SQS preview. Wait for my review before continuing.
```

**Result:** a short MP4, an episode outline, editable sources, sampled frames, and QA notes.

### Produce a complete episode

Give the agent a subject and duration. It should plan the explanation, implement the animation, inspect it, and deliver the requested video.

```text
/educational-video Create a 2-minute video explaining how Amazon SQS decouples a producer from a worker.
```

**Result:** the full video, editable project, storyboard, timeline, sources, and reproduction instructions. Full production does not add an unsolicited approval round.

### Extend an existing video

Point to the actual project so the agent can preserve its opening, assets, and visual style. Extra time should add explanation, examples, or a failure case.

```text
/educational-video Extend ./my-video to 3 minutes. Keep the approved opening and add a failure-and-retry example.
```

**Result:** a longer video built from the available project, with updated timing and verification notes.

### Generate a prompt only

Use this when you want to review the production brief or give it to another agent.

```text
/educational-video Write a self-contained prompt for a 3-minute AWS Lambda explainer. Do not render the video.
```

**Result:** a paste-ready prompt with timed scenes, visual rules, factual boundaries, source links, and acceptance checks. No rendering or dependency setup.

## Choose your language

| Desired output | What to add |
| --- | --- |
| English | Nothing — this is the default for new videos |
| Chinese | `中文` or `--lang zh` |
| Switch back to English | `English` or `--lang en` |

For example:

```text
/educational-video 中文 制作一个 3 分钟的 AWS Lambda 科普视频。
```

```text
/educational-video --lang zh 只写一个 3 分半钟的 Amazon Bedrock 视频 prompt。
```

The selected language applies to captions, optional narration, the workflow reference, and human-facing deliverables. API names and code identifiers stay intact.

- A Chinese request alone does not change the English default; explicitly ask for Chinese output.
- Revisions keep the language saved in the existing project unless you change it.
- `--lang` is an instruction interpreted by the model, not a custom CLI parser.
- `SKILL.zh.md` is the Chinese version of the same skill, not a separate slash command.

## How production works

1. **Define the question.** Establish the audience, one takeaway, duration, language, and output format.
2. **Check the facts.** Use primary sources, state assumptions, and label illustrative data.
3. **Write the storyboard.** Follow one concrete example through timed scenes and readable captions.
4. **Build the animation.** Reuse an appropriate renderer and drive visuals, captions, and audio from a shared timeline.
5. **Inspect the result.** Review scene and transition frames, verify media metadata, and check playback and audio where available.
6. **Deliver the project.** Include the video, editable sources, reproduction commands, and an honest record of completed checks.

A contact sheet is evidence of sampled frames, not proof that the full video was played or its audio reviewed. The workflow requires the agent to distinguish those checks.

## Example library

The library contains **eight reconstructed prompt versions across six AWS topics**. Each includes a concrete scenario, timed scenes, technical caveats, and primary-source links.

| Topic | Duration | What the example explains |
| --- | --- | --- |
| Amazon SQS | 10-second preview + 2-minute extension | Acceptance vs. completion, visibility timeout, retries, and DLQs |
| Amazon OpenSearch Service | 2 minutes | Documents, inverted indexes, relevance, filtering, and freshness |
| Amazon DynamoDB | 2 minutes | Access patterns, composite keys, Query vs. Scan, and GSIs |
| Network Load Balancer | 2 minutes | TCP connections, health checks, and cross-zone routing |
| Amazon Bedrock | 2 minutes + expanded 3½-minute version | Retrieval, generation, evidence, and authorization |
| AWS Lambda | 3 minutes | Events, execution environments, retries, and permissions |

**Browse the cases:** [English](educational/educational-video/references/aws-cases.en.md) · [中文](educational/educational-video/references/aws-cases.zh.md)

These are reusable adaptations of the earlier prompts, not verbatim transcripts or bundled video demonstrations. The [history and tool inventory](docs/history.en.md) records their origin and distinguishes reviewed tools from actual use.

## Customize the format

These are starting points. Your explicit instructions and existing project conventions take priority.

| Setting | Default |
| --- | --- |
| Full video | 120 seconds |
| Preview | 10 seconds within a proposed 30-second episode |
| Canvas | 1920 × 1080 · 16:9 · 30 fps |
| Visual style | Off-white background, dark text, orange emphasis |
| Graphics | Labeled diagrams, restrained motion, generous spacing |
| Text | Short, readable captions |
| Narration | Off unless requested |

For a different format, describe it directly:

```text
/educational-video Create a 60-second vertical video about photosynthesis for children. Use a green palette and add narration.
```

## Documentation

| Resource | English | 中文 |
| --- | --- | --- |
| Skill instructions | [SKILL.md](educational/educational-video/SKILL.md) | [SKILL.zh.md](educational/educational-video/SKILL.zh.md) |
| Production workflow | [Workflow](educational/educational-video/references/workflow.en.md) | [制作流程](educational/educational-video/references/workflow.zh.md) |
| AWS prompt library | [Cases](educational/educational-video/references/aws-cases.en.md) | [案例库](educational/educational-video/references/aws-cases.zh.md) |
| Earlier prompts and tools | [History](docs/history.en.md) | [历史整理](docs/history.zh.md) |
| Behavioral evaluation | [Evaluation guide](evals/README.md) | [评估说明](evals/README.zh.md) |

<details>
<summary><strong>Repository structure</strong></summary>

```text
educational/
└── educational-video/
    ├── SKILL.md
    ├── SKILL.zh.md
    └── references/
        ├── workflow.en.md
        ├── workflow.zh.md
        ├── aws-cases.en.md
        └── aws-cases.zh.md
docs/                   # Prompt history and tool provenance
evals/                  # Behavioral scenarios and evaluation guidance
scripts/validate.py     # Offline package checks
```

</details>

## Validation and contributions

Run the offline checks with Python 3.9+; no third-party Python dependencies are needed:

```sh
python3 scripts/validate.py
```

The checks cover local links, self-contained skill packaging, translation pairs, bilingual timelines, and evaluation coverage. The repository also includes [12 behavioral scenarios](evals/cases.json) for testing with an agent.

> **Validation scope:** package checks do not run Opus or render video. This release has not been end-to-end render-tested in Opus, and historical video files are not included.

When contributing:

- Put new skills in a topic category and provide both `SKILL.md` and `SKILL.zh.md`.
- Keep routing, constraints, references, and user documentation equivalent across languages.
- Add behavioral cases for new modes, and keep topic-specific references optional at runtime.

## Other environments and MCP

Other agents that support `SKILL.md` can use their own installation conventions. Without skill support, paste the [common prompt base and one case](educational/educational-video/references/aws-cases.en.md) into your agent. Rendering still requires suitable tools.

The reusable component here is a production workflow, so this release is a skill package. A shared rendering service, asset store, or render-job API could justify an MCP server later.

---

[MIT License](LICENSE) · [Inspiration and attribution](docs/history.en.md)

Third-party engines, fonts, music, and skills retain their own licenses and are not bundled. This project is not affiliated with Anthropic or AWS.
