# 智能实验室预约系统

> 基于 AI 大模型的智能实验室预约管理系统，支持自然语言交互预约、智能知识库问答、自动化预约审核等功能。

---

##  项目简介

智能实验室预约系统是一款面向高校、科研机构设计的现代化实验室管理解决方案。系统采用前后端分离架构，融合 AI 大语言模型技术，提供智能化的实验室预约体验。

用户可以通过自然语言与 AI 助手对话，完成实验室查询、设备检索、预约提交等操作，同时系统支持知识库检索，自动回答实验室规则、开放时间、安全规范等常见问题。

**核心亮点：**
-  AI 智能助手：支持自然语言对话式预约
- 📚 智能知识库：自动检索实验室文档资料
-  实时流式响应：SSE 技术实现打字机效果
- 🔐 角色权限管理：区分学生和管理员权限
-  响应式界面：基于 Element Plus 的现代化 UI

---

## 🛠️ 技术栈

### 后端技术

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.12+ | 开发语言 |
| FastAPI | 0.115.13 | Web 框架 |
| SQLAlchemy | 2.0.41 | ORM 数据库框架 |
| PyMySQL | 1.1.1 | MySQL 数据库驱动 |
| Pydantic Settings | 2.7.1 | 配置管理 |
| JWT (PyJWT) | 2.15.1 | 用户认证 |
| Bcrypt | 4.0.1 | 密码加密 |
| OpenAI SDK | ≥1.0.0 | 大模型调用 |
| LangChain | ≥0.1.0 | AI 应用框架 |
| LangGraph | ≥0.0.20 | Agent 工作流编排 |
| ChromaDB | ≥0.4.0 | 向量数据库（知识库） |
| Uvicorn | 0.34.0 | ASGI 服务器 |

### 前端技术

| 技术 | 版本 | 用途 |
|------|------|------|
| Vue 3 | 3.5.42 | 前端框架 |
| TypeScript | 6.0.0 | 类型安全 |
| Vite | 8.2.2 | 构建工具 |
| Vue Router | 5.3.1 | 路由管理 |
| Element Plus | 2.14.7 | UI 组件库 |
| Axios | 1.20.0 | HTTP 请求库 |
| Marked | 18.1.0 | Markdown 解析 |
| DOMPurify | 2.5.9 | XSS 防护 |
| ESLint | - | 代码规范 |
| Prettier | 3.9.6 | 代码格式化 |

### 数据库

- **MySQL** - 主业务数据库（用户、实验室、设备、预约记录）
- **ChromaDB** - 向量数据库（知识库文档存储）

---

## 🏗️ 项目流程

### 系统架构流程

```
─────────────────────────────────────────────────────────────────────┐
│                          用户浏览器                                  │
│                    (Vue 3 + Element Plus)                           │
└─────────────────────────┬───────────────────────────────────────────┘
                          │ HTTP/HTTPS
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      FastAPI 后端服务                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │  认证中间件   │  │  异常处理     │  │  CORS 中间件              │  │
│  └──────────────┘  └──────────────┘  ──────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────────  │
│  │                    API 路由层                                 │  │
│  │  /api/auth  /api/user  /api/lab  /api/equipment              │  │
│  │  /api/reservation  /api/ai  /api/files                       │  │
│  └──────────────────────────────────────────────────────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │  Service 层   │  │  LangGraph   │  │  ChromaDB 知识库          │  │
│  │  (业务逻辑)   │  │  (AI Agent)  │  │  (向量检索)               │  │
│  └──────────────┘  └──────────────  └──────────────────────────┘  │
└─────────────────────────┬───────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        MySQL 数据库                                  │
│     users | labs | equipments | reservations                       │
└─────────────────────────────────────────────────────────────────────┘
```

### 用户操作流程

```
学生用户：
登录 → 查看实验室列表 → 选择实验室/设备 → 提交预约 → 等待审核 → 使用实验室

管理员用户：
登录 → 实验室管理 → 设备管理 → 用户管理 → 预约审核 → 通过/拒绝预约

AI 助手：
所有用户 → 进入 AI 聊天 → 自然语言提问 → AI 检索知识库/查询数据库 → 返回结果
         → 如需预约 → AI 确认信息 → 用户确认 → 自动提交预约
```

### 预约审核流程

```
学生提交预约 → 状态：待审核 (0)
                ↓
管理员审核 → 通过：状态 (1) / 拒绝：状态 (2)
                ↓
预约成功 → 学生可使用实验室
```

