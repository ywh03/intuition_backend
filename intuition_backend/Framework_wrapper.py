from langchain_core.documents import Document
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chat_models import init_chat_model

llm = init_chat_model("gpt-4o-mini",model_provider="openai")

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_store = FAISS.load_local("framework_decider_index", embeddings, allow_dangerous_deserialization=True)
print("Total vectors:", vector_store.index.ntotal)
prompt = PromptTemplate.from_template("""
You are supposed to choose a management change framework based on the given prompt.  Make your decision based on the research given. 
If unsure, just pick an optimal one.

Firstly, return a one word answer of either 'ADKAR' or 'Lewin'.

Then justify why. 

Research:
{context}

Question:
{question}

Answer:
""")


class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"], k=5)
    return {"context": retrieved_docs}


def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response}


def gen_response(question):
    graph_builder = StateGraph(State).add_sequence([retrieve, generate])
    graph_builder.add_edge(START, "retrieve")
    graph = graph_builder.compile()

    response = graph.invoke({"question": question})
    parts = response["answer"].content.split("Justification:")

    answer = parts[0].replace("Answer:", "").strip()
    justification = parts[1].strip()

    return {'answer': answer, 'justification': justification}