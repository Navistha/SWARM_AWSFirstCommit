# llm_client.py
import json
import os

MOCK_MODE = os.environ.get("REVIEW_COMMITTEE_MOCK", "1") == "1"


class MockLLMClient:
    """No network calls at all. Keyword heuristics standing in for a real model."""

    SECURITY_RED_FLAGS = [
        "eval(", "exec(", "os.system(", "pickle.loads(", "SELECT * FROM",
        "password =", "api_key =", "shell=True", "verify=False",
    ]
    STYLE_RED_FLAGS = ["def f(", "def g(", "def x("]

    def invoke(self, system: str, user: str) -> str:
        code = user.split("```\n")[-1].rsplit("\n```", 1)[0]

        if "Security" in system:
            hits = [f for f in self.SECURITY_RED_FLAGS if f in code]
            if hits:
                return json.dumps({"verdict": "BLOCK", "reasoning": f"Found: {', '.join(hits)}"})
            return json.dumps({"verdict": "PASS", "reasoning": "No obvious red flags."})

        if "style" in system.lower():
            hits = [f for f in self.STYLE_RED_FLAGS if f in code]
            if hits:
                return json.dumps({"verdict": "SUGGESTION", "reasoning": "Unclear function naming (single-letter names)."})
            return json.dumps({"verdict": "PASS", "reasoning": "Naming and formatting look fine."})

        return json.dumps({"verdict": "PASS", "reasoning": "Structure looks reasonable."})


class OllamaLLMClient:
    """Real local model via Ollama. No AWS account, no API key, no cost."""

    def __init__(self, model: str = "llama3.1"):
        import ollama
        self._ollama = ollama
        self.model = model

    def invoke(self, system: str, user: str) -> str:
        response = self._ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            format="json",  # forces the model to return valid JSON only
        )
        return response["message"]["content"]


def get_llm_client():
    if MOCK_MODE:
        return MockLLMClient()
    return OllamaLLMClient()