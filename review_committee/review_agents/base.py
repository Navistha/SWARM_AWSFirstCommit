import os
from pydantic import BaseModel
from strands import Agent
from strands.models.ollama import OllamaModel

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
DEFAULT_MODEL_ID = os.environ.get("REVIEWER_MODEL_ID", "llama3.1:8b")


def build_reviewer_agent(name: str, system_prompt: str, output_model: type[BaseModel], model_id: str = DEFAULT_MODEL_ID) -> Agent:
    model = OllamaModel(
        host=OLLAMA_HOST,
        model_id=model_id,
        temperature=0.1,
    )
    return Agent(
        model=model,
        name=name,
        system_prompt=system_prompt,
        structured_output_model=output_model,
        callback_handler=None,
    )
def review(agent: Agent, code: str, agent_key: str) -> BaseModel:
    prompt = (
        "Review the following code snippet. Set `agent` in your response to "
        f'"{agent_key}". Only comment on what your role covers -- ignore anything '
        "outside your lane, even if you notice it.\n\n"
        f"```\n{code}\n```"
    )
    result = agent(prompt)
    review_result = result.structured_output
    if review_result is None:
        raise RuntimeError(f"{agent_key} reviewer did not return structured output: {result}")
    return review_result