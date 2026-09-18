# main.py
import argparse
import json
import sys
from orchestrator import run_review

DEMO_SNIPPETS = {
    "clean": '''
def calculate_total(prices: list[float]) -> float:
    """Return the sum of a list of prices."""
    return sum(prices)
''',
    "style": '''
def f(x,y,z,a,b,c,d):
    if x==1:
        if y==2:
            if z==3:
                return a+b+c+d
    return 0
''',
    "security": '''
import sqlite3

def get_user(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchone()

password = "hardcoded-secret-do-not-do-this"
''',
    "structure": '''
def process_order(order_data):
    if not order_data.get("items"):
        raise ValueError("no items")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders VALUES (?)", (order_data,))
    total = sum(i["price"] * i["qty"] for i in order_data["items"])
    if total > 1000:
        total *= 0.9
    return {"status": "ok", "total": total}
''',
}


def print_result(label: str, result: dict) -> None:
    print(f"\n{'=' * 60}")
    print(f"SNIPPET: {label}")
    print("=" * 60)
    for vote in result["votes"]:
        print(f"[{vote['agent']}] {vote['verdict']} — {vote['reasoning']}")
    print("-" * 60)
    decision = result["decision"]
    if decision["merge_blocked"]:
        print(f"RESULT: MERGE BLOCKED — {decision['blocking_reason']}")
    else:
        print("RESULT: MERGE ALLOWED")
        for s in decision["suggestions"]:
            print(f"  (suggestion, non-blocking): {s}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--snippet", choices=DEMO_SNIPPETS.keys(), default=None,
                         help="run just one built-in demo snippet")
    parser.add_argument("--file", type=str, default=None,
                         help="path to a code file to review instead of the demo snippets")
    parser.add_argument("--json", action="store_true", help="print raw JSON instead of formatted output")
    args = parser.parse_args()

    if args.file:
        with open(args.file) as f:
            code = f.read()
        result = run_review(code)
        print(json.dumps(result, indent=2) if args.json else print_result(args.file, result))
        sys.exit(0)

    snippets = {args.snippet: DEMO_SNIPPETS[args.snippet]} if args.snippet else DEMO_SNIPPETS
    for label, code in snippets.items():
        result = run_review(code)
        if args.json:
            print(json.dumps({label: result}, indent=2))
        else:
            print_result(label, result)