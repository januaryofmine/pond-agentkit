from typing import Any, Dict
from langchain_core.tools import Tool

class ActionProvider:
    """Base class for all action providers."""
    def __init__(self, name: str, tools: list[Tool]):
        self.name = name
        self.tools = tools

class ActionInput:
    """Input for an action."""
    def __init__(self, input: str):
        self.input = input

class ActionOutput:
    """Output for an action."""
    def __init__(self, output: str):
        self.output = output
