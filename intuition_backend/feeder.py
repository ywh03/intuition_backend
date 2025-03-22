from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chat_models import init_chat_model

docs = ("Advantages of Lewin's Model A Foundational Approach: Lewin's model lays the groundwork for many subsequent theories and models in change management. Its basic principles are applicable across a wide range of change initiatives, making it a versatile tool in the change manager's toolkit. " +
        "Ease of Application: The clarity and simplicity of the model make it easily adaptable to various contexts. Organizations can use it to guide the planning and implementation of change initiatives, offering a step-by-step structure that is easy to follow and execute. " +
        "Limitations of Lewin's Model Potential for Oversimplification: Lewin’s model simplified approach can also be its’ shortcoming. Modern organizations face complex, ever-evolving landscapes that may require more iterative and flexible approaches to change. The linear progression suggested by Lewin might not fully capture the nuances of implementing change in today’s dynamic environments." +
        "Need for More Emphasis on Sustaining Change: While Lewin’s model effectively addresses the need to solidify changes through its Refreeze stage, it could offer more in terms of strategies for maintaining and reinforcing these changes over the long term. The modern business environment, characterized by continuous change, challenges the notion of refreezing, suggesting that a more fluid approach to embedding and sustaining change might be necessary.  "+
        "Advantages of the ADKAR Model Personalized Approach: The strength of the ADKAR Model lies in its ability to address the unique responses to change of everyone, fostering an environment where personal barriers to change are acknowledged and managed. This tailored approach enhances the likelihood of each person reaching their change milestones successfully."+
        "Comprehensive Coverage: By covering the full spectrum of the change process, from awareness to reinforcement, the ADKAR Model ensures no aspect of the individual's journey is overlooked. This thoroughness helps in building a solid foundation for sustained change. "+
        "Demands Significant Resources: Implementing a personalized change management strategy can be resource intensive. Organizations may find the requirement for individual assessments, tailored communication, and support strategies challenging, particularly for large-scale change initiatives."+
        "Potential for Oversight: While focusing on individual change is crucial, there's a risk that the broader organizational context might be under emphasized. Successful organizational change also requires attention to systemic factors, cultural dynamics, and structural adjustments that might not be fully addressed by concentrating on individual change alone. ")

docs = [Document(page_content=docs, metadata={"source": "Lewin's Guide"})]

llm = init_chat_model("gpt-4o-mini",model_provider="openai")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
all_splits = text_splitter.split_documents(docs)


embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


vector_store = FAISS.from_documents(all_splits,embedding=embeddings)
vector_store.save_local("framework_decider_index")
print("Total vectors:", vector_store.index.ntotal)
