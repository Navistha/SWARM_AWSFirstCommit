from typing import Literal
from pydantic import BaseModel, Field

# Advisory agents (Style, Structure) sirf ye do values de sakte hain
AdvisoryVerdictValue = Literal["pass", "suggestion"]

# Security agent (Agent 1) ye do values de sakta hai
SecurityVerdictValue = Literal["pass", "block"]


class Finding(BaseModel):
    """Style/Structure agent ka ek issue"""
    summary: str = Field(description="One-line issue, e.g. 'inconsistent indentation'")
    line_hint: str | None = Field(default=None, description="Line number ya code excerpt")
    severity: Literal["minor", "moderate"] = Field(default="minor")


class AdvisoryReview(BaseModel):
    """Style ya Structure agent ka poora verdict"""
    agent: str
    verdict: AdvisoryVerdictValue
    reasoning: str = Field(description="1-3 sentence explanation")
    findings: list[Finding] = Field(default_factory=list)


class Vulnerability(BaseModel):
    """Security agent ka ek vulnerability finding"""
    summary: str = Field(description="e.g. 'SQL injection via string-formatted query'")
    line_hint: str | None = Field(default=None)
    category: str = Field(description="e.g. 'injection', 'hardcoded-secret', 'auth-bypass'")
    severity: Literal["low", "medium", "high", "critical"]


class SecurityReview(BaseModel):
    """Security agent (Agent 1) ka poora verdict"""
    agent: Literal["security"] = "security"
    verdict: SecurityVerdictValue
    reasoning: str = Field(description="1-3 sentence explanation")
    vulnerabilities: list[Vulnerability] = Field(default_factory=list)