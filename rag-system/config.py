"""
RAG知识库系统配置文件
"""

import os
from pathlib import Path

# 尝试加载环境变量（可选依赖）
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv 未安装，跳过环境变量加载
    pass

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
# ⚠️ 重要：每次在 doc-mapping.md 中添加新文档后，必须同步更新此字典！
# 更新步骤：
#   1. 在 doc-mapping.md 中添加文档ID映射
#   2. 在此处添加对应的 DOC_MAPPING 条目
#   3. 创建对应的 YAML 索引文件（rag-index/indexes/DOC-XXX.yaml）
#   4. 运行 python scripts/build_index.py 重建索引
# 详细检查清单：rag-index/索引更新检查清单.md
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
    "DOC-D013": "伟大不能被计划，但可以被有计划地接住.md",
    "DOC-D014": "财富创造的范式转移.md",
    "DOC-D015": "熵增定律与负熵流-万物运行的底层逻辑.md",
    "DOC-D016": "社会资源论：商业成功的第四维度.md",
    "DOC-D017": "产品设计的三大反人性陷阱.md",
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
    "DOC-S028": "芒格不会投你的AI创业公司.md",
    "DOC-S029": "跟着感觉走——可能是你听过的最坑人的建议.md",
    "DOC-S030": "为什么有些人明知道该离开，却怎么也走不了.md",
    "DOC-S031": "即兴演讲.md",
    "DOC-S032": "破坏式创新.md",
    "DOC-S033": "价值链创新.md",
    "DOC-S034": "供应链数字化.md",
    "DOC-S035": "高频业务的战略价值.md",
    "DOC-S036": "精益创业.md",
    "DOC-S037": "从0到1.md",
    "DOC-S038": "规则制定者.md",
    "DOC-S039": "受益方共创模式：精益创业的补充.md",
    "DOC-S040": "AI应用拆解实验室：导师能力训练指南.md",
    "DOC-S041": "生态型VC构建指南：从个人投资到规则制定者.md",

    # --- business-cases（商业学习子项目） ---
    # 说明：这里使用“相对路径”避免 README.md 等同名文件的歧义
    "DOC-S042": "shangye-anli/README.md",
    "DOC-S043": "shangye-anli/00_系统指令/README.md",
    "DOC-S044": "shangye-anli/00_系统指令/Claude-案例拆解提示词.md",
    "DOC-S045": "shangye-anli/00_系统指令/Claude-模型提炼提示词.md",
    "DOC-S046": "shangye-anli/00_系统指令/Claude-洞察归纳提示词.md",
    "DOC-S047": "三大标杆的可复用方法论-Notion亚马逊Musk.md",
    "DOC-S048": "创业项目评估方法论-从归因分析到投资决策.md",
    "DOC-S049": "shangye-anli/02_模型库/模型总索引.md",
    "DOC-S050": "shangye-anli/03_洞察库/洞察总索引.md",
    "DOC-S051": "shangye-anli/05_学习记录/学习进度追踪器.md",
    "DOC-S052": "shangye-anli/01_案例库/按行业分类/消费零售/案例模板.md",

    # --- AI产品分析 / AI产品竞品分析 ---
    "DOC-S053": "AI产品分析/README.md",
    "DOC-S054": "AI产品分析/AI产品竞品分析/README.md",
    "DOC-S055": "AI产品分析/AI产品竞品分析/00_系统指令/README.md",
    "DOC-S056": "AI产品分析/AI产品竞品分析/00_系统指令/Claude-竞品分析主指令.md",
    "DOC-S057": "AI产品分析/AI产品竞品分析/00_系统指令/Claude-导师点评指令.md",
    "DOC-S058": "AI产品分析/AI产品竞品分析/00_系统指令/Claude-评分系统指令.md",
    "DOC-S059": "AI产品分析/AI产品竞品分析/00_系统指令/Claude-失败案例分析指令.md",
    "DOC-S060": "AI产品分析/AI产品竞品分析/00_系统指令/Cursor-文档生成指令.md",
    "DOC-S061": "AI产品分析/AI产品竞品分析/01_竞品库/竞品总索引.md",
    "DOC-S062": "AI产品分析/AI产品竞品分析/03_追踪记录/追踪总览.md",
    "DOC-S063": "AI产品分析/AI产品竞品分析/04_改进清单/改进清单总表.md",
    "DOC-S064": "AI产品分析/AI产品竞品分析/01_竞品库/产品模板/Step9-完整报告.md",
    "DOC-S065": "深度用户才是真正的护城河.md",
    "DOC-S066": "Notion案例深度拆解：为什么始终被模仿但从未被超越？.md",
    "DOC-S067": "shangye-anli/01_案例库/按行业分类/科技互联网/AI创业项目评估系统 - 商业计划书.md",
    "DOC-S068": "创业神话的致命陷阱-你为什么被私募式创业割了韭菜.md",
    "DOC-S069": "婚姻决策框架-择偶与关系管理的系统性分析.md",
    "DOC-S070": "B端杠杆：撬动C端市场的务实路径.md",
    "DOC-S071": "白标SaaS与生态链杠杆.md",
}

def get_doc_file_path(doc_id: str) -> Path:
    """根据doc_id获取文档文件路径"""
    if doc_id not in DOC_MAPPING:
        raise ValueError(f"未知的文档ID: {doc_id}")
    
    filename = DOC_MAPPING[doc_id]

    # 支持 DOC_MAPPING 直接存放相对路径（用于避免 README.md 等重名文件带来的歧义）
    # 例如： "shangye-anli/README.md"
    direct_path = DOCS_DIR / filename
    if direct_path.exists():
        return direct_path
    
    # 首先尝试在新目录结构中查找（01-dao/ 和 02-shu/）
    possible_dirs = [
        DOCS_DIR / "01-dao" / "theory",
        DOCS_DIR / "01-dao" / "framework",
        DOCS_DIR / "01-dao" / "philosophy",
        DOCS_DIR / "02-shu" / "innovation",
        DOCS_DIR / "02-shu" / "communication",
        DOCS_DIR / "02-shu" / "behavior-change",
        DOCS_DIR / "02-shu" / "strategy",
        DOCS_DIR / "02-shu" / "execution",
        DOCS_DIR / "02-shu" / "psychology",
        DOCS_DIR,  # 最后尝试根目录（向后兼容）
    ]
    
    for dir_path in possible_dirs:
        file_path = dir_path / filename
        if file_path.exists():
            return file_path
    
    # 如果直接路径找不到，尝试递归查找
    possible_files = list(DOCS_DIR.rglob(filename))
    if possible_files:
        return possible_files[0]
    
    # 最后尝试模糊匹配
    filename_base = filename.split('.')[0]
    possible_files = list(DOCS_DIR.rglob(f"*{filename_base}*"))
    if possible_files:
        return possible_files[0]
    
    raise FileNotFoundError(f"找不到文档文件: {filename}")
