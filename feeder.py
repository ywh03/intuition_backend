import bs4
import os
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chat_models import init_chat_model

# Load and chunk contents of the blog
loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2024-11-28-reward-hacking/",),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title", "post-header")
        )
    ),
)

docs = ("Stage 1 – Unfreeze The first stage in Lewin’s model deals with perception management and aims to prepare the affected stakeholders for the upcoming organizational change. Change leaders must look at ways to improve the company’s preparedness for change and create a sense of urgency similar to Kotter’s change model."+
        "During this stage, effective change communication is vital in getting the desired team members buy-in and support of the people in the change management."+
        "Conduct a business process analysis to understand the current loopholes in the business processes Obtain organizational buy-in Create a strategic change vision and change strategy Communicate in a compelling way about why change has to occur Address employee concerns with honesty and transparency"+
        "Stage 2 – Change Once the status quo is disrupted, this stage deals with implementing change. To smoothen the transition, you must consider an agile and iterative approach that incorporates employee feedback. You can further look at the following actionable items to keep uncertainty at bay:"+
        "Ensure a continuous flow of information to obtain the support of your team members Organize change management workshops and sessions for change management exercises Empower employees to deal with the change proactively Generate easy wins as visible results will motivate your team"+
        "Stage 3 – Refreeze Employees move from the transition phase towards stabilization or acceptance in the final’ refreezing’ stage. However, if change leaders fail to reinforce the change in organizational culture, employees might revert to previous behaviors. The following activities will help you support the change."+
        "Identify and reward early adopters and change champions Collect employee feedback regularly Offer on-demand employee training and support Explore digital adoption platforms (DAP) such as Whatfix to be your partner in change with intuitive features such as interactive walkthroughs, customizable popups, and multi-format self-help content")


#llm = HuggingFaceEndpoint(
#    repo_id="tiiuae/falcon-7b-instruct",
#    task="text-generation",
#    max_new_tokens=512
#)

docs = [Document(page_content=docs, metadata={"source": "Lewin's Guide"})]

llm = init_chat_model("gpt-4o-mini",model_provider="openai")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
all_splits = text_splitter.split_documents(docs)



embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

#vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

#vector_store.add_documents(all_splits)

vector_store = FAISS.from_documents(all_splits,embedding=embeddings)
vector_store.save_local("lewins_faiss_index")
print("Total vectors:", vector_store.index.ntotal)
# Define prompt for question-answering
prompt = hub.pull("rlm/rag-prompt")


# Define state for application
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


# Define application steps
def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"], k=5)
    return {"context": retrieved_docs}


def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response}


# Compile application and test
graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()

response = graph.invoke({"question": "What is the second step of the AKDAR model"})
print(response["answer"].content)
print(response["context"])