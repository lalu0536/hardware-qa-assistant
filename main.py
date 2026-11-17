import subprocess
import platform
import shutil

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Hardware Q&A Assistant",
    description="Ask questions about CPU, RAM, disk and Linux system information."
)


class Question(BaseModel):
    question: str


def run_command(command):
    """Run only predefined, safe system commands."""
    if shutil.which(command[0]) is None:
        return f"{command[0]} command is not available on this server."

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=5,
            check=True
        )
        return result.stdout
    except Exception as error:
        return f"Could not read information: {error}"


def get_cpu_info():
    return run_command(["lscpu"])


def get_memory_info():
    return run_command(["free", "-h"])


def get_disk_info():
    return run_command(
        ["lsblk", "-o", "NAME,SIZE,TYPE,MOUNTPOINT"]
    )


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

    return (
        "Sorry, I cannot answer that question yet. "
        "Try asking about CPU, RAM, disk, or Linux system."
    )


@app.get("/")
def home():
    return {
        "message": "Hardware Q&A Assistant is running!",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/ask")
def ask_question(data: Question):
    if not data.question.strip():
        return {"answer": "Please enter a question."}

    return {
        "question": data.question,
        "answer": answer_question(data.question)
    }






   

   
