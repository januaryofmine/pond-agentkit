"""Pond AI action provider"""

import os
import json
import requests 
from typing import Optional
from coinbase_agentkit.types import ActionProvider, ActionInput, ActionOutput
from coinbase_agentkit.network import Network


class PondActionProvider(ActionProvider):
    """Action provider for interacting with POND AI AGENTS."""

    def __init__(self, api_url: str, api_key: str | None = None):
        super().__init__("pond_ai", tools=[])
        self.api_url = api_url
        self.api_key = api_key

    def supports_network(self, network: Network) -> bool:
        return True

    def invoke(self, input: ActionInput) -> ActionOutput:
        try:
            prompt = input.input

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "query": prompt,
                "user": "agentkit",  # Optional: to track source
            }

            response = requests.post(
                self.api_url,
                headers=headers,
                data=json.dumps(payload),
                timeout=30
            )
            response.raise_for_status()

            result = response.json()
            return ActionOutput(output=result.get("answer", "[POND] No response returned."))

        except requests.exceptions.RequestException as e:
            return ActionOutput(output=f"[POND ERROR] {str(e)}")
        except Exception as e:
            return ActionOutput(output=f"[POND ERROR] Unexpected failure: {str(e)}")


def pond_action_provider(
    api_url: Optional[str] = None,
    api_key: Optional[str] = None,
) -> PondActionProvider:
    """
    Factory for PondActionProvider. You can set:
    - api_url: Your gateway endpoint
    - api_key: API key issued to developers
    """
    api_url = api_url or os.getenv("POND_AI_API_URL")
    api_key = api_key or os.getenv("POND_AI_API_KEY")

    if not api_url or not api_key:
        raise ValueError("Missing POND_AI_API_URL or POND_AI_API_KEY")

    return PondActionProvider(api_url=api_url, api_key=api_key)
