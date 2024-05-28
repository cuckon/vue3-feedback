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


async def get_data_from_db():
    db = get_db()
    collection = db['feedbacks']
    pipeline = [
        {"$group": {
            "_id": "$to",
            "data": {
                "$push": {
                    "user": "$user",
                    "timestamp": "$timestamp",
                    "rate": "$rate",
                    "good_comment":
                    "$good_comment",
                    "bad_comment":
                    "$bad_comment"
                }
            }
        }},
        {"$project": {"_id": 0, "to": "$_id", "data": 1}},
        {"$sort": {"user": 1}},
    ]
    result = [doc async for doc in collection.aggregate(pipeline)]
    return result

def write_excel(data):
    import xlwt
    from datetime import datetime

    style_title = xlwt.easyxf('font:bold on')
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = xlwt.Style.colour_map['gray25']
    style_date.pattern = pattern

    style_date = xlwt.easyxf(num_format_str='D-MMM-YY')
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Feedbacks')

    current_ln = 0

    # write header
    ws.write(0, 0, 'Feedbacker', style_title)
    ws.write(0, 1, 'date', style_title)
    ws.write(0, 2, 'to', style_title)
    ws.write(0, 3, 'rate', style_title)
    ws.write(0, 4, 'good_comment', style_title)
    ws.write(0, 5, 'bad_comment', style_title)

    for per_feedback_engineer in data:
        ws.write(current_ln, 0, per_feedback_engineer['user'])
        # TODO: full header

        ws.write(
            current_ln, 1,
            datetime.fromtimestamp(per_feedback_engineer['data']['timestamp']),
            style_date
        )
        ws.write(current_ln, 2, per_feedback_engineer['data']['user'])
        ws.write(current_ln, 3, per_feedback_engineer['data']['rate'])
        ws.write(current_ln, 3, per_feedback_engineer['data']['good_comment'])
        ws.write(current_ln, 3, per_feedback_engineer['data']['bad_comment'])
        current_ln += 1



@app.get('/download_summary')
async def download_summary():

    return await get_data_from_db()

    import xlwt
    from datetime import datetime


    ws.write(0, 0, 'Feedbacker')
    ws.write(1, 0, datetime.now(), style_date)
    ws.write(2, 0, 'Feedbacker')




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
