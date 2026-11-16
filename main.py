import subprocess
import platform

def get_cpu_info():
    """Get CPU information safely."""
    try:
        result = subprocess.run(
            ["lscpu"],
            capture_output=True,
            text=True,
            timeout=5,
            check=True
        )
        return result.stdout
    except Exception as error:
        return f"Could not read CPU information: {error}"


def get_memory_info():
    """Get memory information safely."""
    try:
        result = subprocess.run(
            ["free", "-h"],
            capture_output=True,
            text=True,
            timeout=5,
            check=True
        )
        return result.stdout
    except Exception as error:
        return f"Could not read memory information: {error}"


def get_disk_info():
    """Get disk information safely."""
    try:
        result = subprocess.run(
            ["lsblk", "-o", "NAME,SIZE,TYPE,MOUNTPOINT"],
            capture_output=True,
            text=True,
            timeout=5,
            check=True
        )
        return result.stdout
    except Exception as error:
        return f"Could not read disk information: {error}"


def answer_question(question):
    question = question.lower()

    if "cpu" in question or "processor" in question:
        return get_cpu_info()

    elif "ram" in question or "memory" in question:
        return get_memory_info()

    elif "disk" in question or "ssd" in question or "storage" in question:
        return get_disk_info()

    elif "system" in question or "linux" in question:
        return platform.platform()

    else:
        return (
            "Sorry, I cannot answer that question yet.\n"
            "Try asking about CPU, RAM, disk, or Linux system."
        )


def main():
    print("=" * 50)
    print("       HARDWARE Q&A ASSISTANT")
    print("=" * 50)
    print("Ask questions about your computer.")
    print("Type 'exit' to close the assistant.")

    while True:
        question = input("\nYou: ").strip()

        if question.lower() == "exit":
            print("Assistant: Goodbye!")
            break

        if not question:
            print("Assistant: Please enter a question.")
            continue

        answer = answer_question(question)
        print("\nAssistant:")
        print(answer)


if __name__ == "__main__":
    main()