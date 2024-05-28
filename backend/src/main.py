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
    await collection.create_index([('to', 1), ('user', 1)])
    pipeline = [
        {'$match': {}},
        {'$sort': {'to': 1, 'user': 1}},
        {'$project': {'_id': 0}},
    ]
    result = collection.aggregate(pipeline)
    return await result.to_list(length=None)


def write_excel(data):
    import xlwt
    from datetime import datetime

    style_title = xlwt.easyxf('font:bold on')
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = xlwt.Style.colour_map['gray25']
    style_title.pattern = pattern

    style_date = xlwt.easyxf(num_format_str='D-MMM-YY')
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Feedbacks')

    current_ln = 0

    # write header
    ws.write(current_ln, 0, 'Feedbacker', style_title)
    ws.write(current_ln, 1, 'Date', style_title)
    ws.write(current_ln, 2, 'To', style_title)
    ws.write(current_ln, 3, 'Rate', style_title)
    ws.write(current_ln, 4, 'Good Comment', style_title)
    ws.write(current_ln, 5, 'Bad Comment', style_title)

    current_ln += 1

    for per_feedback_engineer in data:
        ws.write(current_ln, 0, per_feedback_engineer['user'])

        timestamp = per_feedback_engineer['timestamp'] / 1000
        date_data = datetime.fromtimestamp(timestamp)
        ws.write(current_ln, 1, date_data, style_date)

        ws.write(current_ln, 2, per_feedback_engineer['to'])
        ws.write(current_ln, 3, per_feedback_engineer['rate'])
        ws.write(current_ln, 4, per_feedback_engineer['good_comment'])
        ws.write(current_ln, 5, per_feedback_engineer['bad_comment'])
        current_ln += 1

    wb.save('d:/tmp/feedbacks.xls')


@app.get('/download_summary')
async def download_summary():

    data = await get_data_from_db()
    write_excel(data)


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
