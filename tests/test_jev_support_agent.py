from demos.jev_support_agent import (
    RecordedJev,
    TICKETS,
    lookup_recent_transactions,
    offline_agent,
    policy_decision,
)


def test_ticket_a_is_a_dry_run_refund() -> None:
    result = offline_agent("A", RecordedJev())
    assert result["action"] == "issue_refund"
    assert result["mode"] == "dry_run"
    assert result["amount"] == 49.99


def test_ticket_b_routes_to_urgent_technical_review() -> None:
    result = offline_agent("B", RecordedJev())
    assert result["action"] == "create_support_ticket"
    assert result["route"] == "technical"
    assert result["priority"] == "high"


def test_ticket_c_is_escalated_when_confidence_is_low() -> None:
    result = offline_agent("C", RecordedJev())
    assert result["action"] == "human_review"


def test_transaction_tool_returns_duplicate_evidence() -> None:
    transactions = lookup_recent_transactions("demo-customer-001")
    assert any(item["duplicate_of"] for item in transactions)


def test_policy_does_not_refund_without_duplicate_evidence() -> None:
    result = RecordedJev().assess(TICKETS["A"], {})
    action = policy_decision(result, [])
    assert action["action"] == "human_review"
