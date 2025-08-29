import os 
import google.generativeai as genai
from dotenv import load_dotenv

import json

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def getWeather(city):
    """
    Simulates fetching weather data for a given city.
    In a real application, this would call a weather API.
    """
    return "10 degree c "

available_tools = {
    "getWeather" : getWeather
}


SYSTEM_PROMPT = """ You are a helpful AI assistant , who is specialized in solving the queries of the user .

You work on start , plan , action and observe mode.
For the given user query and available tools , plan the step by step execution, based on the planning
select the best tool to execute the task from the avaiable tools ,and based on the tool selection
you perform an action to call the tool 

Wait for the observation and based on the observation from the tool call resolve the user query.

Rules to follow :

-follow the Output JSON format.
-Always perform one step at a time and wait for the next input.
-Carefully analyse the user query.

Available tools:
-"getWeather" - This function takes the city name as an input and based on that it return the current weather of that city.

Output JSON Format : 
{{
    "step":"string",
    "content":"string",
    "function":"The name of function if the step is action",
    "input" : "The input parameter of the function",

}}

Example :
User Query: What is the weather of Bhopal?

Output :{{"step" : "plan" , "content" : "The user is interested in weather data of Bhopal"}}
Output :{{"step" : "plan" , "content" : "From the available tools I should call the getWeather tool"}}
Output :{{"step" : "action" , "function" : "getWeather" , "input":"Bhopal"}}
Output :{{"step" : "observe" , "output" : "12 degree c"}}
Output : {{"step" : "output" , "content" : "The weather of Bhopal seems to be 12 degree c"}}
"""
model = genai.GenerativeModel("gemini-1.5-flash")

messages = [
    {"role": "assistant", "parts": [{"text": SYSTEM_PROMPT}]}
]
query = input("> ")
messages.append({"role" : "user" , "parts" : [{"text": query}]})

while True:
    response = model.generate_content(messages)
    
    # Append the actual response text to the conversation history.
    messages.append({"role": "assistant" , "parts" : [{"text": response.text}]})
    
    try:
        parsed_response = json.loads(response.text)
    except json.JSONDecodeError:
        print("Error: The model did not return valid JSON. Retrying...")
        continue

    step = parsed_response.get("step")
    content = parsed_response.get("content")

    if step == "plan":
        print(f"🧠 Planning: {content}")
        continue
    
    elif step == "action":
        # Corrected the typo from "funciton" to "function".
        tool_name = parsed_response.get("function")
        tool_input = parsed_response.get("input")

        print(f"🔨 Action: Calling tool '{tool_name}' with input '{tool_input}'")

        # More robust check to see if the tool exists.
        if tool_name in available_tools:
            output = available_tools[tool_name](tool_input)
            
            # The observation should come from the assistant.
            messages.append({"role" : "assistant" , "parts" : [{"text" : json.dumps({"step" : "observe" , "output" : output})}]})
            continue
        else:
            print(f"Error: Tool '{tool_name}' not found.")
            break
            
    elif step == "output":
        print(f"🤖 Final Answer: {content}")
        break

    else:
        print(f"Error: Unknown step type '{step}'.")
        break