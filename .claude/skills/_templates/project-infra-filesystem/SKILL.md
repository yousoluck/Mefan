---
name: project-infra-filesystem
description: Use when architect-stage0 needs to characterize how the project reads, writes, and manages files on local or remote storage - tier 1 for FE-I-003
---

# Filesystem Skill — Investigation Template

> Architect-stage0 uses this template to generate a `project-infra-filesystem` skill.
> Output must cite real `path/to/file:line` evidence; no template content may be copied.

## Investigation Points

| ID | Investigation Point | L | Difficulty | graphify query | bash fallback | Code Target |
|----|---------------------|---|------------|----------------|---------------|-------------|
| FE-I-003.FS-1 | Storage backend (local disk / S3 / OSS / NFS / in-memory) | L1 | M | `graphify query "storage backend S3"` | `grep -rn "S3Client\|MinioClient\|FileSystem\|fs.open" src/ \| head` |  |
| FE-I-003.FS-2 | File path safety (absolute vs relative, path traversal defense) | L1 | M | `graphify query "path traversal sanitize"` | `grep -rn "Path.resolve\|sanitize\|normalize" src/ \| head` |  |
| FE-I-003.FS-3 | Streaming vs full-read for large files | L1 | M | `graphify query "streaming read write"` | `grep -rn "InputStream\|stream()\|readable" src/ \| head` |  |
| FE-I-003.FS-4 | Concurrent access / file locking | L1 | H | `graphify query "file lock concurrent"` | `grep -rn "FileChannel\|flock\|tryLock" src/ \| head` |  |
| FE-I-003.FS-5 | Compression / encoding (gzip / snappy / base64) | L1 | M | `graphify query "compression gzip"` | `grep -rn "GZIPInputStream\|compress\|gzip" src/ \| head` |  |
| FE-I-003.FS-6 | Upload flow (multipart / presigned URL / streaming PUT) | L1 | H | `graphify query "upload presigned multipart"` | `grep -rn "presigned\|multipart\|InitiateMultipartUpload" src/ \| head` |  |
| FE-I-003.FS-7 | Download flow (signed URL / streaming GET) | L1 | M | `graphify query "download signed URL"` | `grep -rn "getObject\|download\|signedUrl" src/ \| head` |  |
| FE-I-003.FS-8 | Encryption at rest (server-side / client-side / KMS) | L1 | H | `graphify query "encryption at rest"` | `grep -rn "ServerSideEncryption\|KMS\|encrypt" src/ \| head` |  |
| FE-I-003.FS-9 | Atomic rename / temp file pattern | L1 | M | `graphify query "atomic rename temp file"` | `grep -rn "renameTo\|atomicMove\|os.replace" src/ \| head` |  |
| FE-I-003.FS-10 | Thread pool / async executor for IO operations | L1 | M | `graphify query "thread pool async IO"` | `grep -rn "ExecutorService\|@Async\|CompletableFuture" src/ \| head` |  |
## Query Execution Rules

1. Tokens from graph.json or `.vocab.txt` only
2. Max 12 tokens per query
3. On failure, retry once with synonym, then bash

## Output Spec

`project-infra-filesystem/SKILL.md` must:
- Real YAML frontmatter
- Sections shaped by data, not by this 10-point table
- Every fact cited with `path/to/file:line`
- Missing data → `[需人工补充]`

## Iron Law

**NO SKILL WITHOUT EVIDENCE** — Each claim requires `path/to/file:line`.

## Red Flags

- Reuses this template's table verbatim
- Hardcodes `java.nio.file.*` guidance for a non-Java project
- Says "应该使用 path.resolve" without citing the actual call
- Description starts with "文件系统操作" instead of "Use when"
