# SupportOps Agent 后端 API 文档

## 1. 文档说明

本文档用于描述 `SupportOps Agent：企业知识库驱动的智能客服与工单处理系统` 的后端 API 设计。

后端推荐使用：

- Python
- FastAPI
- SQLite / PostgreSQL
- FAISS / Chroma
- OpenAI API 或其他大模型 API

默认后端地址：

```text
http://127.0.0.1:8000
```

默认 API 前缀：

```text
/api
```

## 2. 通用约定

### 2.1 请求格式

除文件上传接口外，所有接口默认使用：

```http
Content-Type: application/json
```

文件上传接口使用：

```http
Content-Type: multipart/form-data
```

### 2.2 通用响应格式

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

### 2.3 通用错误响应

```json
{
  "code": 400,
  "message": "参数错误",
  "data": null
}
```

### 2.4 常用状态码

| 状态码 | 含义 |
|---|---|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 401 | 未认证 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 500 | 服务端异常 |

## 3. 健康检查 API

### 3.1 服务健康检查

```http
GET /
```

#### 响应示例

```json
{
  "message": "SupportOps Agent API is running"
}
```

### 3.2 API 健康检查

```http
GET /api/health
```

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "status": "ok",
    "service": "supportops-agent",
    "version": "0.1.0"
  }
}
```

## 4. 知识库文档 API

### 4.1 上传知识库文档

用于上传 FAQ、SOP、产品手册、历史工单等文件。

```http
POST /api/documents/upload
```

#### 请求类型

```http
multipart/form-data
```

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| file | File | 是 | 上传文件 |
| doc_type | string | 否 | 文档类型，例如 faq、sop、manual、ticket_history |
| description | string | 否 | 文档说明 |

#### 支持文件类型

```text
.md, .txt, .pdf, .csv, .docx
```

#### 响应示例

```json
{
  "code": 200,
  "message": "文档上传成功",
  "data": {
    "document_id": "doc_001",
    "filename": "FAQ.md",
    "doc_type": "faq",
    "chunk_count": 18,
    "vectorized": true
  }
}
```

### 4.2 获取文档列表

```http
GET /api/documents
```

#### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| page | int | 否 | 页码，默认 1 |
| size | int | 否 | 每页数量，默认 10 |
| doc_type | string | 否 | 文档类型筛选 |

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 2,
    "items": [
      {
        "document_id": "doc_001",
        "filename": "FAQ.md",
        "doc_type": "faq",
        "chunk_count": 18,
        "created_at": "2026-04-30 19:00:00"
      }
    ]
  }
}
```

### 4.3 获取文档详情

```http
GET /api/documents/{document_id}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "document_id": "doc_001",
    "filename": "FAQ.md",
    "doc_type": "faq",
    "description": "企业常见问题文档",
    "chunk_count": 18,
    "created_at": "2026-04-30 19:00:00"
  }
}
```

### 4.4 删除文档

```http
DELETE /api/documents/{document_id}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "文档删除成功",
  "data": {
    "document_id": "doc_001"
  }
}
```

### 4.5 检索知识库

用于测试 RAG 检索效果。

```http
POST /api/documents/search
```

#### 请求体

```json
{
  "query": "账号登录失败怎么办？",
  "top_k": 5,
  "doc_type": "faq"
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "query": "账号登录失败怎么办？",
    "results": [
      {
        "chunk_id": "chunk_001",
        "document_id": "doc_001",
        "filename": "FAQ.md",
        "content": "如果账号登录失败，请先检查账号状态、密码是否正确以及是否完成权限开通。",
        "score": 0.89,
        "metadata": {
          "title": "账号登录失败处理流程"
        }
      }
    ]
  }
}
```

## 5. Chat / Agent 对话 API

### 5.1 普通对话

用于用户向 Agent 提问，Agent 根据知识库和工具调用返回回答。

```http
POST /api/chat
```

#### 请求体

```json
{
  "message": "我的账号登录不上，提示权限不足，应该怎么办？",
  "conversation_id": "conv_001",
  "user_id": "user_001",
  "use_rag": true,
  "auto_create_ticket": true
}
```

