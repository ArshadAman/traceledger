# TraceLedger — Distributed Audit Logging & Processing System

TraceLedger is a backend system designed to capture, process, and search audit events in a scalable and fault-tolerant manner. It follows an event-driven architecture to decouple API requests from background processing, improving performance, reliability, and extensibility.

---

## 🚀 Features

- Event-driven architecture using RabbitMQ (decoupling write path from processing)
- Asynchronous background processing with workers (non-blocking API layer)
- Retry mechanisms and Dead Letter Queues (DLQ) for failure handling
- Idempotent event processing to prevent duplicate writes
- Redis caching for performance optimization (cache-aside pattern)
- API rate limiting for abuse protection (request-level control)
- Full-text search on audit logs using Elasticsearch (inverted index)
- Graceful degradation when dependent services fail

---

## 🏗️ System Architecture

Client → FastAPI → RabbitMQ → Worker → PostgreSQL  
                                        ↘ Elasticsearch  

---

## 🔄 Flow

1. Client sends request to FastAPI (entry point)
2. API publishes event to RabbitMQ (fire-and-forget pattern)
3. Worker consumes event asynchronously (consumer model)
4. Data is stored in PostgreSQL (source of truth)
5. Data is indexed into Elasticsearch (read optimization)
6. Redis is used for caching and rate limiting (hot path optimization)

---

## ⚙️ Tech Stack

| Layer            | Technology      |
|------------------|----------------|
| Backend API      | FastAPI        |
| Database         | PostgreSQL     |
| Cache            | Redis          |
| Messaging Queue  | RabbitMQ       |
| Search Engine    | Elasticsearch  |
| Language         | Python         |

---

## 📦 Core Components

### API Layer (FastAPI)

- Handles incoming requests (request lifecycle)
- Validates input and schema
- Publishes events to RabbitMQ instead of direct DB writes
- Applies rate limiting and caching where required

👉 Purpose: keep API fast and stateless

---

### Messaging Layer (RabbitMQ)

- Decouples API from processing (producer-consumer model)
- Uses fanout exchange for broadcasting events
- Ensures durability using persistent messages
- Supports retry queues and DLQ

👉 Key idea: at-least-once delivery

---

### Worker System

- Consumes messages from queue
- Processes audit events (business logic execution)
- Writes to PostgreSQL
- Indexes into Elasticsearch
- Handles retries and failures

👉 Important: must be idempotent

---

### Database (PostgreSQL)

- Stores structured audit logs (primary storage)
- Uses UUID for uniqueness
- Enforces constraints for data integrity

👉 Source of truth

---

### Caching Layer (Redis)

- Implements cache-aside strategy:
  - check cache → fallback to DB → update cache
- Used for:
  - read optimization
  - rate limiting counters

👉 Reduces DB pressure

---

### Search Layer (Elasticsearch)

- Stores denormalized indexed data
- Enables full-text search using inverted index
- Supports filtering and querying

👉 Optimized for reads, not writes

---

## 🔁 Fault Tolerance Mechanisms

### Circuit Breaker

- Prevents repeated calls to failing services
- Opens circuit after failure threshold
- Returns fallback response instead of retrying continuously

👉 Avoids cascading failures

---

### Dead Letter Queue (DLQ)

- Messages exceeding retry limit go to DLQ
- Used for debugging and inspection

👉 Prevents infinite retry loops

---

### Idempotent Consumers

- Ensures same message processed multiple times does not create duplicates
- Typically handled using unique constraints or checks

👉 Required because of at-least-once delivery

---

### Graceful Degradation

- Redis down → fallback to DB
- Elasticsearch down → search disabled, core system works
- RabbitMQ down → system avoids crash, logs failure

👉 System should degrade, not fail

---

## ⚡ Performance Optimizations

- Async processing reduces API latency
- Redis caching reduces repeated DB reads
- Rate limiting prevents overload
- Background workers handle heavy operations

👉 Move heavy work off request path

---

## 🔐 Security

- Input validation at API layer
- Controlled access patterns
- Rate limiting to prevent abuse

---

## 📊 Example Use Cases

- Audit logging systems
- User activity tracking
- Debugging and monitoring
- Compliance systems

---

## 🛠️ Local Setup

### Start Services

    brew services start postgresql
    brew services start redis
    brew services start rabbitmq
    brew services start elasticsearch-full

### Run API

    uvicorn app.main:app --reload

### Run Worker

    python worker/main.py

---

## 📌 API Endpoints

| Endpoint                  | Description         |
|--------------------------|---------------------|
| POST /users              | Create user         |
| POST /auth/login         | Login user          |
| GET /audit-events        | List audit logs     |
| GET /audit-events/search | Search audit logs   |

---

## 🧠 Concepts Implemented

- REST API Design (request-response lifecycle)
- Event-Driven Architecture (decoupling)
- Message Queues (RabbitMQ internals: exchange, queue, binding)
- Retry Mechanisms (TTL + DLX)
- Dead Letter Queues
- Idempotency (duplicate safety)
- Caching (Redis, cache-aside)
- Rate Limiting (token/bucket logic)
- Full-Text Search (Elasticsearch basics)
- Fault Tolerance
- Graceful Degradation

---

## 📈 Future Improvements

- Monitoring & observability (metrics, logging, tracing)
- Docker & Kubernetes deployment
- CI/CD pipeline

---

## 👨‍💻 Author

Arshad Aman  
Backend Engineer | Python  
