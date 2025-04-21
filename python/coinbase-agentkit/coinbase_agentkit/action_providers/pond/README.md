# Pond AI Action Provider

This directory contains the **PondActionProvider**, a unified integration that connects Coinbase AgentKit to a growing suite of AI agents hosted by the Pond platform (https://cryptopond.xyz/).

Through a centralized backend gateway, the provider routes free-form user prompts to the appropriate Pond AI agent.

## Directory Structure

```
pond/
├── pond_action_provider.py       # Main provider logic
├── __init__.py                   # Package exports
└── README.md                     # This file

# From python/coinbase-agentkit/
examples/
├── pond_ai_demo.py               # Example usage script
```

---

## Overview

The PondActionProvider is designed to:

- Accept free-text user prompts from AgentKit
- Route them to the correct AI agent (smart contracts, token safety, wallet analysis, etc.)
- Return responses via a single integration endpoint

Routing, classification, and security enforcement happen server-side via Pond's gateway.

---

## Setup

To use the Pond AI provider:

```python
from coinbase_agentkit.action_providers.pond import pond_action_provider

# With environment variables
provider = pond_action_provider()

# Or with explicit configuration
provider = pond_action_provider(
    api_url="pond_ai_agents_gateway",
    api_key="your-user-api-key"
)
```

Set the following environment variables to use the default configuration:

```bash
POND_AI_API_URL=pond_ai_agents_gateway
POND_AI_API_KEY=your-user-api-key
```

---

## Routing Logic

All prompt classification and agent routing is handled by the Pond backend.  
Supported categories currently include (but are not limited to):

- Smart contract summarization
- Token safety and volatility analysis
- Wallet summaries and transaction insights
- Base ecosystem tooling
- General blockchain FAQs

As new agents are added, they are automatically supported without requiring changes to the AgentKit integration.

---

## Notes

- The provider makes no assumptions about the underlying AI models.
- All classification, logging, and intent-to-agent mapping happens via the Pond.
- For more information about Pond, visit [https://cryptopond.xyz/](https://cryptopond.xyz/) or contact the Pond team.
