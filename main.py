from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from database import db
from models import DataModel, DataModel2, AbstractModel
from ml_utils import getEmbedding, string_to_list
from sklearn.metrics.pairwise import cosine_similarity
from config import CORS_ORIGIN

app = FastAPI()

# CORS setup (using environment variable)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[CORS_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/checkscore")
async def check(abstract_1: str, abstract_2: str):
    embedding_1 = getEmbedding(abstract_1)
    embedding_2 = getEmbedding(abstract_2)
    similarity_score = cosine_similarity([embedding_1], [embedding_2])
    return {"score": float(similarity_score[0][0])}

@app.post("/compareDatabase")
async def compareDatabase(text: DataModel2):
    embedding = getEmbedding(text.abstract)
    docs = db.abstracts.find({})
    scores = [(doc["title"], cosine_similarity(string_to_list(doc["abstract_e"]), [embedding])[0][0], doc["abstract"], str(doc["_id"])) for doc in docs]
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:3] + [str(embedding)]

@app.post("/api/insert")
async def insert1(data: DataModel):
    db.embeddings.insert_one({
        "title_r": data.title,
        "title_e": str(getEmbedding(data.title)),
        "abstract_r": data.abstract,
        "abstract_e": str(getEmbedding(data.abstract)),
        "domain_r": data.domains,
        "keyword_r": data.keywords,
    })
    return {"message": "done"}

@app.get("/api/display")
async def display1():
    return [doc.get("raw", "No raw data available") for doc in db.embeddings.find({})]

@app.post("/api/insert2")
async def insert2(request: Request, abstracts: list[AbstractModel]):
    if not abstracts:
        raise HTTPException(status_code=400, detail="No abstracts submitted to insert")

    abstracts_to_insert = [{
        "ownerId": str(request.state.user._id) if hasattr(request.state, 'user') else "anonymous",
        "title": abstract.title,
        "abstract": abstract.abstract,
        "abstract_e": str(getEmbedding(abstract.abstract)),
        "domain": abstract.domain,
        "keywords": abstract.keywords,
        "status": "completed"
    } for abstract in abstracts]

    result = db.abstracts.insert_many(abstracts_to_insert)
    if not result.inserted_ids:
        raise HTTPException(status_code=400, detail="Proper abstracts format required")

    return {"message": "Abstracts submitted successfully"}

handler = Mangum(app)
