import json
import os
import subprocess
from utils import *
from schema import *
from tools import *

# keeep track of message list
messages = []

# list of tools available to the model
TOOLS = {
    "list_files": list_files,
    "read_file": read_file,
    "write_file": write_file,
    "run_shell_command": run_shell_command,
}


def main():
    massages.append({"role": "system", "content": SYSTEM_PROMPT})
    print(f"Mini agent ready. Type 'exit' to quit.")

    # loop for the user to keep prompting the model
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ("exit", "quit"):
            break

        massages.append({"role": "user", "content": user_input})

        reply = run_agent(massages)
        print(f"\nAgent: {reply}")


if __name__ == "__main__":
    main()
