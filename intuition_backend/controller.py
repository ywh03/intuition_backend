from Framework_wrapper import gen_response
from ADKAR_wrapper import gen_response_adkar
from Lewin_wrapper import gen_response_lewin
from fastapi import FastAPI, Request
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

class Query(BaseModel):
    question: str

@app.post("/decide-framework")
def decide_framework(query: Query):
    model = ''
    question = query.question
    answer = ''
    justification = ''

    if model == '':
        res = gen_response(question)
        model = res['answer']
        justification = res['justification']

    if model == 'ADKAR':
        answer = gen_response_adkar(question)
    elif model == 'Lewin':
        answer = gen_response_lewin(question)
    return {
        "model": model,
        "answer": answer,
        "justification": justification
    }

""""
model = ''
question = 'Solve the problem of motivating employees to adopt Artificial Intelligence'
answer = ''
justification = ''

if model == '':
    res = gen_response(question)
    model = res['answer']
    justification = res['justification']

if model == 'ADKAR':
    answer = gen_response_adkar(question)
elif model == 'Lewin':
    answer = gen_response_lewin(question)

print(justification)
print(answer)

"""

