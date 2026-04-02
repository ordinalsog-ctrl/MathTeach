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


class LearnerProfile(BaseModel):
    age_group: AgeGroup
    math_level: MathLevel
    confidence: ConfidenceLevel = "medium"
    preferred_pace: Pace = "balanced"
    language: str = "de"
    wants_visuals: bool = True
    wants_history: bool = True
    declared_support_needs: list[SupportNeed] = Field(default_factory=list)


class SessionRequest(BaseModel):
    objective: str = Field(min_length=5, max_length=500)
    learner_profile: LearnerProfile


class RetrievalPlan(BaseModel):
    concept_depth: str
    include_history: bool
    history_mode: str
    include_proof_sketch: bool
    include_modern_applications: bool
    highlight_misconceptions: bool
    network_focus: list[str]
    required_source_types: list[str]


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


class TeachingPlan(BaseModel):
    lesson_mode: str
    audience_mode: str
    tone: str
    teaching_pattern: list[str]
    response_arc: list[str]
    support_signal_profile: SupportSignalProfile
    response_settings: TutorResponseSettings
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


class CorpusDomain(BaseModel):
    slug: str
    name: str
    priority: str
    goal: str


class SourceFamily(BaseModel):
    slug: str
    name: str
    role: str


class CollectionQueueItem(BaseModel):
    slug: str
    priority: str
    target_domains: list[str]
    source_families: list[str]
    output_expectation: str


class CorpusBlueprintResponse(BaseModel):
    checked_on: str
    mission: str
    collection_principles: list[str]
    domains: list[CorpusDomain]
    source_families: list[SourceFamily]
    starter_collection_queue: list[CollectionQueueItem]
    out_of_scope_for_now: list[str]


class ProofThread(BaseModel):
    slug: str
    title: str
    story_focus: str
    required_artifacts: list[str]


class EquationThread(BaseModel):
    slug: str
    title: str
    story_focus: str


class ChronologyEra(BaseModel):
    slug: str
    name: str
    sequence: int
    focus: str
    canonical_figures: list[str]
    canonical_works: list[str]
    proof_threads: list[ProofThread]
    equation_threads: list[EquationThread]


class ChronologyProgramResponse(BaseModel):
    checked_on: str
    mission: str
    organizing_rule: str
    eras: list[ChronologyEra]
    collection_rules: list[str]


class SourceAccessRoute(BaseModel):
    provider: str
    access_type: str
    url: str
    availability: str
    notes: str


class SourceRegistryEntry(BaseModel):
    slug: str
    era: str
    title: str
    date_label: str
    figures: list[str]
    source_kind: str
    significance: str
    proof_or_equation_value: str
    rights_class: str
    storage_class: str
    storage_path_hint: str
    access_routes: list[SourceAccessRoute]


class SourceAccessProgramResponse(BaseModel):
    checked_on: str
    mission: str
    storage_rule: str
    sources: list[SourceRegistryEntry]


class NetworkAnchor(BaseModel):
    era_slug: str
    label: str
    anchor_type: str
    contribution: str


class NetworkTrack(BaseModel):
    slug: str
    title: str
    throughline: str
    eras: list[str]
    anchors: list[NetworkAnchor]
    learner_value: str


class NetworkProgramResponse(BaseModel):
    checked_on: str
    mission: str
    networking_principles: list[str]
    proof_lines: list[NetworkTrack]
    equation_lines: list[NetworkTrack]
    transmission_paths: list[NetworkTrack]
    domain_lines: list[NetworkTrack]
    application_bridges: list[NetworkTrack]
    build_order: list[str]
