# 历史 prompt、工具与证据来源

本文区分先前对话与 2026-10-29 创建的通用 skill。案例库是重建整理，不是逐字对话存档。本包没有复制第三方 skill 代码或原始社交媒体长 prompt。

## Prompt 逐步形成的共性

我们从 10 秒风格试片开始，发展到两分钟服务讲解；机制复杂时再增加时长。稳定下来的形式是：一个实际问题、一个贯穿例子、表达因果的图示、简短字幕、统一风格，以及明确的技术边界。

| Prompt 版本 | 时长 | 主要新增内容 |
| --- | --- | --- |
| SQS 样片 | 渲染 10 秒，规划 30 秒 | 验证风格；已接受不等于已完成 |
| SQS 扩展 | 约 120 秒 | 生命周期、不可见期、重复、容量、DLQ |
| OpenSearch | 约 120 秒 | 文档 → 词项 → 候选 → 过滤 → 更新可见性 |
| DynamoDB | 约 120 秒 | 访问模式、复合键、Query/Scan、GSI |
| NLB | 约 120 秒 | 连接路由、健康检测延迟、跨 AZ 范围 |
| Bedrock 初版 | 约 120 秒 | 应用、模型、检索、生成 |
| Bedrock 扩展 | 约 210 秒 | 分开导入与查询；证据不足与授权 |
| Lambda | 约 180 秒 | 事件、执行环境、重试、两类权限边界 |

[英文案例库](../educational/educational-video/references/aws-cases.en.md)和[中文案例库](../educational/educational-video/references/aws-cases.zh.md)保留关键分镜、示例数据与边界。历史 prompt 使用中文，英文是本次新增改写。旧时长范围作为历史记录保留，通用流程则明确目标时长与误差。

## 两条帖子的启发

- [laobaishare：仓库合集](https://x.com/laobaishare/status/2108533494725103926)：提供设计 skills、渲染引擎和动画库的工具地图。它由多位维护者的项目组成，不是单一产品。
- [Tom CC：制作经验](https://x.com/Tom_CC_9986/status/2108512799517450287)：复用风格、用问题吸引观众、先做短样片、同步字幕/动效/音乐、核对事实。纸墨风格和特定配乐的第 17 秒节点属于原案例，不是通用工作流要求。

先前研究记录注明：2026-10-10 阅读了帖子正文和选定仓库；没有观看嵌入视频，也没有独立核实流量或收入。Skill 不承诺传播效果或模型优势。第三条关于多模型团队的帖子不属于视频制作包，因此没有加入团队编排依赖。

## 参考过的引擎和 skills

以下在研究中查看过文档，没有在那次研究中安装或运行：

| 项目 | 吸收的思路 |
| --- | --- |
| [claude-motion](https://github.com/whaleyxbt/claude-motion) | 共享时间线协调场景、声音、审阅；contact sheet 按节点抽样 |
| [claude-motion-design](https://github.com/howseen-ai/claude-motion-design) | HTML/Playwright/ffmpeg、确定性 seek(t)、迭代视觉检查 |
| [HyperFrames](https://github.com/heygen-com/hyperframes) | 通过浏览器工具把 HTML/CSS 动画渲染成视频 |
| [Remotion](https://github.com/remotion-dev/remotion) | React 与按帧驱动的视频制作 |
| [Remotion skills](https://github.com/remotion-dev/skills) | 选择 Remotion 后再加载对应引擎指导 |

为完整记录，下面列出原合集的其他链接。列出不代表推荐、当前可用性核实、安装或兼容性测试：

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

## 实际使用情况

- 先前研究使用了本地 `research` 工作流、网页/浏览器检查与研究辅助 agent。这些用于收集来源，不是视频渲染依赖。
- 先前 prompt 编写使用了 `writing-for-agents` 指导。本包使用 `skill-creator` 与 `writing-for-agents` 编写。安装者不需要额外安装这些写作辅助 skill。
- 用户曾反馈 SQS 的 10 秒样片效果不错。样片在本仓库之外制作，仓库没有其源码、渲染命令或媒体文件；不能据此声称后续每一期均已成功制作。
- 本仓库新增的是中英文 `educational-video` skill。可在本地验证打包；实际 Opus 行为和端到端视频质量需另行评估。

## 提炼成通用能力的部分

保留工作流而非偶然细节：事实依据、场景范围、定时分镜、确定性渲染、可读性、扩展时增加讲解深度、可复现交付，以及如实记录验证状态。配色、比例、时长、音频和语言默认值均可覆盖。AWS 专属语义放入可选案例参考，不混入核心 skill。

先交付 skill，因为当前需要复用的是模型指令和工作流知识。未来确实需要远程渲染、素材管理或任务控制能力时，再通过 MCP 暴露这些工具。