---

## ✨ 项目独特性与优点

### 独特功能

1. **AI Agent 智能预约**
   - 基于 LangGraph 构建的 Agent 工作流
   - 支持多轮对话、工具调用、自动决策
   - 可自主完成日期计算、实验室查询、设备检索、预约提交

2. **RAG 知识库问答**
   - 集成 ChromaDB 向量数据库
   - 支持实验室规则、安全规范、开放时间等文档检索
   - 结合大模型生成精准回答

3. **SSE 流式输出**
   - Server-Sent Events 实时推送
   - 打字机效果的流畅体验
   - 实时显示 AI 思考过程和工具调用状态

4. **自动化任务**
   - 启动时自动预热向量知识库
   - 异步扫描过期预约，自动更新状态

### 技术优点

| 优点 | 说明 |
|------|------|
| **前后端分离** | 清晰的架构边界，便于维护和扩展 |
| **类型安全** | 后端 Pydantic + 前端 TypeScript 双重保障 |
| **异常处理完善** | 全局异常处理器，统一错误响应格式 |
| **安全认证** | JWT Token + Bcrypt 密码加密 + 路由守卫 |
| **代码规范** | ESLint + Prettier 统一代码风格 |
| **响应式 UI** | Element Plus 组件库，界面美观易用 |
| **流式响应** | SSE 技术实现实时数据推送 |
| **向量检索** | ChromaDB 支持语义搜索，提升问答准确率 |

---

##  项目运行步骤

### 环境要求

- **Python** ≥ 3.12
- **Node.js** ≥ 22.18.0 或 ≥ 24.12.0
- **MySQL** ≥ 8.0
- **npm** 或 **pnpm**

### 1. 克隆项目

```bash
git clone https://github.com/sheep666166/lab-reservation-system.git
cd lab-reservation-system
```

### 2. 后端配置

#### 2.1 创建虚拟环境

```bash
cd backend
python -m venv .venv

# Windows 激活
.venv\Scripts\activate

# Linux/Mac 激活
source .venv/bin/activate
```

#### 2.2 安装依赖

```bash
pip install -r requirements.txt
```

#### 2.3 配置环境变量

创建或修改 `backend/.env` 文件：

```env
# 数据库配置
DATABASE_URL=mysql+pymysql://用户名:密码@127.0.0.1:3306/lab_agent

# JWT 配置
JWT_SECRET_KEY=你的随机密钥（建议使用至少 32 位随机字符串）
JWT_EXPIRE_HOURS=24
JWT_ALGORITHM=HS256

# 大模型配置（以阿里云通义千问为例）
LLM_API_KEY=你的 API Key
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL=qwen-plus
```

#### 2.4 创建数据库

```sql
CREATE DATABASE lab_agent DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### 2.5 启动后端服务

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

后端服务地址：`http://localhost:8000`

API 文档：`http://localhost:8000/docs`

### 3. 前端配置

#### 3.1 安装依赖

```bash
cd frontend
npm install
```

#### 3.2 配置环境变量

创建或修改 `frontend/.env.development` 文件：

```env
# 后端 API 地址（留空表示同源，开发时配置代理）
VITE_API_BASE_URL=
```

#### 3.3 启动前端服务

```bash
npm run dev
```

前端服务地址：`http://localhost:5173`

### 4. 知识库初始化

系统启动时会自动预热知识库。如需手动添加文档：

1. 将文档放入 `backend/data/kb/` 目录
2. 支持 `.md` 格式的文档
3. 系统会自动向量化存储

默认知识库文档：
- `安全规范.md` - 实验室安全使用规范
- `开放时间.md` - 实验室开放时间说明
- `设备使用.md` - 设备使用指南
- `预约规则.md` - 预约流程规则

### 5. 访问系统

浏览器打开 `http://localhost:5173`

**默认测试账号：**
- 管理员：`admin / admin123`
- 学生：`student / student123`

---

## 📋 功能特性

### 用户认证模块

| 功能 | 说明 |
|------|------|
| 用户注册 | 支持学生和管理员账号注册 |
| 用户登录 | JWT Token 认证，支持 24 小时免登录 |
| 密码修改 | 支持用户自主修改密码 |
| 权限控制 | 基于角色的访问控制（学生/管理员） |

### 实验室管理模块（管理员）

