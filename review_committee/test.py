# test_judge.py
from agents import AgentVote, Verdict
from policy_engine import CedarPolicyEngine

votes_block = [
    AgentVote("SecurityReviewer", Verdict.BLOCK, "SQL injection found"),
    AgentVote("StyleReviewer", Verdict.PASS, "looks fine"),
    AgentVote("StructureReviewer", Verdict.PASS, "looks fine"),
]

votes_allow = [
    AgentVote("SecurityReviewer", Verdict.PASS, "no issues"),
    AgentVote("StyleReviewer", Verdict.SUGGESTION, "rename this var"),
    AgentVote("StructureReviewer", Verdict.PASS, "fine"),
]

engine = CedarPolicyEngine()
print(engine.decide(votes_block))
print(engine.decide(votes_allow))