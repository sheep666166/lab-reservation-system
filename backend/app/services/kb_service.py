import os
# 设置 Hugging Face 镜像站（解决国内访问问题）
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")

from chromadb.api.models.Collection import Collection
from chromadb.utils import embedding_functions
import chromadb
from app.config import BASE_DIR

KB_DIR = BASE_DIR / "data" / "kb"
CHROMA_DIR = BASE_DIR / "data" / "chroma"

_collection = None
_embedding_fn = None

def get_embedding_fn():
    global _embedding_fn
    if _embedding_fn is not None:
        return _embedding_fn
    _embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="BAAI/bge-small-zh-v1.5"
)
    return _embedding_fn

def get_collection() -> Collection:
    """向量库的初始化"""
    global _collection
    if _collection is not None:
        return _collection
    KB_DIR.mkdir(parents=True,exist_ok=True)
    CHROMA_DIR.mkdir(parents=True,exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    col = client.get_or_create_collection(
        name = "lab_kb",embedding_function=get_embedding_fn()
    )

    if col.count() == 0:
        ids = []
        docs = []
        metas = []
        for path in sorted(KB_DIR.glob("*.md")):
            text = path.read_text(encoding="utf-8").strip()
            if not text:
                continue
            docs.append(text)
            ids.append(path.stem)
            metas.append({"source": path.name})
        if docs:
            col.add(ids=ids,documents=docs,metadatas=metas)
    _collection = col
    return col

def warm_up():
    col = get_collection()
    if col.count() >0 :
        col.query(query_texts=["预热"],n_results=1)




def search(query: str):
    """根据关键字去检索向量数据库"""
    col = get_collection()
    if col.count() == 0:
        return ""
    limit = min(5,col.count())
    res = col.query(query_texts=[query],n_results=limit)
    docs = (res.get("documents") or [[]])[0]
    metas = (res.get("metadatas") or [[]])[0]
    distances = (res.get("distances") or [[]])[0]

    score_parts = []
    for doc, meta, dist in zip(docs, metas, distances):
        # 0-1 越接近1表示越相关
        score = 1 / (1 + dist)
        if score < 0.5:
            continue
        name = meta.get("source") or ""
        score_parts.append({"score": score, "content": f"[{name}]\n{doc}"})
    score_parts.sort(key=lambda x: x["score"], reverse=True)
    final_parts = [item["content"] for item in score_parts[:2]]
    return "\n\n".join(final_parts)


        