| 功能 | 说明 |
|------|------|
| 实验室列表 | 查看所有实验室信息 |
| 添加实验室 | 录入新实验室（名称、位置、容量、开放时间等） |
| 编辑实验室 | 修改实验室信息 |
| 删除实验室 | 停用/删除实验室 |
| 实验室状态 | 设置实验室开放/关闭状态 |

### 设备管理模块（管理员）

| 功能 | 说明 |
|------|------|
| 设备列表 | 查看实验室设备 |
| 添加设备 | 录入新设备（名称、型号、数量等） |
| 编辑设备 | 修改设备信息 |
| 设备状态 | 设置设备正常/维修状态 |

### 预约管理模块

| 功能 | 学生 | 管理员 | 说明 |
|------|------|--------|------|
| 提交预约 | ✅ | - | 选择实验室/设备、时间提交预约 |
| 我的预约 | ✅ | - | 查看个人预约记录 |
| 取消预约 | ✅ | - | 取消待审核的预约 |
| 预约审核 | - | ✅ | 通过/拒绝学生预约申请 |
| 预约列表 | ✅ | ✅ | 分页查看预约记录 |

### AI 智能助手模块

| 功能 | 说明 |
|------|------|
| 知识库问答 | 检索实验室文档，回答规则、开放时间等问题 |
| 实时查询 | 查询当前开放的实验室列表 |
| 设备查询 | 查询指定实验室的设备信息 |
| 智能预约 | 通过对话完成预约信息确认和提交 |
| 日期识别 | 自动识别"今天"、"明天"等自然语言日期 |
| 流式响应 | SSE 实时推送，打字机效果显示 |
| 过程可视化 | 显示 AI 思考和工具调用过程 |

### 用户管理模块（管理员）

| 功能 | 说明 |
|------|------|
| 用户列表 | 查看所有注册用户 |
| 用户信息 | 查看用户详细信息 |
| 用户状态 | 启用/禁用用户账号 |

### 个人中心模块

| 功能 | 说明 |
|------|------|
| 个人信息 | 查看和修改个人资料 |
| 头像上传 | 支持上传用户头像 |
| 修改密码 | 修改登录密码 |

### 文件上传模块

| 功能 | 说明 |
|------|------|
| 图片上传 | 支持实验室封面、设备图片上传 |
| 文件类型 | 支持 jpg、png、pdf、doc 等格式 |
| 文件大小 | 最大支持 100MB |

---

##  接口/API

### 基础信息

- **Base URL**: `http://localhost:8000`
- **认证方式**: JWT Bearer Token
- **请求格式**: JSON
- **响应格式**: 统一响应结构

### 响应结构

```json
{
  "code": 200,
  "message": "成功",
  "data": {}
}
```

### 认证接口 `/api/auth`

| 方法 | 路径 | 说明 | 请求体 | 响应 |
|------|------|------|--------|------|
| POST | `/api/auth/login` | 用户登录 | `{ username, password }` | `{ token, user_info }` |
| POST | `/api/auth/register` | 用户注册 | `{ username, password, name, role, email, phone }` | - |

### 用户接口 `/api/user`

| 方法 | 路径 | 说明 | 请求体 | 权限 |
|------|------|------|--------|------|
| GET | `/api/user/info` | 获取当前用户信息 | - | 登录用户 |
| PUT | `/api/user/info` | 更新用户信息 | `{ name, email, phone, avatar }` | 登录用户 |
| PUT | `/api/user/password` | 修改密码 | `{ old_password, new_password }` | 登录用户 |
| GET | `/api/user/list` | 用户列表（分页） | `?page=1&page_size=10` | 管理员 |

### 实验室接口 `/api/lab`

| 方法 | 路径 | 说明 | 请求体 | 权限 |
|------|------|------|--------|------|
| GET | `/api/lab/list` | 实验室列表（分页） | `?page=1&page_size=10&keywords=&status=` | 登录用户 |
| POST | `/api/lab` | 创建实验室 | `{ name, location, capacity, open_time, close_time, description, img }` | 管理员 |
| PUT | `/api/lab/{id}` | 更新实验室 | `{ name, location, capacity, ... }` | 管理员 |
| DELETE | `/api/lab/{id}` | 删除实验室 | - | 管理员 |

### 设备接口 `/api/equipment`

