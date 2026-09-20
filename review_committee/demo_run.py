from review_agents.security_reviewer import build_security_agent, review_security
from review_agents.style_reviewer import build_style_agent, review_style

CLEAN_CODE = """
def calculate_total(prices: list[float], tax_rate: float) -> float:
    subtotal = sum(prices)
    return round(subtotal * (1 + tax_rate), 2)
"""

STYLE_ISSUE_CODE = """
def calc(p,t):
    x=0
    for i in range(len(p)):
        x=x+p[i]
    return x*(1+t)
"""

SECURITY_ISSUE_CODE = """
def get_user(username):
    conn = sqlite3.connect("app.db")
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    return conn.execute(query).fetchone()
"""

SNIPPETS = [
    ("clean", CLEAN_CODE),
    ("style", STYLE_ISSUE_CODE),
    ("security", SECURITY_ISSUE_CODE),
]


def run():
    security_agent = build_security_agent()
    style_agent = build_style_agent()

    for label, code in SNIPPETS:
        print(f"\nCODE REVIEW SWARM -- reviewing: {label}")
        print("-" * 60)

        sec = review_security(security_agent, code)
        sty = review_style(style_agent, code)

        sec_icon = "🔴" if sec.verdict == "block" else "🟢"
        sty_icon = "🟢" if sty.verdict == "pass" else "🟡"

        print(f"{sec_icon} SecurityReviewer   {sec.verdict.upper():<10} {sec.reasoning}")
        print(f"{sty_icon} StyleReviewer      {sty.verdict.upper():<10} {sty.reasoning}")

        final = "MERGE BLOCKED" if sec.verdict == "block" else "MERGE ALLOWED"
        print(f"\n>>> {final}")
        if sec.verdict == "block":
            for v in sec.vulnerabilities:
                print(f"    - {v.summary} [{v.severity}]")
        elif sty.verdict == "suggestion":
            for f in sty.findings:
                print(f"    - {f.summary}")


if __name__ == "__main__":
    run()