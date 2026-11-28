from agent import build_system_prompt
from utils import run_agent, log_event


def main():
    # One system message at the start, then the conversation grows from here
    messages = [{"role": "system", "content": build_system_prompt()}]

    print(f"Mini agent ready. Type 'exit' to quit.")

    # loop for the user to keep prompting the model
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ("exit", "quit"):
            break

        messages.append({"role": "user", "content": user_input})
        log_event("user", {"text": user_input})

        try:
            reply = run_agent(messages)
        except Exception as error:
            # Never crash during a demo: show a friendly message instead
            print(f"\n[error] {error}\n")
            continue

        print(f"\nAssistant: {reply}\n")


if __name__ == "__main__":
    main()