| 方法 | 路径 | 说明 | 请求体 | 权限 |
|------|------|------|--------|------|
| GET | `/api/equipment/list` | 设备列表（分页） | `?page=1&page_size=10&lab_id=&keywords=` | 登录用户 |
| POST | `/api/equipment` | 创建设备 | `{ lab_id, name, description, img, spec, quantity }` | 管理员 |
| PUT | `/api/equipment/{id}` | 更新设备 | `{ name, description, spec, quantity, status }` | 管理员 |
| DELETE | `/api/equipment/{id}` | 删除设备 | - | 管理员 |

### 预约接口 `/api/reservation`

| 方法 | 路径 | 说明 | 请求体 | 权限 |
|------|------|------|--------|------|
| POST | `/api/reservation` | 创建预约 | `{ lab_id, equipment_id, date, start_time, end_time, remark }` | 登录用户 |
| GET | `/api/reservation/list` | 预约列表（分页） | `?page=1&page_size=10&status=` | 登录用户 |
| PUT | `/api/reservation/{id}/cancel` | 取消预约 | - | 登录用户（仅本人） |
| PUT | `/api/reservation/{id}/audit` | 审核预约 | `{ status: 1或2 }` | 管理员 |

### AI 接口 `/api/ai`

| 方法 | 路径 | 说明 | 请求体 | 响应类型 |
|------|------|------|--------|----------|
| POST | `/api/ai/chat/stream` | AI 对话（SSE 流式） | `{ messages: [{ role, content }] }` | `text/event-stream` |

**SSE 事件类型：**

```json
// 状态更新
{ "type": "status", "message": "正在思考…" }

// 工具开始调用
{ "type": "tool_start", "name": "list_open_labs", "label": "查询开放实验室" }

// 工具调用完成
{ "type": "tool_end", "name": "list_open_labs", "label": "查询开放实验室", "preview": "..." }

// 文本片段
{ "type": "token", "content": "你好" }

// 完成
{ "type": "done" }

// 错误
{ "type": "error", "message": "错误信息" }
```

### 文件接口 `/api/files`

| 方法 | 路径 | 说明 | 请求体 | 响应 |
|------|------|------|--------|------|
| POST | `/api/files/upload` | 上传文件 | `FormData: file` | `{ url: "..." }` |

---

##  环境变量

### 后端环境变量 (`backend/.env`)

| 变量名 | 必填 | 说明 | 示例 |
|--------|------|------|------|
| `DATABASE_URL` | ✅ | 数据库连接 URL | `mysql+pymysql://root:123456@127.0.0.1:3306/lab_agent` |
| `JWT_SECRET_KEY` | ✅ | JWT 签名密钥 | `sjQ9crUw71awph8ORnvERoUtMQ19qelECFjj06i1urz` |
| `JWT_EXPIRE_HOURS` | ❌ | Token 过期时间（小时） | `24` |
| `JWT_ALGORITHM` | ❌ | JWT 算法 | `HS256` |
| `LLM_API_KEY` | ✅ | 大模型 API Key | `sk-xxx` |
| `LLM_BASE_URL` | ✅ | 大模型 API 地址 | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| `LLM_MODEL` | ✅ | 大模型名称 | `qwen-plus` |

### 前端环境变量 (`frontend/.env.development`)

| 变量名 | 必填 | 说明 | 示例 |
|--------|------|------|------|
| `VITE_API_BASE_URL` | ❌ | 后端 API 地址（留空为同源） | `http://localhost:8000` |

---

## 📁 目录结构

