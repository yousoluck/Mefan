---
name: project-infra-message-queue
description: Use when architect-stage0 needs to characterize the project's message queue usage (Kafka, RabbitMQ, Redis Streams, Pulsar, etc.) - tier 1 for FE-I-005
---

# Message Queue Skill — Investigation Template

> Architect-stage0 uses this template to generate a `project-infra-message-queue` skill.
> Output must cite real `path/to/file:line` evidence; no template content may be copied.

## Investigation Points

| ID | Investigation Point | L | Difficulty | graphify query | bash fallback | Code Target |
|----|---------------------|---|------------|----------------|---------------|-------------|
| FE-I-005.MQ-1 | MQ broker type (Kafka / RabbitMQ / RocketMQ / Redis Streams / NATS) | L1 | M | `graphify query "kafka rabbitmq redis streams"` | `grep -rn "KafkaTemplate\|RabbitTemplate\|@KafkaListener" src/ \| head` |  |
| FE-I-005.MQ-2 | Producer configuration (acks / idempotence / batch size) | L1 | M | `graphify query "producer acks batch"` | `grep -rn "acks=\|enable.idempotence\|batch.size" src/ \| head` |  |
| FE-I-005.MQ-3 | Consumer group / subscription pattern | L1 | M | `graphify query "consumer group subscribe"` | `grep -rn "groupId\|@RabbitListener\|consumerGroup" src/ \| head` |  |
| FE-I-005.MQ-4 | Acknowledgment mode (auto / manual / batch) | L1 | M | `graphify query "acknowledge manual"` | `grep -rn "AckMode\|acknowledge\|MANUAL" src/ \| head` |  |
| FE-I-005.MQ-5 | Dead letter queue / poison message handling | L1 | H | `graphify query "dead letter queue"` | `grep -rn "deadLetter\|DLQ\|x-dead-letter" src/ \| head` |  |
| FE-I-005.MQ-6 | Idempotency / exactly-once semantics | L1 | H | `graphify query "idempotent exactly once"` | `grep -rn "idempotent\|@TransactionalEventListener\|deduplication" src/ \| head` |  |
| FE-I-005.MQ-7 | Schema / payload format (Avro / Protobuf / JSON) | L1 | M | `graphify query "schema registry payload"` | `grep -rn "schemaRegistry\|Avro\|Protobuf" src/ \| head` |  |
| FE-I-005.MQ-8 | Transactional message (send + DB) | L1 | H | `graphify query "transactional message"` | `grep -rn "transactional\|@KafkaTransaction\|ChannelTransaction" src/ \| head` |  |
| FE-I-005.MQ-9 | Backpressure / rate limiting on consumer | L1 | M | `graphify query "backpressure rate limit"` | `grep -rn "maxPollRecords\|prefetch\|concurrency" src/ \| head` |  |
| FE-I-005.MQ-10 | Tracing / observability (OpenTelemetry integration) | L1 | M | `graphify query "trace producer consumer"` | `grep -rn "OpenTelemetry\|@Observed\|tracer" src/ \| head` |  |
## Query Execution Rules

1. Tokens from graph.json or `.vocab.txt` only
2. Max 12 tokens per query
3. On failure, retry once with synonym, then bash

## Output Spec

`project-infra-message-queue/SKILL.md` must:
- Real YAML frontmatter
- Sections shaped by data, not by this 10-point table
- Every fact cited with `path/to/file:line`
- Missing data → `[需人工补充]`

## Iron Law

**NO SKILL WITHOUT EVIDENCE** — Each claim requires `path/to/file:line`.

## Red Flags

- Reuses this template's table verbatim
- Kafka-specific guidance for a RabbitMQ project
- Says "应该设置 acks=all" without citing actual config
- Description starts with "消息队列" instead of "Use when"