#### 请求参数说明

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| message | string | 是 | 用户输入 |
| conversation_id | string | 否 | 会话 ID，不传则新建 |
| user_id | string | 否 | 用户 ID |
| use_rag | bool | 否 | 是否启用 RAG，默认 true |
| auto_create_ticket | bool | 否 | 是否允许自动创建工单，默认 true |

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "conversation_id": "conv_001",
    "reply": "根据知识库中的账号权限处理流程，建议你先确认账号是否已激活，并检查是否已申请对应系统权限。如果仍无法登录，请提供系统名称和完整错误提示。",
    "intent": {
      "category": "账号与权限",
      "priority": "P2",
      "need_follow_up": true,
      "missing_fields": ["系统名称", "错误截图"]
    },
    "sources": [
      {
        "document_id": "doc_001",
        "filename": "FAQ.md",
        "title": "账号登录失败处理流程"
      }
    ],
    "ticket": null,
    "trace_id": "trace_001"
  }
}
```

### 5.2 带工单创建的对话

当 Agent 判断需要人工处理时，可以自动创建工单。

#### 请求示例

```json
{
  "message": "我已经确认密码正确，但还是提示没有权限，请帮我处理。系统是 OA。",
  "conversation_id": "conv_001",
  "user_id": "user_001",
  "use_rag": true,
  "auto_create_ticket": true
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "conversation_id": "conv_001",
    "reply": "已为你创建权限处理工单，工单编号为 T202604300001。IT 支持组将继续处理，请保持联系方式畅通。",
    "intent": {
      "category": "账号与权限",
      "priority": "P2",
      "need_follow_up": false
    },
    "sources": [
      {
        "document_id": "doc_002",
        "filename": "AccountPermissionSOP.md",
        "title": "权限申请 SOP"
      }
    ],
    "ticket": {
      "ticket_id": "T202604300001",
      "title": "OA 系统账号权限不足",
      "category": "账号与权限",
      "priority": "P2",
      "department": "IT支持组",
      "status": "待分派"
    },
    "trace_id": "trace_002"
  }
}
```

### 5.3 获取会话历史

```http
GET /api/chat/conversations/{conversation_id}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "conversation_id": "conv_001",
    "messages": [
      {
        "role": "user",
        "content": "我的账号登录不上，提示权限不足，应该怎么办？",
        "created_at": "2026-04-30 19:10:00"
      },
      {
        "role": "assistant",
        "content": "根据知识库中的账号权限处理流程...",
        "created_at": "2026-04-30 19:10:03"
      }
    ]
  }
}
```

## 6. 工单 API

### 6.1 创建工单

```http
POST /api/tickets
```

#### 请求体

```json
{
  "title": "OA 系统账号权限不足",
  "description": "用户反馈 OA 系统登录时提示权限不足，已确认密码正确。",
  "category": "账号与权限",
  "priority": "P2",
  "department": "IT支持组",
  "user_id": "user_001",
  "source_conversation_id": "conv_001"
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "工单创建成功",
  "data": {
    "ticket_id": "T202604300001",
    "status": "待分派"
  }
}
```

### 6.2 获取工单列表

```http
GET /api/tickets
```

#### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| page | int | 否 | 页码 |
| size | int | 否 | 每页数量 |
| status | string | 否 | 工单状态 |
| category | string | 否 | 工单分类 |
| priority | string | 否 | 优先级 |
| department | string | 否 | 责任部门 |

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 1,
    "items": [
      {
        "ticket_id": "T202604300001",
        "title": "OA 系统账号权限不足",
        "category": "账号与权限",
        "priority": "P2",
        "department": "IT支持组",
        "status": "待分派",
        "created_at": "2026-04-30 19:20:00"
      }
    ]
  }
}
```

### 6.3 获取工单详情

```http
GET /api/tickets/{ticket_id}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "ticket_id": "T202604300001",
    "title": "OA 系统账号权限不足",
    "description": "用户反馈 OA 系统登录时提示权限不足，已确认密码正确。",
    "category": "账号与权限",
    "priority": "P2",
    "department": "IT支持组",
    "status": "待分派",
    "suggested_solution": "建议检查用户是否已开通 OA 系统角色权限。",
    "source_conversation_id": "conv_001",
    "created_at": "2026-04-30 19:20:00",
    "updated_at": "2026-04-30 19:20:00"
  }
}
```