```
实验室智能预约系统/
├── backend/                          # 后端项目
│   ├── .env                          # 环境变量配置
│   ├── .gitignore                    # Git 忽略文件
│   ├── requirements.txt              # Python 依赖
│   ├── uploads/                      # 上传文件存储
│   ├── data/
│   │   ├── chroma/                   # ChromaDB 向量数据库存储
│   │   └── kb/                       # 知识库文档
│   │       ├── 安全规范.md
│   │       ├── 开放时间.md
│   │       ├── 设备使用.md
│   │       └── 预约规则.md
│   └── app/
│       ├── __init__.py
│       ├── main.py                   # FastAPI 应用入口
│       ├── config.py                 # 配置管理
│       ├── database.py               # 数据库连接
│       ├── api/                      # API 路由层
│       │   ├── __init__.py
│       │   ├── auth.py               # 认证接口
│       │   ├── user.py               # 用户接口
│       │   ├── lab.py                # 实验室接口
│       │   ├── equipment.py          # 设备接口
│       │   ├── reservation.py        # 预约接口
│       │   ├── ai.py                 # AI 接口
│       │   └── files.py              # 文件接口
│       ├── models/                   # 数据模型
│       │   ├── __init__.py
│       │   ├── user.py               # 用户模型
│       │   ├── lab.py                # 实验室模型
│       │   ├── equipment.py          # 设备模型
│       │   └── reservation.py        # 预约模型
│       ├── schemas/                  # 请求/响应 Schema
│       │   ├── __init__.py
│       │   ├── auth.py
│       │   ├── user.py
│       │   ├── lab.py
│       │   ├── equipment.py
│       │   ├── reservation.py
│       │   └── ai.py
│       ├── services/                 # 业务逻辑层
│       │   ├── __init__.py
│       │   ├── auth_service.py       # 认证服务
│       │   ├── user_service.py       # 用户服务
│       │   ├── lab_service.py        # 实验室服务
│       │   ├── equipment_service.py  # 设备服务
│       │   ├── reservation_service.py # 预约服务
│       │   ├── ai_service.py         # AI 服务（基础对话）
│       │   ├── agent_service.py      # Agent 服务（智能对话）
│       │   ├── agent_tools.py        # Agent 工具定义
│       │   └── kb_service.py         # 知识库服务
│       ├── dependencies/             # 依赖注入
│       │   ├── __init__.py
│       │   └── auth.py               # 认证依赖
│       ├── common/                   # 公共模块
│       │   ├── __init__.py
│       │   ├── response.py           # 统一响应
│       │   └── exceptions.py         # 异常处理
│       └── utils/                    # 工具类
│           ├── __init__.py
│           ├── jwt.py                # JWT 工具
│           └── password.py           # 密码工具
│
├── frontend/                         # 前端项目
│   ├── .env.development              # 开发环境变量
│   ├── .eslintrc.json                # ESLint 配置
│   ├── .prettierrc.json              # Prettier 配置
│   ├── .gitignore                    # Git 忽略文件
│   ├── package.json                  # 依赖配置
│   ├── tsconfig.json                 # TypeScript 配置
│   ├── vite.config.ts                # Vite 配置
│   ├── index.html                    # HTML 入口
│   └── src/
│       ├── main.ts                   # 应用入口
│       ├── App.vue                   # 根组件
│       ├── api/                      # API 请求封装
│       │   ├── auth.ts
│       │   ├── user.ts
│       │   ├── lab.ts
│       │   ├── equipment.ts
│       │   ├── reservation.ts
│       │   ├── ai.ts
│       │   └── file.ts
│       ├── assets/                   # 静态资源
│       │   ├── css/
│       │   │   └── global.css        # 全局样式
│       │   └── imgs/
│       │       ── logo.png          # Logo 图片
│       ├── components/               # 公共组件
│       │   └── ReserveDialog.vue     # 预约对话框
│       ├── layouts/                  # 布局组件
│       │   └── Layout.vue            # 主布局（侧边栏+顶栏）
│       ├── router/                   # 路由配置
│       │   └── index.ts
│       ├── utils/                    # 工具函数
│       │   ├── auth.ts               # 认证工具
│       │   ├── request.ts            # 请求封装
│       │   └── user.ts               # 用户工具
│       └── views/                    # 页面视图
│           ├── Login.vue             # 登录页
│           ├── Register.vue          # 注册页
│           ├── Home.vue              # 首页
│           ├── Lab.vue               # 实验室管理（管理员）
│           ├── LabList.vue           # 实验室列表（学生）
│           ├── Equ.vue               # 设备列表管理（管理员）
│           ├── LabEquipment.vue      # 实验室设备（学生）
│           ├── User.vue              # 用户管理（管理员）
│           ├── MyReservation.vue     # 我的预约（学生）
│           ├── AuditReservation.vue  # 预约审核（管理员）
│           ├── Profile.vue           # 个人信息
│           ├── Password.vue          # 修改密码
│           └── AIChat.vue            # AI 智能助手
│
└── .gitignore                        # Git 忽略文件
```

---

## 📊 数据库设计

### 用户表 `users`

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT (PK) | 主键 ID |
| username | VARCHAR(50) | 账号 |
| password | VARCHAR(255) | 密码（加密） |
| name | VARCHAR(50) | 姓名 |
| role | VARCHAR(50) | 角色（student/admin） |
| email | VARCHAR(50) | 邮箱 |
| phone | VARCHAR(50) | 手机号 |
| avatar | VARCHAR(50) | 头像 |
| status | INT | 状态（0-禁用，1-正常） |
| create_time | DATETIME | 创建时间 |
| update_time | DATETIME | 更新时间 |

