# AWS case library

These are reusable reconstructions of the earlier Chinese prompts, not verbatim transcripts or proof that every video was rendered. English is a new translation. All data below is fictional. Recheck the linked documentation and scenario-specific details when making a video; product scope changes over time. Opening docs were revisited on 2026-10-29.

## Common prompt base

Paste this base together with one case below into Opus, or invoke `/educational-video` with the case's topic and duration. The installed skill adds the detailed workflow.

```text
Create a code-rendered educational video using the case specification below.
Output language: English. Audience: curious beginners with basic software knowledge.
Preserve the project's established style if available; otherwise use 1920×1080,
30 fps, off-white background, dark text, orange emphasis, labeled geometric
diagrams, short readable captions, restrained motion, and no narration.
Use a single concrete example to explain purpose, mechanism, and a useful limitation.
Verify technical claims against current primary documentation. Record sources,
configuration assumptions, and illustrative data. Do not deploy real AWS resources.
Write a timed storyboard before implementation. Reuse the current renderer;
otherwise choose Remotion or deterministic HTML/SVG + Playwright + ffmpeg.
Use one timeline for visuals, captions, audio, and review timestamps. Generate or
use licensed audio if available; report if silent. Inspect scene and transition
frames, check timing/playback where available, and verify output metadata.
Deliver the requested MP4, editable sources, storyboard, timeline, source/asset
ledger, contact sheet, reproduction commands, and an honest QA report.
Do not claim an unperformed render, playback, or listening check. If I request
only a prompt, return a self-contained prompt without rendering. If I request
only a preview, stop after that preview. Otherwise complete the requested video.
```

## 1. SQS: first 10-second preview

**Mode:** preview; plan 30 seconds, render only 0–10 seconds, then wait for the explicitly requested style review. **Question:** why accept a report request before the report is ready?

| Seconds | Visual teaching beat |
| --- | --- |
| 0–3 | Several report requests arrive; direct processing becomes busy. |
| 3–6 | The application sends job metadata to an SQS Standard queue. |
| 6–10 | “Accepted” appears to the caller; “report ready” remains pending. |
| 10–23 | Planned continuation: a worker receives, processes, and deletes the message. |
| 23–30 | Planned takeaway: a queue buffers work; worker capacity is separate. |

Follow a single job ID. Show the worker polling, not SQS executing the job. Delete only after successful processing. The user reported liking this preview; the render and source project are not included in this repository.

## 2. SQS: extend to two minutes

**Mode:** extend; target 120 seconds (historical prompt allowed 115–125). Preserve the approved opening if the assets are available.

| Seconds | Visual teaching beat |
| --- | --- |
| 0–10 | Reuse the accepted-versus-completed hook. |
| 10–25 | Separate producer, queue, and worker responsibilities. |
| 25–45 | Trace SendMessage → ReceiveMessage → processing → DeleteMessage. |
| 45–65 | A failure leaves a message undeleted; visibility timeout expires. |
| 65–85 | Report creation succeeds but the worker crashes before deletion; demonstrate idempotent handling of a retry. |
| 85–100 | Backlog grows; explicitly configured worker scaling adds capacity. |
| 100–110 | A configured redrive policy moves repeatedly received failures to a DLQ. |
| 110–120 | Recap decoupling, buffering, and application responsibility. |

Standard queues can duplicate and reorder messages. Receiving is not deleting; invisibility is not an absolute duplicate-prevention lock. A DLQ does not repair failed jobs. Do not claim exactly-once business effects.

Sources: [SQS introduction](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html), [visibility timeout](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html), [DLQs](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html).

## 3. Amazon OpenSearch Service: two minutes

**Mode:** full; target 120 seconds (historical range 115–125). **Question:** how does a store find relevant products? Use a provisioned domain scenario, not a blend of provisioned and Serverless behavior.

Example JSON documents: P101 “red running shoes”, price 399, in_stock true; P102 “lightweight running shoes”, price 699; P103 “waterproof hiking boots”, price 499. Query `running shoes` with AND semantics and `price <= 500`. Use English product titles with an explicitly selected analyzer even in a Chinese video; Chinese tokenization requires its own explanation.

