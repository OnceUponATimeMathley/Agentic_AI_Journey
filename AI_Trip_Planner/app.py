from fastapi import FastAPI
from pydantic import BaseModel
from agent.agentic_workflow import GraphBuilder
import os

app = FastAPI()


class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    try:
        print(query)
        graph = GraphBuilder(model_provider="alibaba")
        react_app = graph()
        #react_app = graph.build_graph()

        png_graph = react_app.get_graph().draw_mermaid_png()
        with open("my_graph.png", "wb") as f:
            f.write(png_graph)
        
        print(f"Graph save as 'my_graph.png' in {os.getcwd()}")
        # Assuming request is a pydantic object like {"question": "your text"}
        messages = {"messages": [query.question]}
        output = react_app.invoke(messages)

        # If the result is dict with messages
        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content # Last AI response
        else:
            final_output = str(output)
