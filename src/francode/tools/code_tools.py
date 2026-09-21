import os
import subprocess
from pathlib import Path


def bash(command: str) -> dict:
    result = subprocess.run(args=command, shell=True, text=True, timeout=30)
    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "exit_code": result.returncode,
    }


def list_files(path: str):
    return os.listdir(path)


def read_file(path: str):
    content = ""
    with open(path, "r") as f:
        for line in f:
            content += line + "\n"
    return content


def write_file(path: str, content: str):
    with open(path, "w") as f:
        f.write(content)


def create_directory(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)


def create_react_app(name: str):
    bash("pnpm create vite@latest -y")
