from openai import AsyncOpenAI
from app.common.exceptions import BusinessException
from app.config import settings
from app.services.kb_service import search
from app.schemas.ai import ChatRequest
import json
import traceback
from sqlalchemy.orm import Session
from app.services import lab_service,equipment_service

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_open_labs",
            "description": "查询当前开放中的实验室列表，可以按名称关键字来筛选",
            "parameters": {
                "type": "object",
                "properties": {
                    "keywords": {
                        "type": "string",
                        "description": "实验室的名称关键字，可以为空",
                    }
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_lab_equipments",
            "description": "查询某个实验室下的设备列表",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab_id": {
                        "type": "integer",
                        "description": "实验室 ID",
                    },
                    "keywords": {
                        "type": "string",
                        "description": "设备名称的关键字，可以为空",
                    },
                },
            },
        },
    },
]



SYSTEM_PROMPT = """你是智能实验室预约系统的助手，回答要简洁。
如果下面提供了实验室资料，请依据资料回答规则、安全、文档里的开放时间说明。

重要：当用户询问"现在有哪些开放的实验室"、"哪些实验室可以预约"、"当前能约的实验室"等涉及实时状态的查询时，必须调用 list_open_labs 工具查询数据库获取最新信息，不要仅凭知识库内容回答。
查询某个实验室的设备时，必须调用 list_lab_equipments 工具。

你不能替用户提交预约，也不能直接改数据库。
如果用户要预约，请说明去「实验室列表」选择后提交，等待管理员审核。
"""

def run_tool(db: Session, name: str, arguments: str) -> str:
    try:
        args = json.loads(arguments or "{}")
    except json.JSONDecodeError:
        return json.dumps({"error": "参数不是合法的json"}, ensure_ascii=False)

    try:
        if name == "list_open_labs":
            keywords = (args.get("keywords") or "").strip() or None
            page = lab_service.get_lab_page_list(
                db, page=1, page_size=10, keywords=keywords, status=1
            )
            rows = [
                {
                    "id": item.id,
                    "name": item.name,
                    "location": item.location,
                    "capacity": item.capacity,
                    "open_time": item.open_time,
                    "close_time": item.close_time,
                }
                for item in page.list
            ]
            return json.dumps({"total": page.total, "labs": rows}, ensure_ascii=False)

        if name == "list_lab_equipments":
            lab_id = args.get("lab_id")
            if not lab_id:
                return json.dumps(
                    {"error": "参数缺少实验室 lab_id"}, ensure_ascii=False
                )
            keywords = (args.get("keywords") or "").strip() or None
            page = equipment_service.get_equipment_page_list(
                db, page=1, page_size=10, lab_id=int(lab_id), keywords=keywords
            )
            rows = [
                {
                    "id": item.id,
                    "name": item.name,
                    "lab_id": item.lab_id,
                    "lab_name": item.lab_name,
                    "sepc": item.spec,
                    "quantity": item.quantity,
                    "status": item.status,
                }
                for item in page.list
            ]
            return json.dumps(
                {"total": page.total, "equipments": rows}, ensure_ascii=False
            )

        return json.dumps({"error": f"未找到工具：{name}"}, ensure_ascii=False)

    except Exception as exc:
        return json.dumps({"error": exc.message}, ensure_ascii=False)



def get_client() -> AsyncOpenAI:
    if not settings.LLM_API_KEY:
        raise BusinessException(message="未获取到大模型的api_key")
    return AsyncOpenAI(
        api_key=settings.LLM_API_KEY,
        base_url=settings.LLM_BASE_URL,
        timeout=30.0  # 连接超时 30 秒
    )

async def Chat(db: Session, data: ChatRequest):
    if not data.messages:
        raise BusinessException(message="对话内容为空")
    history = []
    for message in data.messages:
        if message.role in ("user","assistant") and message.content.strip():
            history.append(message.model_dump())
    if not history:
        raise BusinessException(message="请输入您要对话的内容")
    question = next((item["content"] for item in reversed(history) if item["role"] =="user"),"")
    knowledge = search(query=question)
    system_prompt = SYSTEM_PROMPT
    if knowledge:
        system_prompt += "\n\n以下是检索到的实验室资料:\n" + knowledge
    client = get_client()
    messages = [
        {"role": "system", "content": system_prompt},
        *history,
    ]
    try:
         for _ in range(3):
            res = await client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
                timeout=60.0  # 请求超时 60 秒
            )
            msg = res.choices[0].message
            tool_calls = msg.tool_calls or []
            if not tool_calls:  # 没有工具调用 则直接返回大模型的输出结果内容
                content = msg.content
                if not content or not content.strip():
                    raise BusinessException(message="大模型没有返回内容")
                return content
            messages.append(
                {
                    "role": "assistant",
                    "content": msg.content or "",
                    "tool_calls": [
                        {
                            "id": call.id,
                            "type": "function",
                            "function": {
                                "name": call.function.name,
                                "arguments": call.function.arguments,
                            },
                        }
                        for call in tool_calls
                    ],
                }
            )
            for call in tool_calls:
                result = run_tool(db, call.function.name, call.function.arguments)
                messages.append(
                    {"role": "tool", "content": result, "tool_call_id": call.id}
                )
    except BusinessException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise BusinessException(message=f"大模型调用失败：{str(e)}")
