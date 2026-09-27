from src.langgraphagenticai.state.state import State

class ChatbotWithToolNode:
    def __init__(self,model):
        self.llm = model

    def process(self,state:State) -> dict:
        """
        Processes the input state and generates response wit tool integration.
        """

        user_input = state["messages"][-1] if state["messages"] else ""
        llm_response = self.llm.invoke([{"role":"user", "content": user_input}])

        #Stimulate tool-specific logic
        tools_reponse = f"Tool integration for: '{user_input}'"

        return {"messages":[llm_response,tools_reponse]}
    

    def create_chatbot(self, tools):
        """
        REturn a chatbot node function
        """

        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state:State):
            """
            Chatbot logic for processing input state and returning a response
            """
            return {"messages": [llm_with_tools.invoke(state["messages"])]}
        return chatbot_node  
        
    