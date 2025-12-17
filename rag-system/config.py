"""
RAG知识库系统配置文件
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 项目路径
PROJECT_ROOT = Path(__file__).parent.parent
DOCS_DIR = PROJECT_ROOT  # 文档在根目录
INDEX_DIR = PROJECT_ROOT / "rag-index" / "indexes"
VECTOR_DB_DIR = PROJECT_ROOT / "vector_db"

# 确保目录存在
VECTOR_DB_DIR.mkdir(exist_ok=True)

# Embedding配置
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")
EMBEDDING_DEVICE = os.getenv("EMBEDDING_DEVICE", "cpu")  # 或 "cuda"

# 向量数据库配置
VECTOR_DB_TYPE = os.getenv("VECTOR_DB_TYPE", "chroma")  # chroma | qdrant | milvus
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "wendao_knowledge_base")

# 检索配置
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
TOP_K = int(os.getenv("TOP_K", "5"))  # 返回文档数量

# LLM配置
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # openai | ollama | local
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Ollama配置（如果使用本地模型）
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5")

# 权重配置
WEIGHT_METADATA = float(os.getenv("WEIGHT_METADATA", "1.0"))
WEIGHT_SUMMARY = float(os.getenv("WEIGHT_SUMMARY", "1.5"))
WEIGHT_CONTENT = float(os.getenv("WEIGHT_CONTENT", "1.0"))
WEIGHT_EXAMPLE = float(os.getenv("WEIGHT_EXAMPLE", "1.2"))

# 文档映射（从doc-mapping.md加载）
DOC_MAPPING = {
    # 道层文档
    "DOC-D001": "认知内共生理论：AI时代人类能力进化的根本路径选择.md",
    "DOC-D002": "专家智慧AI化执行理论：从认知场域到智慧共振的哲学与科学框架.md",
    "DOC-D003": "双螺旋进化模型：人机认知协同的进化动力学理论.md",
    "DOC-D004": "递归式认知进化：情境触发事件驱动的人类智能跃迁理论.md",
    "DOC-D005": "集体认知涌现的多维相变模型：创新生态系统的动力学机制与工程实现.md",
    "DOC-D006": "AI史官集合论：三AI联合深度解析与完整实现方案.md",
    "DOC-D007": "心智路径依赖理论：现代人类认知困境的系统性分析框架.md",
    "DOC-D008": "思想体系核心框架 v1.1 - 理论架构与应用索引.md",
    "DOC-D009": "构建北极星.md",
    "DOC-D010": "人生的意义与实践.md",
    "DOC-D011": "时间的朋友.md",
    "DOC-D012": "你的世界在等你按下回车键.md",
    # 术层文档
    "DOC-S001": "创新三元法.md",
    "DOC-S002": "AI驱动的创新工程系统.md",
    "DOC-S003": "初创企业的生存法则.md",
    "DOC-S004": "动态决策框架迹象验证驾驭AI创业的不确定性.md",
    "DOC-S005": "最小可行启动点.md",
    "DOC-S006": "战略性杠杆：顺势借力.md",
    "DOC-S007": "马斯克的五步工作法.md",
    "DOC-S008": "微习惯和正反馈行为改变框架.md",
    "DOC-S009": "RIAIAI坚持突破框架：从不可能到奇迹的六步心智模型.md",
    "DOC-S010": "不要正面回答别人的问题.md",
    "DOC-S011": "让对方HI起来.md",
    "DOC-S012": "透过现象看本质.md",
    "DOC-S013": "非暴力沟通 的深层技巧和思考.md",
    "DOC-S014": "当真诚成为最狡猾的策略.md",
    "DOC-S015": "思考的模型：定向 → 构建 (加法) → 聚焦 (减法) → 迭代 (增长与反馈).md",
    "DOC-S016": "情境驱动的主动赋能.md",
    "DOC-S017": "网络效应与学习效应.md",
    "DOC-S018": "合理化行为分析框架.md",
    "DOC-S019": "突破潜意识给自己画的那个圈.md",
    "DOC-S020": "动态发展观.md",
    "DOC-S021": "系统性应用思维模型工具箱.md",
    "DOC-S022": "构建系统性复杂向上向下向外寻求生机.md",
    "DOC-S023": "最好的老师不是给你答案，而是引导你自己找到答案.md",
    "DOC-S024": "AI 在金融分析中的核心价值——发现人脑无法触及的暗规律非线性，非逻辑，非理性（人脑偶尔却能超越AI的发现).md",
    "DOC-S025": "为什么给儿子讲道理时你很清醒，给客户报价时你就短视了.md",
    "DOC-S026": "超越用户的预期.md",
    "DOC-S027": "当美好变成理所当然.md",
}

def get_doc_file_path(doc_id: str) -> Path:
    """根据doc_id获取文档文件路径"""
    if doc_id not in DOC_MAPPING:
        raise ValueError(f"未知的文档ID: {doc_id}")
    
    filename = DOC_MAPPING[doc_id]
    file_path = DOCS_DIR / filename
    
    if not file_path.exists():
        # 尝试查找相似文件名
        possible_files = list(DOCS_DIR.glob(f"*{filename.split('.')[0]}*"))
        if possible_files:
            return possible_files[0]
        raise FileNotFoundError(f"找不到文档文件: {filename}")
    
    return file_path
