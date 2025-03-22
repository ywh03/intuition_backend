from langchain_core.documents import Document
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chat_models import init_chat_model

llm = init_chat_model("gpt-4o-mini",model_provider="openai")

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_store = FAISS.load_local("ADKAR_faiss_index", embeddings, allow_dangerous_deserialization=True)
#vector_store.add_documents(all_splits)

#vector_store.save_local("faiss_index")
print("Total vectors:", vector_store.index.ntotal)
# Define prompt for question-answering
prompt = PromptTemplate.from_template("""
You are supposed to use a requested management model to solve a problem using the ADKAR model.  Using the following knowledge of each step in the model, recommend a comprehensive solution and spell out each step. 
If unsure, reply "I don't know".

Context:
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


graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()

response = graph.invoke({"question": "Solve the problem of motivating employees to be early"})
print(response["answer"].content)
print(response["context"])