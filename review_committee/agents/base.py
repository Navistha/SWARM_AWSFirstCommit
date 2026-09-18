from dataclasses import dataclass
from enum import Enum


class Verdict(str, Enum):
    PASS = "PASS"
    SUGGESTION = "SUGGESTION"
    BLOCK = "BLOCK"


@dataclass
class AgentVote:
    agent_name: str
    verdict: Verdict
    reasoning: str

    def to_dict(self):
        return {"agent": self.agent_name, "verdict": self.verdict.value, "reasoning": self.reasoning}


SECURITY_TERMS = ["security", "vulnerab", "injection", "exploit", "hardcoded secret",
                   "credential", "hardcoded", "plaintext", "unauthorized access",
                   "authentication", "auth bypass", "sensitive data"]

SECURITY_CLASSIFIER_PROMPT = (
    "You are a strict classifier. You will be given a single code review comment. "
    "Reply with ONLY one word: YES or NO.\n"
    "Reply YES if the comment describes, hints at, or relates to any security "
    "concern — vulnerabilities, injection, unsafe/unsanitized input, hardcoded "
    "secrets, authentication, exposure of sensitive data — even if it never uses "
    "the word 'security' (e.g. 'raw string concatenated into a query' still counts "
    "as YES, since that IS a description of SQL injection).\n"
    "Reply NO only if the comment is purely about naming, formatting, performance, "
    "or code structure/maintainability with zero security relevance."
)


class BaseAgent:
    name: str = "BaseAgent"
    system_prompt: str = ""

    def __init__(self, llm_client):
        self.llm_client = llm_client

    def _build_prompt(self, code: str) -> str:
        return (
            f"{self.system_prompt}\n\n"
            "Respond with ONLY a JSON object, no prose, no markdown fences:\n"
            '{"verdict": "PASS" | "SUGGESTION" | "BLOCK", "reasoning": "<1-3 sentences>"}\n\n'
            f"Code to review:\n```\n{code}\n```"
        )

    def review(self, code: str) -> AgentVote:
        raw = self.llm_client.invoke(system=self.system_prompt, user=self._build_prompt(code))
        return self._parse(raw)

    def _is_security_related(self, reasoning: str) -> bool:
        try:
            raw = self.llm_client.invoke(
                system=SECURITY_CLASSIFIER_PROMPT,
                user=f"Comment: {reasoning}",
            )
            return raw.strip().upper().startswith("Y")
        except Exception:
            return any(t in reasoning.lower() for t in SECURITY_TERMS)

    def _parse(self, raw_text: str) -> AgentVote:
        import json
        cleaned = raw_text.strip().strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:]
        try:
            data = json.loads(cleaned)
            verdict = Verdict(data["verdict"].upper())
            reasoning = data.get("reasoning", "")
        except Exception:
            verdict = Verdict.BLOCK if self.name == "SecurityReviewer" else Verdict.SUGGESTION
            reasoning = f"Could not parse model output: {raw_text[:150]}"

        if self.name != "SecurityReviewer" and reasoning and self._is_security_related(reasoning):
            verdict = Verdict.PASS
            reasoning = "No concerns within this reviewer's scope."

        return AgentVote(self.name, verdict, reasoning)