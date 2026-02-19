# -*- coding: utf-8 -*-
""" Quick test: DOC-D019 retrieval """
import sys
import traceback
from pathlib import Path

log = open(Path(__file__).parent.parent / "test_d019_result.txt", "w", encoding="utf-8")
def p(x=""):
    print(x, flush=True)
    log.write(str(x) + "\n")
    log.flush()

try:
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))

    import importlib.util
    spec = importlib.util.spec_from_file_location("rag_system", project_root / "rag-system" / "__init__.py")
    rag = importlib.util.module_from_spec(spec)
    sys.modules["rag_system"] = rag
    spec.loader.exec_module(rag)
    for m in ["config", "embedding", "vector_store", "retriever"]:
        spec = importlib.util.spec_from_file_location(f"rag_system.{m}", project_root / "rag-system" / f"{m}.py")
        mod = importlib.util.module_from_spec(spec)
        sys.modules[f"rag_system.{m}"] = mod
        spec.loader.exec_module(mod)

    from rag_system.config import INDEX_DIR, VECTOR_DB_DIR, COLLECTION_NAME, TOP_K
    from rag_system.embedding import EmbeddingModel
    from rag_system.vector_store import VectorStore
    from rag_system.retriever import HybridRetriever

    query = "为什么有流量却赚不到钱"
    p("Query: " + query)
    p("Loading...")
    emb = EmbeddingModel("BAAI/bge-m3", "cpu")
    vs = VectorStore(VECTOR_DB_DIR, COLLECTION_NAME)
    ret = HybridRetriever(vs, emb, INDEX_DIR)
    p("Retrieving...")
    try:
        res = ret.retrieve(query, top_k=5)
    except Exception as ret_e:
        p("RETRIEVE ERROR: " + str(ret_e))
        raise
    p("Results: " + str(len(res)))
    if res:
        p("First result keys: " + str(list(res[0].keys())))
    for i, r in enumerate(res, 1):
        did = r.get('doc_id', '?')
        sc = r.get('score', 0)
        p(f"  {i}. {did} score={sc:.3f}")
        if did == 'DOC-D019':
            p("     -> DOC-D019 FOUND!")
    p("Done.")
except Exception as e:
    p("ERROR: " + str(e))
    p(traceback.format_exc())
    log.close()
    sys.exit(1)
log.close()
