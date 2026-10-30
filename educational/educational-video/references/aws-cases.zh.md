# AWS 案例库

以下是根据先前中文 prompt 重建的可复用版本，不是逐字对话记录，也不代表每条视频都已渲染。英文版为本次新增翻译。所有案例数据均为虚构。制作时重新核对链接文档和场景细节；产品范围会变化。本次于 2026-10-29 重新查看了各服务的入口文档。

## 通用 prompt 底稿

将底稿与下方一个案例一起复制给 Opus，或用 `/educational-video 中文` 加主题与时长。安装后的 skill 会补充详细工作流。

```text
请根据下方案例制作代码渲染的科普视频。
输出语言：中文。受众：具备基本软件知识、对主题好奇的初学者。
有现有项目风格时沿用；否则使用 1920×1080、30 fps、米白背景、深色文字、
橙色强调、有标签的几何图示、简短可读字幕、克制动效，不加旁白。
用一个具体例子解释目的、机制和一个有价值的限制。
用最新一手文档核实技术事实，记录来源、配置假设和示意数据。不要部署真实 AWS 资源。
先写定时分镜，再实现。复用现有渲染器；否则选择 Remotion，或确定性的
HTML/SVG + Playwright + ffmpeg。画面、字幕、音频和检查时间点共用时间线。
有条件时使用生成或有许可的音频；静音时说明。检查场景和转场帧、可用条件下的
时序/播放，以及输出媒体参数。
交付所要求的 MP4、可编辑源码、分镜、时间线、事实/素材来源、联系表、复现命令
和如实的 QA 报告。不能声称执行过实际上未做的渲染、播放或试听。
如果我只要求 prompt，返回完整 prompt，不渲染；如果只要求样片，交付样片后停止；
其他情况完成所要求的视频。
```

## 1. SQS：最初的 10 秒样片

**模式：** preview；规划 30 秒，只渲染 0–10 秒，然后等待用户明确要求的风格审核。**问题：** 为什么可以先接受生成报表的请求，稍后才完成报表？

| 秒数 | 画面与讲解 |
| --- | --- |
| 0–3 | 多个报表请求同时到达，直接处理开始繁忙。 |
| 3–6 | 应用把任务元数据发送到 SQS Standard 队列。 |
| 6–10 | 调用方看到“已接受”，但“报表已完成”仍未出现。 |
| 10–23 | 后续规划：worker 接收、处理，然后删除消息。 |
| 23–30 | 后续结论：队列缓冲工作，worker 容量是另一个问题。 |

跟踪同一个 job ID。画出 worker 轮询，不能画成 SQS 执行业务。处理成功后才删除消息。用户曾反馈此样片效果不错；本仓库不含该成片或源工程。

## 2. SQS：扩展为两分钟

**模式：** extend；目标 120 秒（历史 prompt 允许 115–125 秒）。有素材时保留已认可的开头。

| 秒数 | 画面与讲解 |
| --- | --- |
| 0–10 | 沿用“已接受不等于已完成”的开头。 |
| 10–25 | 区分 producer、queue、worker 的职责。 |
| 25–45 | 跟踪 SendMessage → ReceiveMessage → 处理 → DeleteMessage。 |
| 45–65 | 处理失败、消息未删除，visibility timeout 到期。 |
| 65–85 | 报表生成成功，但 worker 删除消息前崩溃；演示幂等处理重试。 |
| 85–100 | 积压增长，通过明确配置的 worker 扩容增加处理能力。 |
| 100–110 | 配置的 redrive policy 将反复接收仍失败的消息送入 DLQ。 |
| 110–120 | 总结解耦、缓冲和应用责任。 |

Standard 队列可能重复、乱序。接收不等于删除；暂时不可见不等于绝对防重复锁。DLQ 不会自动修复任务。不能保证业务效果恰好发生一次。

来源：[SQS 简介](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html)、[visibility timeout](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html)、[DLQ](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html)。

## 3. Amazon OpenSearch Service：两分钟

**模式：** full；目标 120 秒（历史范围 115–125 秒）。**问题：** 商店如何找到相关商品？采用 provisioned domain 场景，不混合 Serverless 的行为。

示例 JSON 文档：P101 “red running shoes”，价格 399，in_stock true；P102 “lightweight running shoes”，价格 699；P103 “waterproof hiking boots”，价格 499。查询 `running shoes` 使用 AND 语义，并限制 `price <= 500`。即使字幕是中文，商品标题仍用英文并明确 analyzer；中文分词需要单独说明。

