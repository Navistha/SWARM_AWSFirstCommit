# policy_engine.py
from dataclasses import dataclass
from agents import Verdict, AgentVote


@dataclass
class PolicyDecision:
    merge_blocked: bool
    blocking_reason: str | None
    suggestions: list[str]

    def to_dict(self):
        return {
            "merge_blocked": self.merge_blocked,
            "blocking_reason": self.blocking_reason,
            "suggestions": self.suggestions,
        }


def decide(votes: list[AgentVote]) -> PolicyDecision:
    """Only SecurityReviewer's BLOCK vote can ever stop a merge.
    Style/Structure can only ever be SUGGESTION or PASS (enforced in their
    own system prompts too), so we don't even need to check for BLOCK there."""
    security_vote = next(v for v in votes if v.agent_name == "SecurityReviewer")
    other_votes = [v for v in votes if v.agent_name != "SecurityReviewer"]

    merge_blocked = security_vote.verdict == Verdict.BLOCK
    blocking_reason = security_vote.reasoning if merge_blocked else None

    suggestions = [
        v.reasoning for v in other_votes if v.verdict == Verdict.SUGGESTION
    ]

    return PolicyDecision(merge_blocked, blocking_reason, suggestions)