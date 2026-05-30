"""
RAG 注册表一致性校验：YAML ↔ DOC_MAPPING ↔ 主文档
build_index 启动前必须通过，否则报错退出。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

import yaml

from .config import DOC_MAPPING, DOCS_DIR, INDEX_DIR, PROJECT_ROOT, get_doc_file_path

CROSS_REFS_PATH = PROJECT_ROOT / "_cross_refs.yaml"


@dataclass
class RegistryValidationResult:
    ghost_yaml: List[str] = field(default_factory=list)
    ghost_mapping: List[str] = field(default_factory=list)
    duplicate_doc_ids: Dict[str, List[str]] = field(default_factory=dict)
    yaml_syntax_errors: List[str] = field(default_factory=list)
    cross_ref_ghost: List[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not (
            self.ghost_yaml
            or self.ghost_mapping
            or self.duplicate_doc_ids
            or self.yaml_syntax_errors
            or self.cross_ref_ghost
        )

    def format_report(self) -> str:
        lines = ["❌ 校验失败,发现以下问题:", ""]
        if self.ghost_yaml:
            lines.append(f"[幽灵 YAML] {len(self.ghost_yaml)} 个 YAML 文件不在 DOC_MAPPING 中:")
            for item in self.ghost_yaml:
                lines.append(f"  - {item}")
            lines.append("")
        if self.ghost_mapping:
            lines.append(f"[幽灵 mapping] {len(self.ghost_mapping)} 个注册指向不存在的主文档:")
            for item in self.ghost_mapping:
                lines.append(f"  - {item}")
            lines.append("")
        if self.duplicate_doc_ids:
            lines.append(f"[重复 doc_id] {len(self.duplicate_doc_ids)} 处:")
            for doc_id, files in sorted(self.duplicate_doc_ids.items()):
                lines.append(f"  - {doc_id} 出现在: {', '.join(files)}")
            lines.append("")
        if self.yaml_syntax_errors:
            lines.append(f"[YAML 语法错误] {len(self.yaml_syntax_errors)} 处:")
            for item in self.yaml_syntax_errors:
                lines.append(f"  - {item}")
            lines.append("")
        if self.cross_ref_ghost:
            lines.append(
                f"[_cross_refs.yaml 幽灵引用] {len(self.cross_ref_ghost)} 处:"
            )
            for item in self.cross_ref_ghost:
                lines.append(f"  - {item}")
            lines.append("")
        return "\n".join(lines).rstrip()


def _load_yaml_documents(path: Path) -> List[dict]:
    with open(path, encoding="utf-8") as f:
        return [doc for doc in yaml.safe_load_all(f) if isinstance(doc, dict) and doc]


def validate_cross_refs(
    cross_refs_path: Path = CROSS_REFS_PATH,
    doc_mapping: Dict[str, str] = None,
) -> List[str]:
    """校验 _cross_refs.yaml 中本仓库 doc_id 均已在 DOC_MAPPING 注册。"""
    doc_mapping = doc_mapping or DOC_MAPPING
    ghosts: List[str] = []

    if not cross_refs_path.exists():
        return ghosts

    with open(cross_refs_path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    this_repo_ids: List[tuple[str, str]] = []

    for item in data.get("masters_in_this_repo") or []:
        doc_id = item.get("id")
        if doc_id:
            this_repo_ids.append((str(doc_id), "masters_in_this_repo"))

    for item in data.get("references_to_other_repos") or []:
        doc_id = item.get("this_doc_id")
        if doc_id:
            this_repo_ids.append((str(doc_id), "references_to_other_repos.this_doc_id"))

    for doc_id, location in this_repo_ids:
        if doc_id not in doc_mapping:
            ghosts.append(f"{doc_id} ({location}): 不在 DOC_MAPPING 中")

    return ghosts


def validate_registry(
    index_dir: Path = INDEX_DIR,
    doc_mapping: Dict[str, str] = None,
) -> RegistryValidationResult:
    doc_mapping = doc_mapping or DOC_MAPPING
    result = RegistryValidationResult()

    yaml_files = sorted(index_dir.glob("DOC-*.yaml"))
    yaml_stems = {p.stem for p in yaml_files}

    for stem in sorted(yaml_stems - set(doc_mapping.keys())):
        result.ghost_yaml.append(stem)

    doc_id_to_files: Dict[str, List[str]] = {}
    for yaml_path in yaml_files:
        try:
            documents = _load_yaml_documents(yaml_path)
        except yaml.YAMLError as e:
            result.yaml_syntax_errors.append(f"{yaml_path.name}: {e}")
            continue

        if len(documents) != 1:
            result.yaml_syntax_errors.append(
                f"{yaml_path.name}: 应包含 1 个 YAML 文档块,实际 {len(documents)} 个"
            )
            continue

        inner_id = documents[0].get("doc_id")
        if inner_id:
            doc_id_to_files.setdefault(str(inner_id), []).append(yaml_path.name)

        if yaml_path.stem not in doc_mapping:
            continue

    for doc_id, files in doc_id_to_files.items():
        if len(files) > 1:
            result.duplicate_doc_ids[doc_id] = files

    for doc_id in sorted(doc_mapping.keys()):
        if doc_id not in yaml_stems:
            result.ghost_mapping.append(f"{doc_id}: 缺少索引文件 {doc_id}.yaml")
            continue
        try:
            path = get_doc_file_path(doc_id)
        except FileNotFoundError:
            result.ghost_mapping.append(
                f"{doc_id}: 找不到主文档 {doc_mapping[doc_id]!r}"
            )
            continue
        if not path.exists():
            result.ghost_mapping.append(
                f"{doc_id}: 主文档路径不存在 {path.relative_to(DOCS_DIR)}"
            )

    result.cross_ref_ghost = validate_cross_refs(doc_mapping=doc_mapping)

    return result


def assert_registry_valid() -> None:
    result = validate_registry()
    if not result.ok:
        raise SystemExit(result.format_report())
