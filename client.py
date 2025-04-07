import requests

API_URL = "http://localhost:8000/api/code/ask"


def load_pr():
    owner = input("GitHub owner: ").strip()
    repo = input("GitHub repo: ").strip()
    pr_number = input("Pull Request number: ").strip()

    try:
        payload = {"owner": owner, "repo": repo, "pr_number": int(pr_number)}
        response = requests.post("http://localhost:8000/api/code/load_pr", json=payload)
        response.raise_for_status()
        print(f"✅ PR loaded from {response.json()['repo_path']}")
    except Exception as e:
        print(f"❌ Failed to load PR: {e}")


def main():
    print("🤖 Simple Ask Client")
    print("   Type `load` to load a PR")
    print("   Type `review` to request a code review")
    print("   Type `exit` to quit\n")

    while True:
        command = input("You: ").strip()
        if command.lower() in ("exit", "quit"):
            print("👋 Bye!")
            break
        elif command.lower() == "load":
            load_pr()
            continue

        elif command.lower() == "review":
            try:
                response = requests.post(
                    "http://localhost:8000/api/code/review_pr",
                    json={
                        "question": "Please review this pull request in the context of the existing codebase"
                    },
                )
                response.raise_for_status()
                print(f"\n--- CODE REVIEW ---\n{response.json()['review'].content}\n")
            except Exception as e:
                print(f"❌ Review failed: {e}")
            continue

        try:
            response = requests.post(API_URL, json={"question": command})
            response.raise_for_status()
            print(f"AI: {response.json()['answer']}\n")
        except Exception as e:
            print(f"❌ Request failed: {e}")


if __name__ == "__main__":
    main()
