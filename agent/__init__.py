"""
PLC Nova AI Agent Package
Интеграция AI-агента с локальными LLM и голосовым вводом.
"""

from agent.main import PLCAgent, Skill, Tool, get_agent, initialize_agent

__all__ = [
    "PLCAgent",
    "Skill",
    "Tool",
    "get_agent",
    "initialize_agent",
]

__version__ = "1.0.0"
