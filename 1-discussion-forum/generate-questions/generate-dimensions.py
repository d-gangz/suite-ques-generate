from langchain_google_vertexai import ChatVertexAI
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatVertexAI(model="gemini-2.5-pro")

system_prompt = SystemMessage(
    content="You are a helpful assistant that generates dimensions for a given question."
)

llm.invoke(system_prompt)
