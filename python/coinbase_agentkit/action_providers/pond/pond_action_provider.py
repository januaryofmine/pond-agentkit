"""Pond AI action provider"""

import os
import json
import requests 
from typing import Optional, Any
# from coinbase_agentkit.types import ActionProvider, ActionInput, ActionOutput
from coinbase_agentkit.network import Network
from .schemas import BaseWalletSummarySchema
from ..action_decorator import create_action

from coinbase_agentkit.action_providers.action_provider import ActionProvider
from coinbase_agentkit.types import ActionInput, ActionOutput

class PondActionProvider(ActionProvider):
    """Action provider for interacting with POND AI AGENTS."""

    POND_API_URL = "https://broker-service.private.cryptopond.xyz/predict"
    DURATION_MODEL_MAP = {
        1: 16,
        3: 17,
        6: 18,
        12: 19
    }

    def __init__(self, api_url: str, api_key: str):
        super().__init__(name="pond_ai", action_providers=[])  #
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

    @create_action(
        name="base_wallet_summary",
        description="""
This tool summarizes the activity of a Base address over a given period. It takes:

- address: The Ethereum Base address to summarize
- duration_months: One of [1, 3, 6, 12] (in months)

The summary includes token flows, transaction behavior, and interaction patterns.
""",
        schema=BaseWalletSummarySchema,
    )
    def get_base_wallet_summary(self, args: dict[str, Any]) -> str:
        """Fetches a wallet summary for a Base address over a specified duration in months."""
        try:
            validated_args = BaseWalletSummarySchema(**args)

            if validated_args.duration_months not in self.DURATION_MODEL_MAP:
                return "Error: duration_months must be one of [1, 3, 6, 12]."

            model_id = self.DURATION_MODEL_MAP[validated_args.duration_months]

            headers = {
                'Content-Type': 'application/json',
                'Authorization': self.api_key
            }
            payload = {
                "model_id": model_id,
                "input_keys": [validated_args.address]
            }

            response = requests.post(self.POND_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

            if data.get("code") == 200 and data.get("data"):
                result = data["data"][0]
                address = result.get("input_key", "N/A")
                updated_at = result.get("debug_info", {}).get("UPDATED_AT", "N/A")
                analysis = result.get("analysis_result", {})

                summary_lines = [f"Wallet Address: {address}",
                                f"Summary Duration: {validated_args.duration_months} months",
                                f"Feature Updated At: {updated_at}",
                                "",
                                "Key Metrics:"]
                for key, val in analysis.items():
                    pretty_key = key.replace("BASE_", "").replace("_FOR_360DAYS", "").replace("_USER_", " ").replace("_", " ").title()
                    summary_lines.append(f"- {pretty_key}: {val}")

                return "\n".join(summary_lines)
            else:
                return f"Error: Unexpected API response: {data}"

        except requests.exceptions.RequestException as e:
            return f"Error: Failed to connect to POND API: {str(e)}"
        except json.JSONDecodeError as e:
            return f"Error: Invalid JSON response from POND API: {str(e)}"
        except Exception as e:
            return f"Error: Unexpected failure while fetching wallet summary: {str(e)}"

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
