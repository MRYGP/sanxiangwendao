#!/usr/bin/env python3
"""仅校验 DOC_MAPPING ↔ YAML ↔ 主文档一致性，不构建向量索引。"""

import importlib.util
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

rag_system_path = project_root / "rag-system"
rag_system_init = rag_system_path / "__init__.py"
spec = importlib.util.spec_from_file_location("rag_system", rag_system_init)
rag_system_module = importlib.util.module_from_spec(spec)
sys.modules["rag_system"] = rag_system_module
spec.loader.exec_module(rag_system_module)

for module_file in ["config", "registry_check"]:
    module_path = rag_system_path / f"{module_file}.py"
    spec = importlib.util.spec_from_file_location(
        f"rag_system.{module_file}", module_path
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[f"rag_system.{module_file}"] = module
    spec.loader.exec_module(module)

from rag_system.config import DOC_MAPPING, INDEX_DIR
from rag_system.registry_check import validate_registry


def main() -> int:
    result = validate_registry()
    yaml_count = len(list(INDEX_DIR.glob("DOC-*.yaml")))
    mapping_count = len(DOC_MAPPING)

    if not result.ok:
        print(result.format_report())
        print(f"\nDOC_MAPPING: {mapping_count} / YAML: {yaml_count}")
        return 1

    if mapping_count != yaml_count:
        print(f"FAIL count mismatch: DOC_MAPPING={mapping_count}, YAML={yaml_count}")
        return 1

    print(f"OK DOC_MAPPING: {mapping_count} / YAML: {yaml_count} / consistent")
    d_count = sum(1 for k in DOC_MAPPING if k.startswith("DOC-D"))
    s_count = sum(1 for k in DOC_MAPPING if k.startswith("DOC-S"))
    print(f"Distribution: DOC-D {d_count} / DOC-S {s_count} / total {mapping_count}")
    if result.cross_ref_ghost:
        print("cross_refs: FAIL")
    else:
        print("cross_refs: OK (_cross_refs.yaml local doc_ids all in DOC_MAPPING)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