### 实验室表 `labs`

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT (PK) | 主键 ID |
| name | VARCHAR(50) | 实验室名称 |
| location | VARCHAR(100) | 位置 |
| capacity | INT | 容纳人数 |
| open_time | VARCHAR(20) | 开放开始时间 |
| close_time | VARCHAR(20) | 开放结束时间 |
| description | VARCHAR(500) | 简介 |
| img | VARCHAR(200) | 封面图 |
| status | INT | 状态（0-关闭，1-开放） |
| create_time | DATETIME | 创建时间 |
| update_time | DATETIME | 更新时间 |

### 设备表 `equipments`

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT (PK) | 主键 ID |
| lab_id | INT (FK) | 所属实验室 |
| name | VARCHAR(50) | 设备名称 |
| description | VARCHAR(500) | 说明 |
| img | VARCHAR(200) | 图片 |
| spec | VARCHAR(100) | 型号规格 |
| quantity | INT | 数量 |
| status | INT | 状态（0-维修，1-正常） |
| create_time | DATETIME | 创建时间 |
| update_time | DATETIME | 更新时间 |

### 预约表 `reservations`

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT (PK) | 主键 ID |
| user_id | INT (FK) | 预约人 |
| lab_id | INT (FK) | 实验室 |
| equipment_id | INT (FK) | 设备（可空） |
| date | VARCHAR(20) | 预约日期 |
| start_time | VARCHAR(20) | 开始时间 |
| end_time | VARCHAR(20) | 结束时间 |
| remark | VARCHAR(255) | 备注 |
| status | INT | 状态（0-待审核，1-已通过，2-已拒绝，3-已取消） |
| create_time | DATETIME | 创建时间 |
| update_time | DATETIME | 更新时间 |

---

##  安全特性

### 认证与授权

- **JWT Token 认证**：用户登录后获取 Token，后续请求携带 Token 验证身份
- **密码加密**：使用 Bcrypt 算法加密存储，防止密码泄露
- **角色权限控制**：区分学生和管理员权限，敏感操作需要管理员权限
- **路由守卫**：前端路由拦截，未登录用户自动跳转到登录页

### 数据安全

- **SQL 注入防护**：使用 SQLAlchemy ORM，避免原始 SQL 拼接
- **XSS 防护**：前端使用 DOMPurify 过滤 HTML 内容
- **文件上传限制**：限制文件类型和大小，防止恶意文件上传
- **CORS 配置**：限制跨域访问来源

### 异常处理

- **全局异常捕获**：统一处理业务异常、HTTP 异常、验证异常
- **错误日志记录**：记录详细错误信息，便于问题排查
- **友好错误提示**：返回用户友好的错误信息，不暴露系统细节

---

## 🧪 测试

### 后端测试

```bash
# 安装测试依赖
pip install pytest httpx

# 运行测试
pytest
```

### 前端测试

```bash
# 类型检查
npm run type-check

# 代码格式化
npm run format
```

---

## 📝 开发规范

### 后端规范

- 使用 Pydantic Schema 定义请求/响应结构
- 使用 Dependency Injection 管理依赖
- 统一使用 `Response.success()` 返回成功响应
- 异常使用 `BusinessException` 抛出业务错误

### 前端规范

- 使用 TypeScript 编写代码
- 组件使用 Composition API（`<script setup>`）
- API 请求统一在 `src/api/` 目录封装
- 使用 ESLint + Prettier 保持代码风格一致

---

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 项目的部署

本项目已经成功在云服务器上部署，公网访问地址122.51.71.40

---

##  联系方式

如有问题或建议，欢迎通过以下方式联系：

- GitHub Issues: https://github.com/sheep666166/lab-reservation-system/issues
- 邮箱：xmy15162533466@qq.com

---

## 🌟 致谢

感谢以下开源项目：

- [FastAPI](https://fastapi.tiangolo.com/) - 高性能 Web 框架
- [Vue 3](https://vuejs.org/) - 渐进式 JavaScript 框架
- [Element Plus](https://element-plus.org/) - Vue 3 组件库
- [LangChain](https://www.langchain.com/) - AI 应用开发框架
- [LangGraph](https://langchain-ai.github.io/langgraph/) - Agent 工作流编排

---

**Made with ❤️ by xmy**