### 6.4 更新工单状态

```http
PATCH /api/tickets/{ticket_id}/status
```

#### 请求体

```json
{
  "status": "处理中"
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "工单状态更新成功",
  "data": {
    "ticket_id": "T202604300001",
    "status": "处理中"
  }
}
```

### 6.5 分派工单

```http
PATCH /api/tickets/{ticket_id}/assign
```

#### 请求体

```json
{
  "department": "IT支持组",
  "assignee": "张三"
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "工单分派成功",
  "data": {
    "ticket_id": "T202604300001",
    "department": "IT支持组",
    "assignee": "张三"
  }
}
```

### 6.6 添加工单备注

```http
POST /api/tickets/{ticket_id}/comments
```

#### 请求体

```json
{
  "content": "已联系用户补充错误截图。",
  "author": "客服A"
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "备注添加成功",
  "data": {
    "comment_id": "comment_001"
  }
}
```

## 7. 人工确认 API

### 7.1 创建人工确认请求

当 Agent 判断某个操作为高风险时，创建人工确认请求。

```http
POST /api/approvals
```

#### 请求体

```json
{
  "action": "reset_password",
  "risk_level": "high",
  "reason": "该操作会重置用户密码，必须人工确认。",
  "payload": {
    "user_id": "user_001",
    "ticket_id": "T202604300001"
  }
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "已创建人工确认请求",
  "data": {
    "approval_id": "approval_001",
    "status": "pending"
  }
}
```

### 7.2 获取确认请求列表

```http
GET /api/approvals
```

#### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| status | string | 否 | pending、approved、rejected |
| risk_level | string | 否 | low、medium、high |

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [
      {
        "approval_id": "approval_001",
        "action": "reset_password",
        "risk_level": "high",
        "status": "pending",
        "reason": "该操作会重置用户密码，必须人工确认。",
        "created_at": "2026-04-30 19:30:00"
      }
    ]
  }
}
```

### 7.3 通过人工确认

```http
POST /api/approvals/{approval_id}/approve
```

#### 请求体

```json
{
  "operator": "admin",
  "comment": "确认用户身份后允许重置密码。"
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "审批通过",
  "data": {
    "approval_id": "approval_001",
    "status": "approved"
  }
}
```

### 7.4 拒绝人工确认

```http
POST /api/approvals/{approval_id}/reject
```

#### 请求体

```json
{
  "operator": "admin",
  "comment": "用户身份未核验，不允许重置密码。"
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "审批已拒绝",
  "data": {
    "approval_id": "approval_001",
    "status": "rejected"
  }
}
```

## 8. Agent Trace API

### 8.1 获取 Trace 列表

```http
GET /api/traces
```

#### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| conversation_id | string | 否 | 会话 ID |
| ticket_id | string | 否 | 工单 ID |

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [
      {
        "trace_id": "trace_001",
        "conversation_id": "conv_001",
        "ticket_id": "T202604300001",
        "created_at": "2026-04-30 19:10:00"
      }
    ]
  }
}
```

### 8.2 获取 Trace 详情

```http
GET /api/traces/{trace_id}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "trace_id": "trace_001",
    "steps": [
      {
        "step_id": "step_001",
        "agent_name": "IntentAgent",
        "tool_name": null,
        "input": "我的账号登录不上，提示权限不足，应该怎么办？",
        "output": "识别为账号与权限类问题，优先级 P2。",
        "created_at": "2026-04-30 19:10:01"
      },
      {
        "step_id": "step_002",
        "agent_name": "RAGAgent",
        "tool_name": "retrieve_knowledge",
        "input": "账号 权限 登录失败",
        "output": "命中 FAQ.md 和 AccountPermissionSOP.md。",
        "created_at": "2026-04-30 19:10:02"
      }
    ]
  }
}
```

## 9. 报告 API

### 9.1 生成处理报告

```http
POST /api/reports/generate
```

#### 请求体

```json
{
  "conversation_id": "conv_001",
  "ticket_id": "T202604300001",
  "format": "markdown"
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "报告生成成功",
  "data": {
    "report_id": "report_001",
    "format": "markdown",
    "content": "# 工单处理报告\n\n## 用户问题\n用户反馈 OA 系统账号权限不足..."
  }
}
```

