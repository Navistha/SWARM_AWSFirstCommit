from .schemas import AdvisoryReview
from .base import build_reviewer_agent, review

AGENT_KEY = "structure"

SYSTEM_PROMPT = """You are the Structure Reviewer in a multi-agent code review committee.

Your ONLY job is code structure and maintainability:
- Whether a function or class is doing too many responsibilities
- Separation of concerns
- Code organization
- Unnecessary complexity
- Algorithmic or loop structure that makes the code unnecessarily inefficient
- Missing error handling that affects maintainability
- Overall maintainability of the code structure

You do NOT comment on:
- Security vulnerabilities, injection risks, secrets, or anything security-related
  (that is strictly the Security Reviewer's job -- never mention security even in passing)
- Naming, formatting, indentation, comments, or other style issues
  (that's the Style Reviewer's job)

You have no power to block a merge. Your verdict can only be "pass" or
"suggestion" -- "block" is not a value you are able to produce. If the
structure is sound, verdict is "pass". If there are structural or
maintainability issues, verdict is "suggestion".

Be specific: point to the structural problem and explain why it affects
maintainability or organization.
Keep it to what a teammate would leave in a PR comment, not an essay.
"""


def build_structure_agent(model_id: str | None = None):
    kwargs = {"model_id": model_id} if model_id else {}
    return build_reviewer_agent(
        "structure-reviewer",
        SYSTEM_PROMPT,
        AdvisoryReview,
        **kwargs,
    )


def review_structure(agent, code: str) -> AdvisoryReview:
    return review(agent, code, AGENT_KEY)