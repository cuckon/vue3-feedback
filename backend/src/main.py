from typing import List, Optional
import functools
import motor.motor_asyncio

from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

MONGODB_URL = 'mongodb://root:root@pipe.rs.netease.com:23017'


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@functools.lru_cache
def get_db():
    DB_CLIENT = motor.motor_asyncio.AsyncIOMotorClient(
        MONGODB_URL
    )['feedback']
    return DB_CLIENT

class PerFeedback(BaseModel):
    to: str
    rate: int
    good_comment: str
    bad_comment: str


class Feedback(BaseModel):
    user: str
    timestamp: int
    feedbacks: List[PerFeedback]


@app.get('/engineers')
async def get_engineers(feedbacker:str = None):
    engineers_by_feedbacker = {
        'John': ['张三', '李四'],
        '丁磊': ['王五'],
    }

    # return the found list
    if (result := engineers_by_feedbacker.get(feedbacker)):
        return result

    # return all if not found
    result = []
    for engineers in engineers_by_feedbacker.values():
        result.extend(engineers)
    return list(set(result))


@app.post('/feedbacks')
async def post_feedback(feedback: Feedback):
    if not feedback.feedbacks:
        raise HTTPException(status_code=422, detail='no feedbacks')
    db = get_db()
    collection = db['feedbacks']
    base_data = feedback.dict(exclude={'feedbacks'})
    docs = [
        {**base_data, **f.dict()} for f in feedback.feedbacks
    ]
    await collection.insert_many(docs)


@app.get('/')
async def root():
    return {'message': 'Hello World'}