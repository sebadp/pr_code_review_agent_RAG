import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral"

def ask_ollama(prompt: str) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    print("📤 Sending to Ollama...")
    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    result = response.json()
    print("📥 Response from Ollama received.")
    return result["response"]

if __name__ == "__main__":
    print("🤖 Ping Ollama test (type 'exit' to quit)\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("👋 Bye!")
            break

        try:
            reply = ask_ollama(user_input)
            print(f"AI: {reply}\n")
        except Exception as e:
            print(f"❌ Error: {e}")

