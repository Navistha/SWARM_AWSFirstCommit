# orchestrator.py
from agents import ALL_AGENT_CLASSES, AgentVote
from llm_client import get_llm_client
from policy_engine import decide, PolicyDecision


def run_review(code: str, llm_client=None) -> dict:
    """Runs all three reviewers against the code, applies the policy,
    and returns a single JSON-serializable result.

    llm_client is optional — defaults to get_llm_client(), which itself
    respects REVIEW_COMMITTEE_MOCK so you can develop/demo with zero
    network calls, then flip to a real client later without touching
    this file."""
    client = llm_client or get_llm_client()
    votes: list[AgentVote] = []

    for agent_cls in ALL_AGENT_CLASSES:
        agent = agent_cls(client)
        vote = agent.review(code)
        votes.append(vote)

    decision: PolicyDecision = decide(votes)

    return {
        "votes": [v.to_dict() for v in votes],
        "decision": decision.to_dict(),
    }