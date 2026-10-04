from research_agent.graph import graph
question = "What is sales?"
result = graph.invoke({'query':question , 'retry':0})
result['answer']