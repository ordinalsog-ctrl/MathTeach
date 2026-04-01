from typing import Literal

from pydantic import BaseModel, Field


AgeGroup = Literal["child", "teen", "adult", "expert"]
MathLevel = Literal[
    "early_school",
    "middle_school",
    "high_school",
    "undergraduate",
    "graduate",
    "research",
]
ConfidenceLevel = Literal["low", "medium", "high"]
Pace = Literal["gentle", "balanced", "intensive"]


class LearnerProfile(BaseModel):
    age_group: AgeGroup
    math_level: MathLevel
    confidence: ConfidenceLevel = "medium"
    preferred_pace: Pace = "balanced"
    language: str = "de"
    wants_visuals: bool = True
    wants_history: bool = True


class SessionRequest(BaseModel):
    objective: str = Field(min_length=5, max_length=500)
    learner_profile: LearnerProfile


class RetrievalPlan(BaseModel):
    concept_depth: str
    include_history: bool
    include_proof_sketch: bool
    include_modern_applications: bool
    highlight_misconceptions: bool
    required_source_types: list[str]


class TeachingPlan(BaseModel):
    audience_mode: str
    tone: str
    teaching_pattern: list[str]
    retrieval_plan: RetrievalPlan
    evaluation_focus: list[str]
    next_turn_contract: list[str]


class ModelAssignment(BaseModel):
    role: str
    model: str
    why: str


class StackResponse(BaseModel):
    checked_on: str
    primary_choice: str
    assignments: list[ModelAssignment]
    architecture_summary: str


class FoundationLayer(BaseModel):
    name: str
    mission: str
    stores: list[str]
    invariants: list[str]


class FoundationResponse(BaseModel):
    architecture_name: str
    separation_principle: str
    knowledge_core: FoundationLayer
    teacher_mind: FoundationLayer
    handoff_contract: list[str]
    first_build_order: list[str]
