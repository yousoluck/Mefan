---
name: project-infra-cache
description: Use when architect-stage0 needs to characterize the project's caching layer (Redis, Memcached, in-memory, or HTTP cache headers) - tier 1 for FE-I-002
---

# Cache Skill — Investigation Template

> Architect-stage0 uses this template to generate a `project-infra-cache` skill.
> Output must cite real `path/to/file:line` evidence from graphify queries; no template content may be copied verbatim.

## Investigation Points

| ID | Investigation Point | L | Difficulty | graphify query | bash fallback | Code Target |
|----|---------------------|---|------------|----------------|---------------|-------------|
| FE-I-002.CACHE-1 | Cache backend (Redis / Memcached / Caffeine / local Map / ETag) | L1 | M | `graphify query "cache redis memcached"` | `grep -rn "RedisTemplate\|Caffeine\|@Cacheable" src/ \| head` | src/cache/redis_client.py:1-30 |
| FE-I-002.CACHE-2 | TTL policy (fixed / sliding / no expiry) | L1 | M | `graphify query "TTL expiry timeout"` | `grep -rn "expire\|timeout\|TTL" src/ \| head` |  |
| FE-I-002.CACHE-3 | Cache key naming convention (e.g. `user:{id}`) | L1 | M | `graphify query "cache key prefix"` | `grep -rn "cache.put\|cache.set\|RedisTemplate.ops" src/ \| head` |  |
| FE-I-002.CACHE-4 | Invalidation strategy (write-through / write-behind / TTL-only) | L1 | H | `graphify query "cache invalidation write-through"` | `grep -rn "cache.evict\|cache.delete\|@CacheEvict" src/ \| head` |  |
| FE-I-002.CACHE-5 | Serialization format (JSON / Protobuf / JDK / MessagePack) | L1 | M | `graphify query "cache serializer JSON"` | `grep -rn "GenericJackson2JsonRedisSerializer\|serialize" src/ \| head` |  |
| FE-I-002.CACHE-6 | Distributed lock pattern (Redlock / SETNX / ZK / etcd) | L1 | H | `graphify query "distributed lock redlock"` | `grep -rn "RedissonClient\|setIfAbsent\|SETNX" src/ \| head` |  |
| FE-I-002.CACHE-7 | Cache stampede prevention (mutex / single-flight / probabilistic early expiry) | L1 | H | `graphify query "cache stampede"` | `grep -rn "stampede\|singleflight\|@Cacheable.sync" src/ \| head` |  |
| FE-I-002.CACHE-8 | Cache warming / preloading strategy | L1 | M | `graphify query "cache warm preload"` | `grep -rn "warmUp\|preload\|@PostConstruct" src/ \| head` |  |
| FE-I-002.CACHE-9 | Cache monitoring / hit-rate tracking | L1 | M | `graphify query "cache hit rate metric"` | `grep -rn "CacheMetrics\|hit_rate\|cache.stats" src/ \| head` |  |
| FE-I-002.CACHE-10 | Cache penetration / breakdown handling (null caching, bloom filter) | L1 | H | `graphify query "cache penetration null"` | `grep -rn "BloomFilter\|null.*cache\|Optional.empty" src/ \| head` | src/cache/redis_client.py:1-30 |
## Query Execution Rules

1. Tokens from graph.json or `.vocab.txt` only — never invent
2. Max 12 tokens per query
3. On failure, retry once with synonym, then bash

## Output Spec

`project-infra-cache/SKILL.md` must:
- Real YAML frontmatter (name + "Use when..." description)
- Sections shaped by the data, not by this 10-point table
- Every fact cited with `path/to/file:line`
- Missing data → `[需人工补充]`, never fabricate

## Iron Law

**NO SKILL WITHOUT EVIDENCE** — Each claim requires `path/to/file:line`.

## Red Flags

- Template's 10-point table reused verbatim
- Java/Redis-specific guidance appears in a Python/Go project
- "应该设置 TTL" without citing actual config
- Description starts with "缓存技能" instead of "Use when"