| Seconds | Visual teaching beat |
| --- | --- |
| 0–10 | A shopper types the query. |
| 10–25 | A configured ingestion process indexes JSON documents. |
| 25–45 | Analyze terms and show a simplified inverted index. |
| 45–65 | Find candidates and explain relevance ranking. |
| 65–85 | Apply the price constraint; P101 remains. |
| 85–105 | A source update must be synchronized, then become searchable after refresh. |
| 105–120 | Summarize search mechanisms and the managed-service boundary. |

Filtering and scoring are different operations; their explanatory order is not a claim about physical execution order. Avoid fabricated real relevance scores or claims that all competing systems scan every record. Ingestion delay and index refresh are distinct.

Sources: [service overview](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html), [OpenSearch query DSL](https://docs.opensearch.org/latest/query-dsl/), [refresh API](https://docs.opensearch.org/latest/api-reference/index-apis/refresh/).

## 4. Amazon DynamoDB: two minutes

**Mode:** full; 120 seconds. **Question:** how can an application fetch one user's orders efficiently? Table `Orders`, example attribute names `PK` and `SK`:

| PK | SK | orderId | status | total |
| --- | --- | --- | --- | --- |
| USER#042 | ORDER#2026-09-30#O100 | O100 | DELIVERED | 199 |
| USER#042 | ORDER#2026-10-10#O101 | O101 | SHIPPED | 399 |
| USER#042 | ORDER#2026-10-14#O102 | O102 | PENDING | 699 |
| USER#088 | ORDER#2026-10-14#O103 | O103 | SHIPPED | 249 |

| Seconds | Visual teaching beat |
| --- | --- |
| 0–10 | Open “My orders”. |
| 10–25 | Introduce table, item, and attribute. |
| 25–45 | Explain the composite primary key and GetItem with both components. |
| 45–65 | Query `PK = USER#042` and SK prefix `ORDER#2026-10`. |
| 65–80 | Contrast Query and Scan; filtering happens after reading. |
| 80–100 | Query `orderIdIndex`, a GSI with partition key orderId, no sort key, and projected status/total. |
| 100–110 | Separate managed infrastructure from application key design. |
| 110–120 | Recap designing around access patterns. |

Fixed ISO dates make the illustrated string order meaningful. A logical key group is not a dedicated physical server. Query the GSI; do not call GetItem on it. GSI reads are eventually consistent; the index does not enforce orderId uniqueness. Assume the application enforces it in this example. FilterExpression does not reduce read capacity consumed by the read; mention pagination when needed. Do not imply all DynamoDB reads are necessarily eventual.

Sources: [core components](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.CoreComponents.html), [Query](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Query.html), [GSIs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html).

## 5. Network Load Balancer: two minutes

**Mode:** full; 120 seconds. **Question:** how do many devices connect to one service endpoint? Scenario: TCP port 9000; devices C1/C2/C3; instance targets A1/A2 in AZ-A and B1/B2 in AZ-B; TCP health checks. Cross-zone balancing starts disabled with the target group inheriting the load balancer setting.

| Seconds | Visual teaching beat |
| --- | --- |
| 0–10 | Present one service entry point, not a promise of one IP address. |
| 10–28 | Introduce listener, logical target group, and registered targets. |
| 28–50 | A TCP connection maps to one target; its packets stay on that connection. |
| 50–75 | A1 fails while A2 remains healthy; health detection takes time, then a new client connection can reach a healthy target. |
| 75–100 | Compare cross-zone off/on for new connections. |
| 100–110 | DNS resolves the endpoint; per-AZ load balancer addresses handle traffic. |
| 110–120 | Recap connection routing and health checks. |

Do not show round-robin per packet/request, migration of an established connection, instant health detection, or NLB automatically adding EC2 workers. State the chosen unhealthy-connection behavior; scope the example to healthy alternatives being available. Check fail-open exceptions before using “always healthy”. TCP health success does not prove application correctness. DNS is outside the ongoing data path.

Sources: [NLB introduction](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/introduction.html), [health checks](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/target-group-health-checks.html), [target group attributes](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/edit-target-group-attributes.html).

## 6. Amazon Bedrock: original two-minute plan

**Mode:** full; 120 seconds. **Question:** how can an assistant answer using internal documentation? This was later expanded because the mechanism needed more explanation time.

| Seconds | Visual teaching beat |
| --- | --- |
| 0–10 | Ask about production log retention. |
| 10–28 | Distinguish application, Bedrock APIs, and foundation model. |
| 28–40 | The model does not automatically know private documents. |
| 40–60 | Ingest and index documents in a configured knowledge base. |
| 60–80 | Retrieve relevant passages. |
| 80–100 | Send question and passages through Converse; application presents citations. |
| 100–110 | Introduce configured Guardrails and their limits. |
| 110–120 | Recap retrieval plus generation. |

Use the scope, data, and caveats of the expanded plan below.

## 7. Amazon Bedrock: expanded three-and-a-half-minute plan

**Mode:** full or extend; target 210 seconds (historical range 200–210). Fictional document: test logs retained 7 days; production logs 30 days. A rollback document is irrelevant to this query.

| Seconds | Visual teaching beat |
| --- | --- |
| 0–15 | Ask a question the application must ground in internal evidence. |
| 15–40 | Separate application, platform, and foundation model. |
| 40–60 | Explain a Converse request/response. |
| 60–90 | Offline S3 ingestion: chunk documents, embed, store vectors. |
| 90–120 | Query-time Retrieve returns relevant passages. |
| 120–150 | The app supplies passages to Converse and maps sources into its UI. |
| 150–175 | Ask about backup retention; log retention does not answer it. Show insufficient evidence. |
| 175–195 | Separate authorization from configured Guardrails. |
| 195–210 | Recap the grounded-answer pipeline and its limits. |

Scope this to one customer-configured vector-store knowledge base implementation; do not claim it describes every current Bedrock offering. Choose `Retrieve` followed by `Converse`; do not also insert `RetrieveAndGenerate` and duplicate inference. Embedding and generation models have different jobs. RAG is not training. Citations in this flow are an explicit application feature, not an automatic Converse guarantee. Guardrails do not ensure correctness or replace authorization. Avoid fixed model names, automatic model routing claims, or live API calls.

Sources: [Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html), [Retrieve API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Retrieve.html), [Converse API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html), [Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html).

## 8. AWS Lambda: three minutes

**Mode:** full; 180 seconds (historical range 175–185). **Question:** what runs after a photo upload? Scope: event-driven functions with the default on-demand execution model. Current docs call the original event-driven primitive Lambda Event Functions; do not generalize this scenario to Web Functions, MicroVMs, or other execution modes.

Input: immutable, uniquely named `image042.jpg` in an input bucket. A configured ObjectCreated notification invokes Lambda asynchronously. The handler reads bytes from S3, resizes, and writes `thumbnails/image042.jpg` to a separate output bucket.

| Seconds | Visual teaching beat |
| --- | --- |
| 0–15 | Upload accepted is not thumbnail completed. |
| 15–35 | The developer supplies code/configuration; AWS manages infrastructure. |
| 35–60 | S3 event metadata enters Lambda's internal asynchronous queue; the handler fetches the object bytes. |
| 60–85 | Contrast new-environment initialization and possible warm reuse. |
| 85–110 | Concurrent invocations use multiple execution environments for the same function definition. |
| 110–140 | Failure/retry and duplicate delivery motivate idempotent output handling. |
| 140–165 | Separate S3 invoke permission from the function execution role's S3/log permissions. |
| 165–180 | Recap event, execution, scaling, and responsibility. |

The internal queue is not an SQS queue the user provisioned. Scope one invocation per environment to the illustrated default model. Reuse is not guaranteed or durable storage. Scaling is bounded, and retry behavior depends on the invocation source. A deterministic output key is an illustration under immutable input and fixed processing; repeated writes may still create versions/costs. Do not promise exactly-once effects or automatic rollback. Failure destinations must be configured; all logs and events in the video are simulated.

Sources: [Lambda overview](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html), [asynchronous invocation](https://docs.aws.amazon.com/lambda/latest/dg/invocation-async.html), [execution environment](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtime-environment.html), [S3 trigger](https://docs.aws.amazon.com/lambda/latest/dg/with-s3.html).
