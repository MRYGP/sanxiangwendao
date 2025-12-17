"""
文档加载与解析模块
负责读取Markdown文档、解析YAML索引、文档分块
"""

import yaml
import re
from pathlib import Path
from typing import Dict, List, Optional
import logging
import tiktoken

from .config import INDEX_DIR, DOCS_DIR, CHUNK_SIZE, CHUNK_OVERLAP, get_doc_file_path

logger = logging.getLogger(__name__)

# 初始化tokenizer（用于计算token数）
try:
    encoding = tiktoken.get_encoding("cl100k_base")  # GPT-3.5/GPT-4使用的编码
except:
    encoding = None
    logger.warning("tiktoken未安装，将使用字符数估算token数")

class DocumentLoader:
    """文档加载器"""
    
    def __init__(
        self,
        docs_dir: Path = DOCS_DIR,
        index_dir: Path = INDEX_DIR
    ):
        """
        初始化文档加载器
        
        Args:
            docs_dir: 文档目录
            index_dir: 索引文件目录
        """
        self.docs_dir = docs_dir
        self.index_dir = index_dir
        self.index_cache = {}  # 缓存索引数据
    
    def load_index(self, doc_id: str) -> Dict:
        """
        加载文档索引文件
        
        Args:
            doc_id: 文档ID（如 DOC-D001）
            
        Returns:
            索引数据字典
        """
        if doc_id in self.index_cache:
            return self.index_cache[doc_id]
        
        index_file = self.index_dir / f"{doc_id}.yaml"
        
        if not index_file.exists():
            raise FileNotFoundError(f"索引文件不存在: {index_file}")
        
        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                index_data = yaml.safe_load(f)
            
            self.index_cache[doc_id] = index_data
            return index_data
        except Exception as e:
            logger.error(f"加载索引文件失败 {index_file}: {e}")
            raise
    
    def load_document(self, doc_id: str) -> Dict:
        """
        加载单个文档及其索引
        
        Args:
            doc_id: 文档ID
            
        Returns:
            包含索引和内容的字典
        """
        # 加载索引
        index_data = self.load_index(doc_id)
        
        # 获取文档文件路径
        try:
            doc_file = get_doc_file_path(doc_id)
        except FileNotFoundError:
            # 尝试从索引中的title获取文件名
            title = index_data.get('title', '')
            if title:
                # 移除可能的扩展名
                title_base = title.replace('.md', '')
                # 查找匹配的文件
                possible_files = list(self.docs_dir.glob(f"*{title_base}*"))
                if possible_files:
                    doc_file = possible_files[0]
                else:
                    raise FileNotFoundError(f"找不到文档文件: {title}")
            else:
                raise FileNotFoundError(f"无法确定文档文件路径: {doc_id}")
        
        # 读取文档内容
        try:
            with open(doc_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            logger.error(f"读取文档文件失败 {doc_file}: {e}")
            raise
        
        return {
            'doc_id': doc_id,
            'index': index_data,
            'content': content,
            'file_path': doc_file
        }
    
    def chunk_document(
        self,
        doc: Dict,
        chunk_size: int = CHUNK_SIZE,
        overlap: int = CHUNK_OVERLAP
    ) -> List[Dict]:
        """
        文档分块
        
        Args:
            doc: 文档字典（包含index和content）
            chunk_size: 块大小（token数）
            overlap: 重叠大小（token数）
            
        Returns:
            文档块列表
        """
        chunks = []
        doc_id = doc['doc_id']
        index = doc['index']
        content = doc['content']
        
        # 1. 元数据块
        metadata_chunk = {
            'doc_id': doc_id,
            'chunk_type': 'metadata',
            'content': self._format_metadata(index),
            'weight': 1.0,
            'metadata': {
                'doc_type': index.get('doc_type', ''),
                'layer': index.get('layer', ''),
                'doc_weight': index.get('doc_weight', 'important')
            }
        }
        chunks.append(metadata_chunk)
        
        # 2. 摘要块
        summary = index.get('summary', '')
        if summary:
            summary_chunk = {
                'doc_id': doc_id,
                'chunk_type': 'summary',
                'content': summary,
                'weight': 1.5,
                'metadata': {
                    'doc_type': index.get('doc_type', ''),
                    'layer': index.get('layer', ''),
                    'doc_weight': index.get('doc_weight', 'important')
                }
            }
            chunks.append(summary_chunk)
        
        # 3. query_patterns块（单独索引，用于问题-文档映射）
        query_patterns = index.get('query_patterns', [])
        if query_patterns:
            for i, pattern in enumerate(query_patterns):
                pattern_chunk = {
                    'doc_id': doc_id,
                    'chunk_type': 'query_pattern',
                    'content': pattern,
                    'weight': 1.3,
                    'pattern_index': i,
                    'metadata': {
                        'doc_type': index.get('doc_type', ''),
                        'layer': index.get('layer', ''),
                        'doc_weight': index.get('doc_weight', 'important')
                    }
                }
                chunks.append(pattern_chunk)
        
        # 4. 正文块（按段落和token数切分）
        content_chunks = self._split_content(content, chunk_size, overlap)
        
        for i, chunk_text in enumerate(content_chunks):
            chunks.append({
                'doc_id': doc_id,
                'chunk_type': 'content',
                'chunk_index': i,
                'content': chunk_text,
                'weight': 1.0,
                'metadata': {
                    'doc_type': index.get('doc_type', ''),
                    'layer': index.get('layer', ''),
                    'doc_weight': index.get('doc_weight', 'important')
                }
            })
        
        # 5. 案例块（从内容中提取）
        example_chunks = self._extract_examples(content)
        for i, example in enumerate(example_chunks):
            chunks.append({
                'doc_id': doc_id,
                'chunk_type': 'example',
                'content': example,
                'weight': 1.2,
                'example_index': i,
                'metadata': {
                    'doc_type': index.get('doc_type', ''),
                    'layer': index.get('layer', ''),
                    'doc_weight': index.get('doc_weight', 'important')
                }
            })
        
        logger.info(f"文档 {doc_id} 分块完成，共 {len(chunks)} 个块")
        return chunks
    
    def _format_metadata(self, index: Dict) -> str:
        """格式化元数据为文本"""
        parts = [
            f"文档ID: {index.get('doc_id', '')}",
            f"标题: {index.get('title', '')}",
            f"类型: {index.get('doc_type', '')}",
            f"层级: {index.get('layer', '')}",
        ]
        
        summary = index.get('summary', '')
        if summary:
            parts.append(f"摘要: {summary}")
        
        keywords = index.get('keywords', [])
        if keywords:
            parts.append(f"关键词: {', '.join(keywords)}")
        
        return '\n'.join(parts)
    
    def _count_tokens(self, text: str) -> int:
        """计算文本的token数"""
        if encoding:
            return len(encoding.encode(text))
        else:
            # 简单估算：中文约1.5字符=1token，英文约4字符=1token
            chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
            other_chars = len(text) - chinese_chars
            return int(chinese_chars / 1.5 + other_chars / 4)
    
    def _split_content(
        self,
        content: str,
        chunk_size: int,
        overlap: int
    ) -> List[str]:
        """
        按token数切分内容
        
        Args:
            content: 文档内容
            chunk_size: 块大小（token数）
            overlap: 重叠大小（token数）
            
        Returns:
            文本块列表
        """
        # 先按段落分割
        paragraphs = re.split(r'\n\n+', content)
        
        chunks = []
        current_chunk = []
        current_tokens = 0
        
        for para in paragraphs:
            para_tokens = self._count_tokens(para)
            
            # 如果单个段落就超过chunk_size，需要进一步切分
            if para_tokens > chunk_size:
                # 先保存当前块
                if current_chunk:
                    chunks.append('\n\n'.join(current_chunk))
                    current_chunk = []
                    current_tokens = 0
                
                # 切分大段落
                sub_chunks = self._split_long_paragraph(para, chunk_size, overlap)
                chunks.extend(sub_chunks)
            else:
                # 检查是否可以加入当前块
                if current_tokens + para_tokens > chunk_size and current_chunk:
                    # 保存当前块
                    chunks.append('\n\n'.join(current_chunk))
                    
                    # 处理重叠：保留最后一部分作为新块的开始
                    if overlap > 0 and len(current_chunk) > 0:
                        overlap_text = current_chunk[-1]
                        overlap_tokens = self._count_tokens(overlap_text)
                        if overlap_tokens < overlap:
                            # 如果最后一段不够重叠，尝试保留最后两段
                            if len(current_chunk) > 1:
                                overlap_text = '\n\n'.join(current_chunk[-2:])
                                overlap_tokens = self._count_tokens(overlap_text)
                        
                        if overlap_tokens <= overlap:
                            current_chunk = [overlap_text, para]
                            current_tokens = overlap_tokens + para_tokens
                        else:
                            current_chunk = [para]
                            current_tokens = para_tokens
                    else:
                        current_chunk = [para]
                        current_tokens = para_tokens
                else:
                    current_chunk.append(para)
                    current_tokens += para_tokens
        
        # 保存最后一个块
        if current_chunk:
            chunks.append('\n\n'.join(current_chunk))
        
        return chunks
    
    def _split_long_paragraph(
        self,
        text: str,
        chunk_size: int,
        overlap: int
    ) -> List[str]:
        """切分超长段落"""
        # 按句子分割
        sentences = re.split(r'[。！？\n]', text)
        chunks = []
        current_chunk = []
        current_tokens = 0
        
        for sentence in sentences:
            if not sentence.strip():
                continue
            
            sentence_tokens = self._count_tokens(sentence)
            
            if current_tokens + sentence_tokens > chunk_size and current_chunk:
                chunks.append(''.join(current_chunk))
                
                # 重叠处理
                if overlap > 0:
                    overlap_text = current_chunk[-1] if current_chunk else ""
                    overlap_tokens = self._count_tokens(overlap_text)
                    if overlap_tokens < overlap:
                        current_chunk = [overlap_text, sentence]
                        current_tokens = overlap_tokens + sentence_tokens
                    else:
                        current_chunk = [sentence]
                        current_tokens = sentence_tokens
                else:
                    current_chunk = [sentence]
                    current_tokens = sentence_tokens
            else:
                current_chunk.append(sentence)
                current_tokens += sentence_tokens
        
        if current_chunk:
            chunks.append(''.join(current_chunk))
        
        return chunks
    
    def _extract_examples(self, content: str) -> List[str]:
        """
        提取案例块
        
        查找包含"案例"、"例子"、"示例"等标记的段落
        """
        examples = []
        
        # 匹配模式：案例/例子/示例 + 冒号 + 内容
        patterns = [
            r'(?:案例|例子|示例)[：:]\s*\n?(.*?)(?=\n\n|\n#|$)',
            r'##\s*(?:案例|例子|示例).*?\n(.*?)(?=\n##|\Z)',
            r'###\s*(?:案例|例子|示例).*?\n(.*?)(?=\n###|\n##|\Z)',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, content, re.DOTALL | re.IGNORECASE)
            for match in matches:
                example_text = match.group(1).strip()
                if example_text and len(example_text) > 20:  # 过滤太短的
                    examples.append(example_text)
        
        # 去重
        seen = set()
        unique_examples = []
        for ex in examples:
            ex_hash = hash(ex[:100])  # 用前100字符作为hash
            if ex_hash not in seen:
                seen.add(ex_hash)
                unique_examples.append(ex)
        
        return unique_examples
