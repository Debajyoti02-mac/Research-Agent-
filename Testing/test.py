from Graph.graph import graph
question = "What is the Full form of LLM?"
result = graph.invoke({'query':question , 'retry':0})
if __name__ == '__main__':
    print(f'answer : \n {result['answer'].content}')