| 秒数 | 画面与讲解 |
| --- | --- |
| 0–10 | 顾客输入搜索词。 |
| 10–25 | 配置的数据导入流程将 JSON 文档写入索引。 |
| 25–45 | 分析词项，展示简化倒排索引。 |
| 45–65 | 找到候选项，解释相关性排序。 |
| 65–85 | 应用价格限制，留下 P101。 |
| 85–105 | 源数据更新需要同步，并在 refresh 后才能被搜索到。 |
| 105–120 | 总结搜索机制与托管服务边界。 |

过滤与评分不同；讲解顺序不代表底层物理执行顺序。不要编造真实相关性分数，不要声称所有替代系统都逐条扫描。导入延迟和索引 refresh 是不同环节。

来源：[服务简介](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html)、[OpenSearch query DSL](https://docs.opensearch.org/latest/query-dsl/)、[refresh API](https://docs.opensearch.org/latest/api-reference/index-apis/refresh/)。

## 4. Amazon DynamoDB：两分钟

**模式：** full；120 秒。**问题：** 应用如何高效获取某位用户的订单？表名 `Orders`，示例键属性名为 `PK` 和 `SK`：

| PK | SK | orderId | status | total |
| --- | --- | --- | --- | --- |
| USER#042 | ORDER#2026-09-30#O100 | O100 | DELIVERED | 199 |
| USER#042 | ORDER#2026-10-10#O101 | O101 | SHIPPED | 399 |
| USER#042 | ORDER#2026-10-14#O102 | O102 | PENDING | 699 |
| USER#088 | ORDER#2026-10-14#O103 | O103 | SHIPPED | 249 |

| 秒数 | 画面与讲解 |
| --- | --- |
| 0–10 | 打开“我的订单”。 |
| 10–25 | 介绍 table、item、attribute。 |
| 25–45 | 解释复合主键，GetItem 需要两个键部分。 |
| 45–65 | Query 使用 `PK = USER#042`，SK 前缀为 `ORDER#2026-10`。 |
| 65–80 | 比较 Query 与 Scan；过滤发生在读取之后。 |
| 80–100 | Query 查询 GSI `orderIdIndex`；其分区键为 orderId，无排序键，投影 status/total。 |
| 100–110 | 区分托管基础设施与应用的键设计。 |
| 110–120 | 总结按访问模式设计数据。 |

固定 ISO 日期使示例中的字符串排序有意义。逻辑键分组不是专属物理服务器。GSI 使用 Query，不是 GetItem。GSI 读取为最终一致，索引本身不强制 orderId 唯一；示例假设应用负责唯一性。FilterExpression 不减少此次读取消耗的读取容量；需要时说明分页。不要暗示 DynamoDB 所有读取都只能最终一致。

来源：[核心组件](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.CoreComponents.html)、[Query](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Query.html)、[GSI](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html)。

## 5. Network Load Balancer：两分钟

**模式：** full；120 秒。**问题：** 多个设备如何连接同一个服务入口？场景：TCP 9000 端口，设备 C1/C2/C3；AZ-A 中 instance targets A1/A2，AZ-B 中 B1/B2；TCP 健康检查。初始关闭 cross-zone，target group 继承负载均衡器设置。

| 秒数 | 画面与讲解 |
| --- | --- |
| 0–10 | 一个服务入口，不代表只有一个 IP 地址。 |
| 10–28 | 介绍 listener、逻辑 target group、注册 targets。 |
| 28–50 | 一条 TCP 连接映射到一个 target，其数据包沿该连接传输。 |
| 50–75 | A1 失败、A2 仍健康；健康检测需要时间，新客户端连接可到达健康 target。 |
| 75–100 | 比较 cross-zone 关闭/开启对新连接的影响。 |
| 100–110 | DNS 解析入口，各 AZ 的负载均衡器地址处理流量。 |
| 110–120 | 总结连接路由和健康检查。 |

不要画成逐包/逐请求轮询、已建立连接迁移、即时故障发现，或 NLB 自动扩容 EC2 worker。说明选用的 unhealthy connection 行为；示例限定存在健康替代 target。使用“总是健康”前检查 fail-open 例外。TCP 健康不等于业务逻辑正确。DNS 不在持续数据传输路径中。

来源：[NLB 简介](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/introduction.html)、[健康检查](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/target-group-health-checks.html)、[target group 属性](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/edit-target-group-attributes.html)。

## 6. Amazon Bedrock：最初的两分钟方案

**模式：** full；120 秒。**问题：** 助手如何依据内部文档回答？后来因机制较复杂，扩展了讲解时长。

| 秒数 | 画面与讲解 |
| --- | --- |
| 0–10 | 询问生产环境日志保留时间。 |
| 10–28 | 区分应用、Bedrock API、基础模型。 |
| 28–40 | 模型不会自动知道私有文档。 |
| 40–60 | 在已配置的知识库中导入文档、建立索引。 |
| 60–80 | 检索相关段落。 |
| 80–100 | 将问题和段落发送给 Converse，应用展示引用。 |
| 100–110 | 介绍已配置的 Guardrails 及其限制。 |
| 110–120 | 总结检索加生成。 |

使用下面扩展方案相同的范围、数据和边界。

## 7. Amazon Bedrock：扩展为三分半钟

**模式：** full 或 extend；目标 210 秒（历史范围 200–210 秒）。虚构文档规定：测试日志保留 7 天，生产日志保留 30 天。部署回滚文档与此问题无关。

| 秒数 | 画面与讲解 |
| --- | --- |
| 0–15 | 提出需要内部证据才能回答的问题。 |
| 15–40 | 区分应用、平台和基础模型。 |
| 40–60 | 解释一次 Converse 请求/响应。 |
| 60–90 | 离线 S3 导入：文档分块、embedding、向量存储。 |
| 90–120 | 查询时 Retrieve 返回相关段落。 |
| 120–150 | 应用将段落交给 Converse，并把来源映射到界面。 |
| 150–175 | 改问备份保留时间；日志保留时间不能回答它，展示证据不足。 |
| 175–195 | 区分授权与已配置的 Guardrails。 |
| 195–210 | 总结有证据支撑的回答流程及其限制。 |

限定为一种由客户配置向量存储的知识库实现，不能代表当前 Bedrock 所有产品模式。采用 `Retrieve` 然后 `Converse`，不要又加入 `RetrieveAndGenerate` 重复推理。Embedding 模型与生成模型职责不同。RAG 不是训练。本流程的引用是应用显式实现的功能，不是 Converse 自动保证。Guardrails 不保证正确，也不代替授权。避免固定模型名、自动模型路由的泛化说法或真实 API 调用。

来源：[Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)、[Retrieve API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html)、[Converse API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html)、[Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)。

## 8. AWS Lambda：三分钟

**模式：** full；180 秒（历史范围 175–185 秒）。**问题：** 上传照片后是谁在运行代码？范围限定为默认按需执行模式的事件驱动函数。当前文档把原始事件驱动类型称为 Lambda Event Functions；不要把此例泛化到 Web Functions、MicroVMs 或其他执行模式。

输入为 input bucket 中不可变、名称唯一的 `image042.jpg`。配置的 ObjectCreated 通知异步调用 Lambda。Handler 从 S3 读取图片字节，缩放后写入另一个 output bucket 的 `thumbnails/image042.jpg`。

| 秒数 | 画面与讲解 |
| --- | --- |
| 0–15 | 上传已接受不等于缩略图已完成。 |
| 15–35 | 开发者提供代码与配置，AWS 管理基础设施。 |
| 35–60 | S3 事件元数据进入 Lambda 内部异步队列；handler 另外获取对象字节。 |
| 60–85 | 对比新执行环境初始化与可能发生的 warm reuse。 |
| 85–110 | 同一个函数定义的并发调用使用多个执行环境。 |
| 110–140 | 失败重试与重复投递引出输出的幂等处理。 |
| 140–165 | 区分允许 S3 调用函数的权限，与 execution role 读写 S3/日志的权限。 |
| 165–180 | 总结事件、执行、扩容与责任。 |

内部队列不是用户创建的 SQS。单环境一次调用仅限定此例的默认模式。复用不保证发生，也不是持久存储。扩容有边界，不同调用来源的重试不同。确定性的输出键只是不可变输入与固定处理条件下的示例；重复写仍可能产生版本和成本。不能承诺 exactly-once 或自动回滚。失败目的地需要配置；视频中的日志与事件均为模拟。

来源：[Lambda 简介](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)、[异步调用](https://docs.aws.amazon.com/lambda/latest/dg/invocation-async.html)、[执行环境](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtime-environment.html)、[S3 trigger](https://docs.aws.amazon.com/lambda/latest/dg/with-s3.html)。
