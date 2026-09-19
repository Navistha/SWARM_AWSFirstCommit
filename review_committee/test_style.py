from review_agents.style_reviewer import build_style_agent
from review_agents.base import review

BAD_STYLE_CODE = """
def calc(p,t):
    x=0
    for i in range(len(p)):
        x=x+p[i]
    return x*(1+t)
"""

CLEAN_STYLE_CODE = """
def calculate_total(prices: list[float], tax_rate: float) -> float:
    subtotal = sum(prices)
    return round(subtotal * (1 + tax_rate), 2)
"""

agent = build_style_agent()

print("=== Bad style snippet ===")
result1 = review(agent, BAD_STYLE_CODE, "style")
print(result1.model_dump_json(indent=2))

print("\n=== Clean style snippet ===")
result2 = review(agent, CLEAN_STYLE_CODE, "style")
print(result2.model_dump_json(indent=2))