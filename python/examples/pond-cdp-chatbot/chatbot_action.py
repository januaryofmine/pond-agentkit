from coinbase_agentkit.action_providers.pond import pond_action_provider

provider = pond_action_provider()

args = {
    "address": "0xabc123abc123abc123abc123abc123abc123abc1",  # use a valid address
    "duration_months": 3
}

response = provider.get_base_wallet_summary(args)

print("\n🧠 Structured Action Response:")
print(response)
