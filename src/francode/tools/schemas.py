from .code_tools import *
from openai.types.responses import FunctionToolParam
from typing import Iterable

TOOL_REGISTERY = {
    "bash": bash,
    "list_files": list_files,
    "read_file": read_file,
    "write_file": write_file,
    "create_directory": create_directory,
    "create_react_app": create_react_app,
}

TOOLS_OPENAI: Iterable[FunctionToolParam]= [
    {
        "type": "function",
        "name": "bash",
        "description": "Ejecuat comandos de bash",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "comando bash a ejecutar",
                }
            },
            "required": ["command"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "list_files",
        "description": "Lists all the files and directories in the selected directory",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "path to the directory to be listed",
                }
            },
            "required": ["path"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "read_file",
        "description": "reads the contents of a file given the filepath",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "path to the file to be read",
                }
            },
            "required": ["path"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "write_file",
        "description": "writes some content provided as argument into a file with path provided also as an argument",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "path to the file to be written",
                },
                "content": {
                    "type": "string",
                    "description": "content to be written in the file",
                },
            },
            "required": ["path", "content"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "create_directory",
        "description": "creates a new directory, can be directory structure providing the path until the child folder",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "path to the folder to be created. Use children path to create directory structure",
                },
            },
            "required": ["path"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "write_file",
        "description": "writes some content provided as argument into a file with path provided also as an argument",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "path to the file to be written",
                },
                "content": {
                    "type": "string",
                    "description": "content to be written in the file",
                },
            },
            "required": ["path", "content"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]
