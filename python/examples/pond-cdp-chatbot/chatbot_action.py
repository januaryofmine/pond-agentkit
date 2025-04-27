from coinbase_agentkit.action_providers.pond.pond_action_provider import pond_action_provider

try:
    provider = pond_action_provider()

    args = {
        "address": "0x4200000000000000000000000000000000000006",  # Base WETH address
        "duration_months": 3
    }

    response = provider.get_base_wallet_summary(args)

    print("\n🧠 Structured Action Response:")
    print(response)
except ValueError as e:
    print(f"Error: {e}")
    print("Please ensure POND_AI_API_URL and POND_AI_API_KEY environment variables are set.")
except Exception as e:
    print(f"Unexpected error: {e}")
