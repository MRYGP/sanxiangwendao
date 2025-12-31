"""
Reorganize scattered root-level documents into better locations.

Why a script?
- The execution environment may wrap commands in PowerShell, which can break when running
  chained commands involving non-ASCII paths. A Python script is more robust on Windows.

This script performs file moves (not git mv). Git usually still detects renames.
"""

from __future__ import annotations

from pathlib import Path
import shutil


MOVES: list[tuple[str, str]] = [
    # Tooling / SOP docs
    ("新文档写作快速参考.md", "99-工具与SOP/写作/新文档写作快速参考.md"),
    ("新文档写作框架指南.md", "99-工具与SOP/写作/新文档写作框架指南.md"),
    ("知识库构建SOP.md", "99-工具与SOP/知识库/知识库构建SOP.md"),
    ("RAG索引重建操作指南.md", "99-工具与SOP/知识库/RAG索引重建操作指南.md"),
    # Product research project raw material
    ("AI产品竞品分析系统指令v2.0.md", "AI产品分析/AI产品竞品分析/00_系统指令/原始资料/AI产品竞品分析系统指令v2.0.md"),
    # Knowledge docs
    ("AI创业大赛的思考.md", "02-shu/innovation/AI创业大赛的思考.md"),
    ("财富创造的范式转移.md", "01-dao/theory/财富创造的范式转移.md"),
    # Training docs
    ("培训知识库筛选方案.md", "training/培训知识库筛选方案.md"),
]


def move_file(src_rel: str, dst_rel: str) -> None:
    src = Path(src_rel)
    dst = Path(dst_rel)

    def _safe_ascii(text: str) -> str:
        # Some environments use a narrow console encoding (e.g. cp1252).
        # Convert to an ASCII-only representation to avoid UnicodeEncodeError.
        return text.encode("utf-8", "backslashreplace").decode("ascii", "ignore")

    if not src.exists():
        print(f"[SKIP] missing: {_safe_ascii(src_rel)}")
        return

    dst.parent.mkdir(parents=True, exist_ok=True)

    # If destination exists, do not overwrite silently.
    if dst.exists():
        raise FileExistsError(f"Destination already exists: {_safe_ascii(dst_rel)}")

    shutil.move(str(src), str(dst))
    print(f"[OK] {_safe_ascii(src_rel)} -> {_safe_ascii(dst_rel)}")


def main() -> None:
    for src, dst in MOVES:
        move_file(src, dst)


if __name__ == "__main__":
    main()


