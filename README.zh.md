# Opus 视频生成技能

[English](README.md)

让 Claude Opus 制作代码渲染的科普视频：做样片、制作完整视频、扩展视频，或编写 prompt。**默认英文，加 `中文` 即可切换。**

首版包含一个 skill、四种模式，将 AWS 讲解的经验推广到其他知识题材。仓库提供制作指令，不内置渲染器、模型订阅或 MCP 服务。渲染需要能读写文件、执行命令的编程环境和合适的渲染器。

## 在 Claude Code 中安装

复制整个 skill 目录，包括 references：

```sh
git clone https://github.com/HQingXuan/opus-video-generation-skills.git
cd opus-video-generation-skills
mkdir -p ~/.claude/skills
test ! -e ~/.claude/skills/educational-video && cp -R educational/educational-video ~/.claude/skills/educational-video
```

目标已存在时不会覆盖；先检查并备份再替换。只在一个项目使用时，复制到该项目的 `.claude/skills/educational-video/`。Windows 复制到 `%USERPROFILE%\.claude\skills\educational-video\`。安装位置依据 [官方 skills 文档](https://code.claude.com/docs/en/skills)。打开 Claude Code，输入 `/educational-video`。

按需要自行选择 Opus；本 skill 不修改模型。其他支持 `SKILL.md` 的 agent 使用各自安装方式。不支持 skill 时，可复制[通用 prompt 底稿与一个案例](educational/educational-video/references/aws-cases.zh.md)；渲染仍需要工具。

## 使用

```text
/educational-video Create a 10-second preview explaining why the sky is blue.
/educational-video Create a 2-minute video about Amazon SQS.
/educational-video 中文 制作一个 3 分钟的 AWS Lambda 科普视频。
/educational-video --lang zh 只写一个 3 分半钟的 Amazon Bedrock 视频 prompt。
/educational-video Extend ./my-video to 3 minutes; preserve the opening and style.
/educational-video --lang en Create a 60-second vertical video about photosynthesis with narration.
```

以上是 prompt，不是 shell 命令。`--lang` 由模型理解，没有自定义参数解析器。

| 请求 | 模式 | 交付物 |
| --- | --- | --- |
| 样片 / preview | `preview` | 短 MP4、完整视频提纲、可编辑工程 |
| 制作视频 | `full` | 完整 MP4 与可复现工程 |
| 扩展已有视频 | `extend` | 保留可用风格/素材，增加解释深度 |
| 编写 prompt | `prompt-only` | 完整可复制 prompt，不安装、不渲染 |

新视频即使收到中文请求也默认英文。明确的输出语言要求优先：`中文` / `--lang zh` 选择中文；`English` / `--lang en` 选择英文。修改时沿用项目保存的语言，除非明确切换。语言控制工作流参考、字幕、可选旁白和面向人的交付说明；API 名和代码标识符不变。中文指令文件是同一 skill 的翻译，不是另一个命令。

默认成片 120 秒；样片是 30 秒提纲中的 10 秒；1080p/30 fps；米白/深色/橙色图示；短字幕；无旁白。用户要求和现有项目约定优先。只要样片就停在样片；完整制作不额外强制审批。

## 目录

```text
educational/educational-video/
  SKILL.md                         # 自动发现入口，默认英文
  SKILL.zh.md                      # 对应中文指令
  references/
    workflow.en.md / workflow.zh.md
    aws-cases.en.md / aws-cases.zh.md
docs/history.en.md / history.zh.md # 历史 prompt 与工具清单
evals/cases.json                   # 供 agent 执行的行为场景
scripts/validate.py                # 离线打包/链接/时间线检查
```

案例库重建了六个主题、八个版本：SQS 样片与扩展版、OpenSearch、DynamoDB、NLB、Bedrock 两个时长版本、Lambda。包含定时分镜、数据、边界、一手来源。这些是改写，不是逐字对话。[历史文档](docs/history.zh.md)区分讨论过的工具、实际使用与用户反馈。

## 验证与贡献

```sh
python3 scripts/validate.py
```

需要 Python 3.9+，无需第三方依赖。检查本地链接、独立打包、翻译配对、双语时间线与评估覆盖。它**不会**运行 Opus 或渲染视频，也不能证明模型遵守指令。见[行为评估说明](evals/README.zh.md)。仓库不含历史成片，本版尚未在 Opus 中完成端到端渲染测试。

新 skill 放在题材分类下，提供英文 `SKILL.md` 和中文 `SKILL.zh.md`。路由、限制、参考与用户文档保持等价，API 标识符不变。新增模式补充行为场景，运行时只加载相关参考。

## 为什么先做 skill？

可复用的是证据、讲解、时间分配、渲染与检查流程。Skill 直接调用已有工具。以后若需要共享渲染服务、素材库或渲染任务 API，再考虑 MCP；当前不需要额外服务器。

## 许可与致谢

保留原有 [MIT 许可证](LICENSE)。第三方引擎、字体、音乐和 skills 各自的许可不变，本仓库不捆绑它们。灵感与参考项目见[历史文档](docs/history.zh.md)。本项目与 Anthropic 或 AWS 没有隶属关系。
