# Few-Shot Examples

These examples calibrate your output quality and style.

---

## ❌ BAD Example: Document Generator Output

This is what a "summarizer" produces. It fails the 6-Month Rule.

```markdown
# Today's Chat About RPC

We discussed how to write a raw HTTP server using Node.js net module. The user wrote some code and ran into a port collision error (EADDRINUSE), so we changed the port from 8080 to 8081. Then we discussed how data events emit Buffer objects instead of strings by default, which can be fixed by calling .toString(). Finally we decided to build a simple RPC demo next.
```

**Why it's bad:**
- Chronological diary, not knowledge
- Port errors and `.toString()` are ephemeral noise
- "We decided to build RPC next" is a planning statement with zero future value
- Fails the 6-Month Rule: useless without today's context

---

## ✅ GOOD Example 1: Decision / Solution (Template A)

```markdown
# Redis as Session Store: TTL-Native Storage for Ephemeral Auth State

## Context
A web application requires server-side session management with strict expiration semantics and sub-millisecond read latency under high concurrency.

## Problem
Relational databases (PostgreSQL, MySQL) require manual expiration logic (cron jobs or application-level TTL checks), adding operational complexity and risking stale session leaks under load.

## Solution / Decision
Use Redis as the session store with native key-level TTL (`EXPIRE` / `SET EX`).

## Why (Trade-offs & Rationale)
- **Pro**: TTL is a first-class primitive — no cron, no GC, no stale data. O(1) read/write.
- **Pro**: Built-in eviction policies (`volatile-lru`) handle memory pressure gracefully.
- **Con**: Data is in-memory; requires persistence config (`RDB`/`AOF`) or acceptance of data loss on crash.
- **Con**: Adds an infrastructure dependency vs. reusing the existing RDBMS.

## Lessons Learned
- When your data has a natural expiration semantic, choose a store where TTL is a native primitive, not a bolted-on feature.
- "Reuse the existing database" is not always simpler — sometimes it imports more complexity than a purpose-built tool.
```

---

## ✅ GOOD Example 2: Mental Model (Template B)

```markdown
# TCP is Bytes, HTTP is Messages, RPC is Function Calls

## One-Liner
Network protocols form an abstraction ladder: TCP delivers raw bytes, HTTP imposes request/response message structure, and RPC masks the network entirely behind a function call interface.

## Explanation
TCP (`net.Socket`) provides a reliable, ordered byte stream with no concept of "message boundaries." When you listen to `socket.on('data')`, each event delivers an arbitrary chunk of bytes — it may be half a JSON object, or three concatenated requests. There is no guarantee that one `data` event equals one logical message.

HTTP builds on TCP by defining explicit message boundaries: a header section terminated by `\r\n\r\n`, a `Content-Length` or `Transfer-Encoding` field to delimit the body, and a strict request/response pairing. This is why `http.createServer()` can hand you a clean `req` object — it has already solved the framing problem.

RPC goes one step further: it hides the entire network interaction behind what looks like a local function call. The caller writes `result = await remoteAdd(1, 2)` without knowing that serialization, transport, deserialization, and error mapping happened underneath. The "abstraction seam" is the function signature itself.

## When to Apply
- When debugging "partial data" issues in TCP servers — you're fighting the byte-stream nature of TCP.
- When designing application protocols — consciously decide which layer of the abstraction ladder you're building at.
- When evaluating RPC frameworks (gRPC, tRPC, JSON-RPC) — understand that they are all solving the same framing + serialization + call-semantics problem, just with different trade-offs.

## Lessons Learned
- Never assume a single `data` event on a TCP socket contains a complete application message.
- Understanding the abstraction ladder prevents you from accidentally reimplementing a lower layer's responsibilities.
```

---

## ✅ GOOD Example 3: Anti-Pattern (Template C)

```markdown
# Polling Anti-Pattern: Why Busy-Wait Loops Fail for IPC Synchronization

## Context
Two processes need to synchronize state — Process A produces data, Process B consumes it. A simple approach is to have Process B poll a shared resource (file, database row, shared memory flag) in a tight loop.

## What Was Tried
Process B runs a `while (true)` loop with a short `sleep(100ms)`, checking a shared flag or file for changes on every iteration.

## Why It Failed
- **CPU waste**: Even with sleep intervals, the polling loop consumes CPU cycles proportional to the poll frequency, not the event frequency. At 10ms intervals, that's 100 syscalls/second doing nothing.
- **Latency-throughput tradeoff**: Increasing sleep reduces CPU waste but adds latency. There is no interval that optimizes both.
- **Scalability collapse**: With N consumers polling, resource contention grows linearly. The shared resource becomes a bottleneck.

## Better Alternative
Use event-driven IPC mechanisms: OS-level signals, named pipes, message queues (`child_process.send()` in Node.js), or pub/sub systems. The consumer blocks (zero CPU) until the producer explicitly pushes a notification.

## Lessons Learned
- If you find yourself writing `while + sleep + check`, you are almost certainly reimplementing a notification system poorly.
- The correct primitive is "block until notified", not "check repeatedly."
```
