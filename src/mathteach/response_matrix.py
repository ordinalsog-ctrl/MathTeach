from typing import Literal

from pydantic import BaseModel, Field


SupportNeed = Literal[
    "adhd_aware_support",
    "dyscalculia_aware_support",
    "dyslexia_aware_support",
    "autism_spectrum_aware_support",
    "language_sensitive_support",
    "scarcity_aware_support",
]
SupportLevel = Literal["none", "possible", "declared", "highly_relevant"]
SupportState = Literal["fragile", "supported", "typical", "strong"]
SafetyLevel = Literal["low", "moderate", "high"]


class SupportSignalProfile(BaseModel):
    working_memory_load: SupportState = "typical"
    attention_regulation: SupportState = "typical"
    symbolic_processing: SupportState = "typical"
    math_anxiety: SafetyLevel = "low"
    adhd_aware_support: SupportLevel = "none"
    dyscalculia_aware_support: SupportLevel = "none"
    dyslexia_aware_support: SupportLevel = "none"
    autism_spectrum_aware_support: SupportLevel = "none"
    language_sensitive_support: SupportLevel = "none"
    scarcity_aware_support: SupportLevel = "none"
    active_supports: list[SupportNeed] = Field(default_factory=list)


class TutorResponseSettings(BaseModel):
    session_duration: str
    break_pattern: str
    transition_buffer: str
    conceptual_increment: str
    worked_example_ratio: str
    fading_speed: str
    symbolic_vs_verbal_balance: str
    word_budget_per_chunk: str
    primary_representation: str
    error_response_style: str
    check_frequency: str
    language_support: str
    sensory_load_level: str
    external_scaffolds: list[str]
    active_supports: list[SupportNeed]
    rationale_summary: list[str]
    source_anchors: list[str]
