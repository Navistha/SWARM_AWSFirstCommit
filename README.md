# Multi-Agent Code Review Swarm

Two specialist AI agents review the same code independently — one only
checks security, one only checks style — and a policy engine decides whose
verdict actually has the power to block a merge.

Built for the AWS First Commit Hackathon (BUILD IT track). Runs entirely
locally, no AWS account required.

## Status

- [x] Security Agent — built, structured output verified
- [x] Style Agent — built, structured output verified
- [x] Policy engine (Python fallback) — built and tested, logic confirmed correct
- [x] Test snippets for the 3-beat demo script
- [x] Orchestrator (`run_review.py`)
- [ ] Real Cedar policy wired in (see `policy/README.md` — optional upgrade, fallback works fine)
- [ ] OpenSearch retrieval for agent context (stretch goal, day 2)
- [ ] Ollama running locally so agents actually respond (needed before demo)

## Setup

1. Install Ollama and pull a model:
   ```
   # https://ollama.com/download
   ollama pull llama3.1
   ```
   Ollama runs its own local server automatically — no further config needed.
   (Alternative: set `USE_ANTHROPIC = True` in `agents/model_config.py` and
   export `ANTHROPIC_API_KEY` if you'd rather use Claude for stronger demo
   quality.)

2. Install Python dependencies:
   ```
   pip install strands-agents ollama
   ```

3. Run the demo:
   ```
   python run_review.py
   ```
   Or run just one scenario: `python run_review.py --one 2`

## Project structure

```
agents/
  model_config.py   — picks Ollama (local) or Anthropic (API key) as the backend
  schema.py          — the Verdict shape both agents must return
  security_agent.py  — only flags security issues
  style_agent.py     — only flags style issues
policy/
  swarm.cedar         — the real policy, in Cedar syntax
  fallback_policy.py  — same logic in plain Python (used by default — see policy/README.md)
data/
  test_snippets.py   — the 3 fixed snippets for the demo script
run_review.py         — orchestrator, run this for the demo
```

## Demo script

1. Clean snippet → both PASS → merge allowed
2. Style issue only → Style Agent suggests, Security passes → merge STILL allowed
3. Security issue → Security Agent blocks → merge blocked, no override

See the engineering doc for full details on judging-criteria alignment and
the day-by-day build plan.
 