<div align="center">

# Opus 视频生成技能

**把一个问题做成科普视频，保留可编辑的代码、清晰的讲解和可复用的制作流程。**

[English](README.md) · **简体中文**

[快速开始](#快速开始) · [使用场景](#选择你要完成的任务) · [语言切换](#选择输出语言) · [案例库](#案例库) · [文档导航](#文档导航)

</div>

---

告诉 Claude Opus 主题、受众和目标时长，skill 会指导它完成资料核实、分镜、动画和审阅，让讲解有据可查，也让视频工程便于继续修改。

首个 skill **`educational-video`** 来自我们制作 AWS 系列讲解的经验，也适用于科学、工程和其他知识题材。你可以从短样片开始，直接制作完整视频，扩展已有作品，或只生成一段交给其他 agent 使用的 prompt。

> **默认英文。** 加上 `中文` 或 `--lang zh` 即可切换中文输出。一次安装同时包含两个语言版本。

## 快速开始

下面的斜杠命令在 Claude Code 中使用。实际渲染还需要 agent 能读写文件、执行命令，并具备合适的渲染器，例如 Remotion 或基于 HTML 与浏览器的流程。本 skill 提供制作指导，不捆绑渲染器或模型订阅。

### 1. 获取仓库

```sh
git clone https://github.com/HQingXuan/opus-video-generation-skills.git
cd opus-video-generation-skills
```

### 2. 安装 skill

将**整个文件夹**连同参考资料复制到个人 skills 目录：

```sh
mkdir -p ~/.claude/skills

if [ -e ~/.claude/skills/educational-video ]; then
  echo "Skill already exists. Review and back it up before replacing it."
else
  cp -R educational/educational-video ~/.claude/skills/educational-video
fi
```

安装后，你的本地 Claude Code 项目都可以使用它。若目标目录已存在，这段命令会保留原有安装。

<details>
<summary><strong>只在一个项目中安装，或使用 Windows</strong></summary>

只在一个项目使用时，将文件夹复制到该项目的 `.claude/skills/educational-video/`。

Windows 用户可复制到：

```text
%USERPROFILE%\.claude\skills\educational-video\
```

无论哪种方式，都要将 `SKILL.md`、`SKILL.zh.md` 和整个 `references/` 目录一起保留。安装位置依据 [Claude Code 官方 skills 文档](https://code.claude.com/docs/en/skills)。

</details>

### 3. 先做一个小样片

在准备保存视频工程的项目中打开 Claude Code，按需要选择 Opus，然后输入：

```text
/educational-video 中文 做一个 10 秒样片，解释天空为什么是蓝色的。
```

Agent 应交付短样片、完整视频提纲和可编辑工程文件。若缺少渲染工具，应说明缺少什么，并明确标记产物尚未渲染。

Skill 不修改模型选择。本 README 中的 `/educational-video` 示例都是输入 Claude Code 的 prompt，不是 shell 命令。

## 选择你要完成的任务

### 先验证一个概念

用短样片确认视觉方向和可读性，再投入更长的视频。需要先审核时，明确要求 agent 等待。

```text
/educational-video 中文 只做一个 10 秒的 SQS 样片，等我审核后再继续。
```

**交付物：** 短 MP4、完整视频提纲、可编辑源码、抽样帧和 QA 记录。

### 制作完整的一期

给出主题与时长，让 agent 规划讲解、实现动画、检查结果，并完成视频交付。

```text
/educational-video 中文 制作一个 2 分钟的视频，解释 Amazon SQS 如何解耦 producer 和 worker。
```

**交付物：** 完整视频、可编辑工程、分镜、时间线、来源和复现说明。完整制作不会额外强制一次审批。

### 扩展已有视频

提供实际工程路径，让 agent 沿用已有开头、素材和视觉风格。增加的时间用于深入讲解、补充例子或展示失败场景。

```text
/educational-video 将 ./my-video 扩展到 3 分钟，保留已认可的开头，加入失败和重试的例子。
```

**交付物：** 基于现有工程扩展的视频，以及更新后的时间安排和检查记录。未明确切换语言时，沿用项目保存的语言。

### 只生成 prompt

适合先审阅制作要求，或把任务交给另一个 agent。

```text
/educational-video 中文 写一段完整的 prompt，用于制作 3 分钟的 AWS Lambda 科普视频。不要渲染视频。
```

**交付物：** 可直接复制的 prompt，包含定时分镜、视觉规则、事实边界、来源链接和验收要求。不渲染，也不安装依赖。

## 选择输出语言

| 想要的输出 | 如何指定 |
| --- | --- |
| 英文 | 无需添加参数，新视频默认使用英文 |
| 中文 | 添加 `中文` 或 `--lang zh` |
| 切回英文 | 添加 `English` 或 `--lang en` |

例如：

```text
/educational-video 中文 制作一个 3 分钟的 AWS Lambda 科普视频。
```

```text
/educational-video --lang zh 只写一个 3 分半钟的 Amazon Bedrock 视频 prompt。
```

所选语言用于字幕、可选旁白、工作流参考和面向人的交付说明。API 名称与代码标识符保持原样。

- 仅用中文提问不会改变默认英文的规则；需要明确要求中文输出。
- 修改现有项目时，沿用保存的语言，除非明确切换。
- `--lang` 由模型理解，不是自定义的 CLI 参数解析器。
- `SKILL.zh.md` 是同一个 skill 的中文版本，不是另一个斜杠命令。

## 制作流程

1. **明确问题。** 确定受众、一个核心结论、时长、语言与输出格式。
2. **核实事实。** 查阅一手来源，说明假设，将示意数据标清楚。
3. **编写分镜。** 用一个具体例子贯穿定时场景，配上可读的字幕。
4. **实现动画。** 复用合适的渲染器，让画面、字幕和音频使用共享时间线。
5. **检查结果。** 审阅场景与转场帧，核对媒体参数，在条件允许时检查播放与音频。
6. **交付工程。** 提供视频、可编辑源码、复现命令和如实的检查记录。

Contact sheet 只能说明抽样帧经过检查，不能证明完整播放或试听过视频。工作流要求 agent 区分这些验证状态。

## 案例库

目前包含 **6 个 AWS 主题、8 个重建整理的 prompt 版本**。每个案例都有具体场景、时间分镜、技术边界和一手来源链接。

| 主题 | 时长 | 讲解重点 |
| --- | --- | --- |
| Amazon SQS | 10 秒样片 + 2 分钟扩展版 | 接受与完成、visibility timeout、重试、DLQ |
| Amazon OpenSearch Service | 2 分钟 | 文档、倒排索引、相关性、过滤、更新可见性 |
| Amazon DynamoDB | 2 分钟 | 访问模式、复合键、Query 与 Scan、GSI |
| Network Load Balancer | 2 分钟 | TCP 连接、健康检查、跨 AZ 路由 |
| Amazon Bedrock | 2 分钟 + 3 分半钟扩展版 | 检索、生成、证据和授权 |
| AWS Lambda | 3 分钟 | 事件、执行环境、重试和权限 |

**查看案例：** [English](educational/educational-video/references/aws-cases.en.md) · [中文](educational/educational-video/references/aws-cases.zh.md)

这些是先前 prompt 的可复用改写，不是逐字对话，也不包含视频演示文件。[历史与工具清单](docs/history.zh.md)记录了来源，并区分参考过的工具与实际使用情况。

## 自定义视频形式

下面是制作起点。你明确提出的要求和现有项目约定优先。

| 设置 | 默认值 |
| --- | --- |
| 完整视频 | 120 秒 |
| 样片 | 计划中的 30 秒视频，先制作 10 秒 |
| 画布 | 1920 × 1080 · 16:9 · 30 fps |
| 视觉风格 | 米白背景、深色文字、橙色强调 |
| 图形 | 有标签的图示、克制动效、充足留白 |
| 文字 | 简短、可读的字幕 |
| 旁白 | 默认关闭，按要求添加 |

需要其他形式时，直接说明：

```text
/educational-video 中文 制作一个面向儿童的 60 秒竖屏视频，解释光合作用。使用绿色配色，并添加旁白。
```

## 文档导航

| 文档 | English | 中文 |
| --- | --- | --- |
| Skill 指令 | [SKILL.md](educational/educational-video/SKILL.md) | [SKILL.zh.md](educational/educational-video/SKILL.zh.md) |
| 制作工作流 | [Workflow](educational/educational-video/references/workflow.en.md) | [制作流程](educational/educational-video/references/workflow.zh.md) |
| AWS prompt 库 | [Cases](educational/educational-video/references/aws-cases.en.md) | [案例库](educational/educational-video/references/aws-cases.zh.md) |
| 历史 prompt 与工具 | [History](docs/history.en.md) | [历史整理](docs/history.zh.md) |
| 行为评估 | [Evaluation guide](evals/README.md) | [评估说明](evals/README.zh.md) |

<details>
<summary><strong>仓库目录结构</strong></summary>

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
docs/                   # 历史 prompt 与工具来源
evals/                  # 行为场景与评估说明
scripts/validate.py     # 离线打包检查
```

</details>

## 验证与贡献

使用 Python 3.9+ 运行离线检查，无需第三方 Python 依赖：

```sh
python3 scripts/validate.py
```

检查覆盖本地链接、独立安装所需文件、翻译配对、双语时间线和评估场景覆盖。仓库还提供 [12 个行为场景](evals/cases.json)，用于实际测试 agent。

> **验证范围：** 打包检查不会运行 Opus 或渲染视频。本版本尚未在 Opus 中完成端到端渲染测试，也不包含历史成片。

贡献时请：

- 将新 skill 放在题材分类下，同时提供 `SKILL.md` 和 `SKILL.zh.md`。
- 保持双语路由、限制、参考资料和用户文档等价。
- 为新增模式补充行为场景，让题材专属参考仍然按需加载。

## 其他环境与 MCP

其他支持 `SKILL.md` 的 agent 可使用各自的安装方式。不支持 skill 时，可以把[通用 prompt 底稿和一个案例](educational/educational-video/references/aws-cases.zh.md)复制给 agent。渲染仍然需要合适的工具。

当前复用的是制作工作流，因此先以 skill 包交付。如果以后需要共享渲染服务、素材库或渲染任务 API，再考虑增加 MCP 服务。

---

[MIT 许可证](LICENSE) · [灵感与来源](docs/history.zh.md)

第三方引擎、字体、音乐和 skills 保留各自的许可，本仓库不捆绑它们。本项目与 Anthropic 或 AWS 没有隶属关系。
