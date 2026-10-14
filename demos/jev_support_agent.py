"""Support-ticket agent demo: OpenRouter orchestrates, Jev evaluates, code acts.

The default mode is completely offline and uses recorded Jev answers.  For live
experiments install the provider extras, set OPENROUTER_API_KEY and
TYPESAFE_API_KEY, then use --live-openrouter and/or --live-jev.
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Protocol


ROOT = Path(__file__).parent
FIXTURE_PATH = ROOT / "fixtures" / "jev_responses.json"


@dataclass(frozen=True)
class Transaction:
    transaction_id: str
    description: str
    amount: float
    duplicate_of: str | None = None


CUSTOMER = {
    "demo-customer-001": {
        "customer_id": "demo-customer-001",
        "name": "Alex Example",
        "plan": "Pro",
    }
}

TRANSACTIONS = {
    "demo-customer-001": [
        Transaction("txn-100", "Pro subscription", 49.99),
        Transaction("txn-101", "Pro subscription duplicate", 49.99, "txn-100"),
    ]
}

TICKETS = {
    "A": "I was billed twice this month. Please refund the duplicate charge.",
    "B": "My export fails and I need the file for a meeting in 30 minutes.",
    "C": "I cannot sign in after changing my phone, and I also want to cancel.",
}


class DecisionProvider(Protocol):
    def assess(self, ticket: str, evidence: dict[str, Any]) -> dict[str, Any]:
        ...


class RecordedJev:
    """Deterministic replay provider for teaching and video recording."""

    def __init__(self, path: Path = FIXTURE_PATH) -> None:
        self.answers = json.loads(path.read_text())

    def assess(self, ticket: str, evidence: dict[str, Any]) -> dict[str, Any]:
        del evidence
        for key, value in TICKETS.items():
            if value == ticket:
                result = self.answers[key]
                print(f"[Jev: recorded fixture for ticket {key}]")
                return result
        raise ValueError("No recorded Jev response exists for this ticket")


class LiveJev:
    """Adapter for the documented TypeSafe Python SDK."""

    def __init__(self) -> None:
        from typesafe_sdk import Choice, Noul, TypeSafeClient

        self.Choice = Choice
        self.Noul = Noul
        self.TypeSafeClient = TypeSafeClient

    def assess(self, ticket: str, evidence: dict[str, Any]) -> dict[str, Any]:
        state = {"ticket": ticket, "evidence": evidence}
        with self.TypeSafeClient(model="jev-latest") as client:
            response = client.system_one(
                state=state,
                questions={
                    "route": self.Choice(
                        instructions="Which support team should own this ticket?",
                        criteria={
                            "billing": "Payment or subscription issues",
                            "technical": "Bugs, exports, or integration problems",
                            "account": "Sign-in, profile, or cancellation issues",
                            "other": "No listed team clearly fits",
                        },
                    ),
                    "urgent": self.Noul(
                        instructions=(
                            "Is this urgent under the policy: a service interruption "
                            "or a time-bound business deadline?"
                        )
                    ),
                    "refund_eligible": self.Noul(
                        instructions=(
                            "Is there verified evidence of a duplicate charge "
                            "eligible for refund under the policy?"
                        )
                    ),
                },
            )
        result = {
            "route": _to_json(response.choices["route"]),
            "urgent": _to_json(response.nouls["urgent"]),
            "refund_eligible": _to_json(response.nouls["refund_eligible"]),
        }
        print("[Jev: live response]")
        print(json.dumps(result, indent=2))
        return result


def _to_json(value: Any) -> dict[str, Any]:
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if hasattr(value, "__dict__"):
        return {
            key: item
            for key, item in vars(value).items()
            if not key.startswith("_")
        }
    return {"value": value}


def get_customer(customer_id: str) -> dict[str, Any]:
    customer = CUSTOMER.get(customer_id)
    if customer is None:
        raise ValueError(f"Unknown customer: {customer_id}")
    return customer


def lookup_recent_transactions(customer_id: str) -> list[dict[str, Any]]:
    get_customer(customer_id)
    return [asdict(transaction) for transaction in TRANSACTIONS[customer_id]]


def find_duplicate(transactions: list[dict[str, Any]]) -> dict[str, Any] | None:
    return next(
        (transaction for transaction in transactions if transaction["duplicate_of"]),
        None,
    )


def create_support_ticket(route: str, priority: str, reason: str) -> dict[str, Any]:
    return {
        "action": "create_support_ticket",
        "ticket_id": "support-demo-001",
        "route": route,
        "priority": priority,
        "reason": reason,
    }


def request_human_review(reason: str, evidence: dict[str, Any]) -> dict[str, Any]:
    return {
        "action": "human_review",
        "reason": reason,
        "evidence": evidence,
    }


def issue_refund(transaction_id: str, amount: float) -> dict[str, Any]:
    """Never charges money: this demo tool is intentionally a dry run."""
    return {
        "action": "issue_refund",
        "mode": "dry_run",
        "transaction_id": transaction_id,
        "amount": amount,
    }


def policy_decision(
    result: dict[str, Any], transactions: list[dict[str, Any]]
) -> dict[str, Any]:
    route = result["route"]["choice"]
    route_confidence = result["route"].get("confidence", 0.0)
    urgent = result["urgent"]["noul"]
    refund_eligible = result["refund_eligible"]["noul"]
    duplicate = find_duplicate(transactions)

    if (
        route == "billing"
        and route_confidence >= 0.90
        and refund_eligible >= 0.95
        and duplicate is not None
    ):
        return issue_refund(duplicate["transaction_id"], duplicate["amount"])
    if urgent >= 0.70:
        return create_support_ticket(route, "high", "Urgent under the demo policy")
    return request_human_review(
        "Insufficient confidence or evidence for automatic action",
        {"decision": result, "transactions": transactions},
    )


def offline_agent(ticket_id: str, decisions: DecisionProvider) -> dict[str, Any]:
    ticket = TICKETS[ticket_id]
    customer_id = "demo-customer-001"
    print(f"User: {ticket}")
    print("Agent: I will gather customer and transaction evidence first.")
    customer = get_customer(customer_id)
    transactions = lookup_recent_transactions(customer_id)
    evidence = {"customer": customer, "transactions": transactions}
    print("Tool: lookup_recent_transactions ->", json.dumps(transactions))
    print("Agent: I will ask Jev three separate decision questions.")
    result = decisions.assess(ticket, evidence)
    action = policy_decision(result, transactions)
    print("Policy:", json.dumps(action, indent=2))
    return action


TOOLS: dict[str, Callable[..., Any]] = {
    "get_customer": get_customer,
    "lookup_recent_transactions": lookup_recent_transactions,
    "create_support_ticket": create_support_ticket,
    "request_human_review": request_human_review,
    "issue_refund": issue_refund,
}

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_customer",
            "description": "Get a customer record by ID.",
            "parameters": {
                "type": "object",
                "properties": {"customer_id": {"type": "string"}},
                "required": ["customer_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "lookup_recent_transactions",
            "description": "List recent transactions for a customer.",
            "parameters": {
                "type": "object",
                "properties": {"customer_id": {"type": "string"}},
                "required": ["customer_id"],
            },
        },
    },
]


def openrouter_agent(
    ticket: str,
    decisions: DecisionProvider,
    model: str = "openai/gpt-4o-mini",
) -> str:
    """Run a small OpenAI-compatible tool-calling loop through OpenRouter."""
    import httpx

    messages: list[dict[str, Any]] = [
        {
            "role": "system",
            "content": (
                "You are a support workflow agent. Gather evidence with tools. "
                "Do not approve refunds yourself; after evidence is gathered, "
                "call no more tools and explain that the application policy "
                "will evaluate the typed Jev result."
            ),
        },
        {"role": "user", "content": ticket},
    ]
    headers = {
        "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
        "Content-Type": "application/json",
    }
    tool_implementations: dict[str, Callable[..., Any]] = {
        **TOOLS,
        "jev_assess_ticket": lambda customer_id: _assess_and_apply(
            ticket, customer_id, decisions
        ),
    }
    tool_schemas = [
        *TOOL_SCHEMAS,
        {
            "type": "function",
            "function": {
                "name": "jev_assess_ticket",
                "description": (
                    "Gather verified evidence, ask Jev the typed ticket questions, "
                    "and apply the application policy. Use after evidence tools."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {"customer_id": {"type": "string"}},
                    "required": ["customer_id"],
                },
            },
        },
    ]

    for _ in range(6):
        response = httpx.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json={"model": model, "messages": messages, "tools": tool_schemas},
            timeout=60,
        )
        response.raise_for_status()
        message = response.json()["choices"][0]["message"]
        messages.append(message)
        calls = message.get("tool_calls", [])
        if not calls:
            return message.get("content", "")
        for call in calls:
            name = call["function"]["name"]
            arguments = json.loads(call["function"]["arguments"])
            if name not in tool_implementations:
                raise ValueError(f"Unsupported tool requested by model: {name}")
            tool_result = tool_implementations[name](**arguments)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call["id"],
                    "content": json.dumps(tool_result),
                }
            )
    raise RuntimeError("OpenRouter agent exceeded the tool-call limit")


def _assess_and_apply(
    ticket: str, customer_id: str, decisions: DecisionProvider
) -> dict[str, Any]:
    evidence = {
        "customer": get_customer(customer_id),
        "transactions": lookup_recent_transactions(customer_id),
    }
    result = decisions.assess(ticket, evidence)
    action = policy_decision(result, evidence["transactions"])
    return {"jev": result, "policy_action": action}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticket", choices=sorted(TICKETS), default="A")
    parser.add_argument("--live-jev", action="store_true")
    parser.add_argument("--live-openrouter", action="store_true")
    args = parser.parse_args()

    decisions: DecisionProvider = LiveJev() if args.live_jev else RecordedJev()
    if args.live_openrouter:
        print(openrouter_agent(TICKETS[args.ticket], decisions))
    else:
        offline_agent(args.ticket, decisions)


if __name__ == "__main__":
    main()
