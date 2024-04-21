from typing import List, Optional
from fastapi import FastAPI, Body
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PerFeedback(BaseModel):
    to: str
    rate: int
    good_comment: str
    bad_comment: str


class Feedback(BaseModel):
    user: str
    time: str
    #feedbacks: List[PerFeedback]


@app.get('/engineers')
async def get_engineers():
    return [
        '张三',
        '李四',
    ]


# @app.post('/feedbacks')
# async def post_feedback(feedback: Feedback):
#     return 'Received feedbacks from {}'.format(feedback.user)



@app.post('/feedbacks')
async def post_feedback():
    return 'Received feedbacks'

@app.get('/')
async def root():
    return {'message': 'Hello World'}