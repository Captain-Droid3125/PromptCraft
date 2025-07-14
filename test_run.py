from generator.langgraph_flow import build_graph, GenerationState

def test():
    prompt = "a logo for Derma Tools"
    flow = build_graph()
    result = flow.invoke(GenerationState({"prompt": prompt}))
    print(result)

if __name__ == "__main__":
    test()
