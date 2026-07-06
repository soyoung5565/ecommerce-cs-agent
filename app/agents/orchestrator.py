"""Agent编排层 — L0-L3 多Agent架构

参考 KnoCell 的分层设计:
- L0 Router: 意图分类 + 用户画像 + 平台识别
- L1 Specialist: 售前/售后/推荐/投诉 专项Agent
- L2 Integrator: 结果整合 + 格式化 + 安全审核
- L3 Escalator: 转人工 + 工单创建
"""

from enum import Enum
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
import logging
import json

from app.core.config import settings

logger = logging.getLogger(__name__)


# ========== L0: 意图分类 ==========

class Intent(str, Enum):
    """客户意图分类"""
    PRE_SALES = "pre_sales"         # 售前咨询（商品信息/规格/库存/活动）
    AFTER_SALES = "after_sales"     # 售后处理（退换货/退款/改地址/物流）
    RECOMMENDATION = "recommendation"  # 商品推荐（客户主动要推荐/关联购买）
    COMPLAINT = "complaint"         # 投诉（差评威胁/情绪激动/服务不满）
    CHITCHAT = "chitchat"           # 闲聊（无明确意图的闲聊）
    OTHER = "other"                 # 其他


class Urgency(str, Enum):
    """紧急程度"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"          # 差评威胁、资金问题
    URGENT = "urgent"      # 多次投诉、平台介入


@dataclass
class RoutingResult:
    """L0路由结果"""
    intent: Intent
    urgency: Urgency
    platform: str
    shop_id: str
    buyer_id: str
    needs_human: bool = False
    buyer_tags: list = field(default_factory=list)       # 新客/老客/高价值/疑似恶意
    context: dict = field(default_factory=dict)          # 提取的上下文（订单号等）


async def route_message(
    platform: str,
    shop_id: str,
    buyer_id: str,
    content: str,
    conversation_history: list = None,
) -> RoutingResult:
    """L0 意图路由器
    
    使用LLM对客户消息进行意图分类、紧急程度判断、
    是否需要转人工的决策。
    
    TODO: 实际接入LLM调用，当前为规则引擎占位
    """
    # 规则引擎快速判断（后续替换为LLM）
    content_lower = content.lower()

    # 售后关键词
    after_sales_keywords = ["退款", "退货", "换货", "退换", "退款", "修改地址", "改地址",
                           "物流", "快递", "没收到", "破损", "质量问题", "发错", "少件"]
    if any(kw in content_lower for kw in after_sales_keywords):
        intent = Intent.AFTER_SALES
    # 推荐关键词
    elif any(kw in content_lower for kw in ["推荐", "还有", "其他", "类似", "更好"]):
        intent = Intent.RECOMMENDATION
    # 投诉关键词
    elif any(kw in content_lower for kw in ["投诉", "差评", "举报", "315", "12315", "骗子"]):
        intent = Intent.COMPLAINT
    # 售前关键词
    elif any(kw in content_lower for kw in ["多少钱", "价格", "有货", "库存", "怎么卖",
                                            "尺码", "颜色", "材质", "尺寸", "重量"]):
        intent = Intent.PRE_SALES
    else:
        intent = Intent.PRE_SALES  # 默认归为售前

    # 紧急程度
    urgency = Urgency.NORMAL
    if intent == Intent.COMPLAINT:
        urgency = Urgency.HIGH
    if any(kw in content_lower for kw in ["投诉", "315", "12315"]):
        urgency = Urgency.URGENT

    # 是否需要转人工
    needs_human = urgency in (Urgency.HIGH, Urgency.URGENT)

    result = RoutingResult(
        intent=intent,
        urgency=urgency,
        platform=platform,
        shop_id=shop_id,
        buyer_id=buyer_id,
        needs_human=needs_human,
    )

    logger.info(f"L0路由: [{platform}] {buyer_id} → intent={intent.value} urgency={urgency.value} human={needs_human}")
    return result


# ========== L1: 专项Agent ==========

async def handle_pre_sales(routing: RoutingResult, content: str, **kwargs) -> str:
    """L1 售前Agent — 商品咨询、规格查询、库存、活动说明
    
    TODO: 接入RAG知识库 + 商品查询工具
    """
    logger.info(f"L1售前: {content[:30]}")
    # 后续实现:
    # 1. 从RAG知识库检索相关商品信息
    # 2. 调用search_products / get_product_detail工具
    # 3. 用LLM生成自然语言回复
    return "您好！感谢您的咨询。请问您想了解哪款商品呢？我可以帮您查询价格、库存和详细规格。"


async def handle_after_sales(routing: RoutingResult, content: str, **kwargs) -> str:
    """L1 售后Agent — 退换货、改地址、物流查询、退款审核
    
    TODO: 接入订单查询 + 风控引擎 + 退款工具
    """
    logger.info(f"L1售后: {content[:30]}")
    # 后续实现:
    # 1. 从消息中提取订单号（LLM解析）
    # 2. 调用query_order获取订单信息
    # 3. 调用assess_refund_risk做风控评估
    # 4. 根据决策结果执行: 自动退款/转人工/协商
    # 5. 生成回复
    return "好的，我来帮您处理售后问题。请问您的订单号是多少呢？或者您可以描述一下遇到的问题。"


async def handle_recommendation(routing: RoutingResult, content: str, **kwargs) -> str:
    """L1 推荐Agent — 关联推荐、凑单、上新通知
    
    TODO: 接入商品搜索 + 购买历史分析
    """
    logger.info(f"L1推荐: {content[:30]}")
    return "好的，我来为您推荐几款热门商品。请问您有什么偏好吗？比如预算范围或者想要的类型？"


async def handle_complaint(routing: RoutingResult, content: str, **kwargs) -> str:
    """L1 投诉Agent — 情绪安抚、赔偿方案、转人工
    
    TODO: 接入情感分析 + 工单系统
    """
    logger.info(f"L1投诉: {content[:30]}")
    # 投诉类通常需要转人工，但先安抚
    return "非常抱歉给您带来了不好的体验！我已经记录了您的问题，会尽快为您处理。请问能详细描述一下具体情况吗？如果问题比较紧急，我可以帮您转接专属客服。"


async def handle_chitchat(routing: RoutingResult, content: str, **kwargs) -> str:
    """L1 闲聊处理"""
    return "您好呀～有什么可以帮到您的吗？如果您在挑选商品，我可以为您推荐哦！"


# ========== L2: 整合Agent ==========

async def integrate_response(
    routing: RoutingResult,
    raw_response: str,
    tools_used: list = None,
) -> str:
    """L2 回复整合 — 格式化 + 安全审核
    
    TODO:
    1. 检查回复是否泄露内部信息
    2. 检查是否包含过度承诺
    3. 适配平台消息格式限制
    4. 添加平台特定的后缀（如好评引导）
    """
    # 输出过滤
    filtered = _filter_response(raw_response)

    # 根据平台调整格式
    # 拼多多消息长度限制较短，需要更简洁
    if routing.platform == "pdd" and len(filtered) > 500:
        filtered = filtered[:497] + "..."

    return filtered


def _filter_response(response: str) -> str:
    """输出过滤 — 防止泄露系统信息"""
    sensitive_patterns = ["api_key", "token", "secret", "password", "系统提示", "system prompt"]
    for pattern in sensitive_patterns:
        if pattern.lower() in response.lower():
            logger.warning(f"输出过滤: 检测到敏感词 '{pattern}'")
            return "抱歉，我无法回答这个问题。请问还有其他可以帮到您的吗？"
    return response


# ========== L3: 转人工 ==========

async def escalate_to_human(
    routing: RoutingResult,
    reason: str,
    context: dict = None,
) -> str:
    """L3 转人工 — 创建工单 + 通知人工客服
    
    TODO:
    1. 创建工单（接入TGO工单系统或自建）
    2. 通过企业微信/钉钉通知客服
    3. 告知客户已转人工
    """
    logger.info(f"L3转人工: [{routing.platform}] {routing.buyer_id} 原因={reason}")

    # 通知机制（后续实现）
    # await notify_human_agent(shop_id=routing.shop_id, buyer_id=routing.buyer_id, reason=reason)

    return "好的，正在为您转接人工客服，请稍等片刻。人工客服会尽快为您处理，感谢您的耐心等待！"