### 9.2 获取报告详情

```http
GET /api/reports/{report_id}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "report_id": "report_001",
    "format": "markdown",
    "content": "# 工单处理报告\n\n## 用户问题\n...",
    "created_at": "2026-04-30 19:40:00"
  }
}
```

### 9.3 导出报告

```http
GET /api/reports/{report_id}/export
```

#### Query 参数

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| format | string | 否 | markdown、pdf、docx，MVP 阶段默认 markdown |

#### 响应

返回文件下载流。

## 10. 配置 API

### 10.1 获取系统配置

```http
GET /api/settings
```

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "model_name": "gpt-xxx",
    "embedding_model": "text-embedding-3-small",
    "rag_top_k": 5,
    "auto_create_ticket": true,
    "human_approval_enabled": true
  }
}
```

### 10.2 更新系统配置

```http
PATCH /api/settings
```

#### 请求体

```json
{
  "rag_top_k": 5,
  "auto_create_ticket": true,
  "human_approval_enabled": true
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "配置更新成功",
  "data": {
    "rag_top_k": 5,
    "auto_create_ticket": true,
    "human_approval_enabled": true
  }
}
```

## 11. MVP 接口优先级

第一阶段建议优先实现以下接口：

| 优先级 | 接口 | 说明 |
|---|---|---|
| P0 | `GET /` | 服务启动检查 |
| P0 | `POST /api/chat` | 用户和 Agent 对话 |
| P0 | `POST /api/documents/upload` | 上传知识库文档 |
| P0 | `POST /api/documents/search` | RAG 检索测试 |
| P0 | `POST /api/tickets` | 创建工单 |
| P1 | `GET /api/tickets` | 工单列表 |
| P1 | `GET /api/traces/{trace_id}` | 查看 Agent 执行步骤 |
| P1 | `POST /api/reports/generate` | 生成处理报告 |
| P2 | `POST /api/approvals` | 人工确认 |
| P2 | `POST /api/approvals/{approval_id}/approve` | 审批通过 |
| P2 | `POST /api/approvals/{approval_id}/reject` | 审批拒绝 |

## 12. 前后端页面对应关系

| 前端页面 | 主要接口 |
|---|---|
| ChatView | `POST /api/chat`, `GET /api/chat/conversations/{id}` |
| KnowledgeBaseView | `POST /api/documents/upload`, `GET /api/documents`, `POST /api/documents/search` |
| TicketView | `GET /api/tickets`, `GET /api/tickets/{id}`, `PATCH /api/tickets/{id}/status` |
| ApprovalView | `GET /api/approvals`, `POST /api/approvals/{id}/approve`, `POST /api/approvals/{id}/reject` |
| TraceView | `GET /api/traces`, `GET /api/traces/{id}` |
| ReportView | `POST /api/reports/generate`, `GET /api/reports/{id}` |

## 13. 后端模块建议

```text
backend/
  app/
    main.py
    config.py
    api/
      health.py
      chat.py
      documents.py
      tickets.py
      approvals.py
      traces.py
      reports.py
      settings.py
    agents/
      intent_agent.py
      rag_agent.py
      action_agent.py
      risk_agent.py
      reply_agent.py
    tools/
      rag_tools.py
      ticket_tools.py
      approval_tools.py
      report_tools.py
    services/
      llm_service.py
      embedding_service.py
      vector_store_service.py
      document_service.py
      ticket_service.py
      trace_service.py
      report_service.py
    models/
      schemas.py
      database.py
      document.py
      ticket.py
      trace.py
      approval.py
      report.py
```

## 14. 开发建议

建议开发顺序：

1. `GET /` 和 `GET /api/health`；
2. `POST /api/chat` 固定回复版本；
3. 接入大模型，完成普通对话；
4. 实现文档上传和解析；
5. 实现 embedding 和 RAG 检索；
6. 将 RAG 接入 `POST /api/chat`；
7. 实现工单创建和查询；
8. 实现 Agent 自动创建工单；
9. 实现 Trace 日志；
10. 实现人工确认和报告生成。

