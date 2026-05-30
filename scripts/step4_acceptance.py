"""Step 4 post-build self-check and 8 acceptance queries."""
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

rag_system_path = project_root / "rag-system"
spec = importlib.util.spec_from_file_location("rag_system", rag_system_path / "__init__.py")
mod = importlib.util.module_from_spec(spec)
sys.modules["rag_system"] = mod
spec.loader.exec_module(mod)

for name in ["config", "embedding", "vector_store", "retriever"]:
    p = rag_system_path / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"rag_system.{name}", p)
    m = importlib.util.module_from_spec(spec)
    sys.modules[f"rag_system.{name}"] = m
    spec.loader.exec_module(m)

from rag_system.config import (
    COLLECTION_NAME,
    DOC_MAPPING,
    EMBEDDING_DEVICE,
    EMBEDDING_MODEL,
    INDEX_DIR,
    VECTOR_DB_DIR,
)
from rag_system.embedding import EmbeddingModel
from rag_system.retriever import HybridRetriever
from rag_system.vector_store import VectorStore

QUERIES = [
    ("认知流变学 水流与河床", "DOC-D025"),
    ("挂果前必须种菜 双轨", "DOC-D018"),
    ("认知内共生 CEO 实战", "DOC-D001"),
    ("阶段错配 不死模式", "DOC-D024"),
    ("神经可塑性 内在稳定", "DOC-D029"),
    ("红队攻击 决策模式", "DOC-S083"),
    ("生命信息论", "DOC-D026"),
    ("AI创业大赛", "DOC-S080"),
]


def main():
    records_path = (
        VECTOR_DB_DIR / "numpy_store" / COLLECTION_NAME / "records.json"
    )
    with open(records_path, encoding="utf-8") as f:
        records = json.load(f)
    doc_ids = [m.get("doc_id", "") for m in records["metadatas"]]
    unique = sorted(set(doc_ids))
    print("=== SELF CHECK ===")
    print(f"chunks: {len(doc_ids)}")
    print(f"unique doc_id: {len(unique)}")
    print(f"DOC_MAPPING: {len(DOC_MAPPING)}")
    missing = sorted(set(DOC_MAPPING.keys()) - set(unique))
    extra = sorted(set(unique) - set(DOC_MAPPING.keys()))
    print(f"missing from store: {missing or 'none'}")
    print(f"extra in store: {extra or 'none'}")
    print()

    embedding_model = EmbeddingModel(EMBEDDING_MODEL, EMBEDDING_DEVICE)
    vector_store = VectorStore(VECTOR_DB_DIR, COLLECTION_NAME)
    retriever = HybridRetriever(vector_store, embedding_model, INDEX_DIR)

    print("=== 8 ACCEPTANCE QUERIES (top-5) ===")
    results = []
    for i, (query, expected) in enumerate(QUERIES, 1):
        hits = retriever.retrieve(query, top_k=5)
        top1 = hits[0]["doc_id"] if hits else "NONE"
        top1_score = hits[0]["score"] if hits else 0.0
        ok = top1 == expected
        print(f"\n#{i} query={query!r} expected={expected}")
        for j, h in enumerate(hits, 1):
            mark = " <-- top1" if j == 1 else ""
            in_top = expected in [x["doc_id"] for x in hits]
            print(f"  [{j}] {h['doc_id']} score={h['score']:.4f}{mark}")
        rank_expected = next(
            (j for j, h in enumerate(hits, 1) if h["doc_id"] == expected), None
        )
        if not ok and rank_expected is None:
            hits10 = retriever.retrieve(query, top_k=10)
            rank10 = next(
                (j for j, h in enumerate(hits10, 1) if h["doc_id"] == expected),
                None,
            )
            print(f"  expected rank in top-10: {rank10 or 'NOT IN TOP-10'}")
        results.append(
            {
                "query": query,
                "expected": expected,
                "top1": top1,
                "top1_score": top1_score,
                "ok": ok,
                "rank_expected_top5": rank_expected,
            }
        )

    passed = sum(1 for r in results if r["ok"])
    print(f"\n=== SUMMARY: {passed}/8 top1 match ===")
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
