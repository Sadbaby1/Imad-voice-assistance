import json
import os
import subprocess
from agent import *
from schema import *


# calling (runing) the tool
def run_tool(tool_call):
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    print(f"Model wants to run tool: {name}({args})")
    try:
        return str(TOOLS[name](**args))
    except Exception as error:
        return f"Error: {error}"


# One run of our AI agent. --> run each time the user sens a prompte
def run_agent(messages):
    # loop that handle one loop give to the model
    while True:
        # generate response from the AI agent
        response = client.chat.completions.create(
            model=MODEL, messages=messages, tools=TOOL_SCHEMAS
        )
        message = response.choices[0].message
        messages.append(message)

        # no tool calls mean the model is done and gave us a normal answer
        if not message.tool_calls:
            print(message.content)
            break

        for tool_call in message.tool_calls:
            result = run_tool(tool_call)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                }
            )
