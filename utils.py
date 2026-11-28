import json
from agent import client, MODEL
from datetime import datetime
import re  # for qwen model, to be remove in case of aorder model
from schema import TOOL_SCHEMAS
from tools import TOOLS

MAX_STEPS = 5  # stop the model from calling tools forever
LOG_FILE = "test_log.jsonl"


def log_event(kind, data):
    """Append one line per event, used later for your test results table."""
    entry = {"time": datetime.now().isoformat(timespec="seconds"), "kind": kind, **data}
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def run_tool(tool_call):
    """Run one tool the model asked for and return the result as text."""
    name = tool_call.function.name

    try:
        args = json.loads(tool_call.function.arguments or "{}")
    except json.JSONDecodeError:
        return "Error: the tool arguments were not valid JSON."

    if name not in TOOLS:
        return f"Error: unknown tool '{name}'."

    print(f"[tool] {name}({args})")
    try:
        result = str(TOOLS[name](**args))
    except Exception as error:
        result = f"Error: {error}"

    log_event("tool", {"name": name, "args": args, "result": result})
    return result


def run_agent(messages):
    """Handle one user turn. Returns the assistant's final text reply."""
    for _ in range(MAX_STEPS):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOL_SCHEMAS,
        )
        message = response.choices[0].message
        messages.append(message)

        # No tool calls means the model gave a normal answer, so we are done
        if not message.tool_calls:
            reply = message.content or ""
            """
            reply = re.sub(
                r"<think>.*?</think>", "", reply, flags=re.DOTALL
            ).strip()  # turn off think for qwen3 model : to be remove for order model
            
            """
            log_event("reply", {"model": MODEL, "reply": reply})
            return reply

        # Otherwise run each requested tool and send the results back to the model
        for tool_call in message.tool_calls:
            result = run_tool(tool_call)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                }
            )

    return "Sorry, I could not finish that. Could you try again?"
