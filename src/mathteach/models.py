from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator

from mathteach.response_matrix import (
    SupportNeed,
    SupportSignalProfile,
    TutorResponseSettings,
)

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
ObservationStrength = Literal["weak", "meaningful", "strong"]
ObservationSignalType = Literal[
    "confusion_signal",
    "overload_signal",
    "stagnation_signal",
    "breakthrough_signal",
    "confidence_recovery_signal",
]
TransitionFamily = Literal["simplifying", "reframing", "stretching"]
ModeAdaptationCheckpointVersion = str


class LearnerProfile(BaseModel):
    age_group: AgeGroup
    math_level: MathLevel
    confidence: ConfidenceLevel = "medium"
    preferred_pace: Pace = "balanced"
    language: str = "de"
    wants_visuals: bool = True
    wants_history: bool = True
    declared_support_needs: list[SupportNeed] = Field(default_factory=list)


class RuntimeObservationInput(BaseModel):
    evidence: list[str] = Field(default_factory=list)


class ModeAdaptationState(BaseModel):
    current_mode: str = Field(min_length=3)
    blocks_in_current_mode: int = Field(default=0, ge=0)
    mode_changes_in_session: int = Field(default=0, ge=0)
    last_change_reason: str | None = None
    cooldown_blocks_remaining: int = Field(default=0, ge=0)
    pending_transition_message: str | None = None
    last_observation_evidence: list[str] = Field(default_factory=list)


class ModeAdaptationCheckpoint(BaseModel):
    schema_version: ModeAdaptationCheckpointVersion = "phase_h1_v1"
    mode_adaptation_state: ModeAdaptationState


class SessionRequest(BaseModel):
    objective: str = Field(min_length=5, max_length=500)
    learner_profile: LearnerProfile
    session_id: str | None = Field(default=None, min_length=3, max_length=128)
    runtime_observations: list[RuntimeObservationInput] = Field(default_factory=list)
    mode_adaptation_state: ModeAdaptationState | None = None
    mode_adaptation_checkpoint: ModeAdaptationCheckpoint | None = None

    @model_validator(mode="after")
    def validate_runtime_resume_inputs(self) -> SessionRequest:
        if (
            self.mode_adaptation_state is not None
            and self.mode_adaptation_checkpoint is not None
        ):
            raise ValueError(
                "Provide either mode_adaptation_state or mode_adaptation_checkpoint, not both."
            )
        return self


class RetrievalPlan(BaseModel):
    concept_depth: str
    include_history: bool
    history_mode: str
    include_proof_sketch: bool
    include_modern_applications: bool
    highlight_misconceptions: bool
    network_focus: list[str]
    required_source_types: list[str]


class ModeSelection(BaseModel):
    requested_mode: str
    selected_mode: str
    rationale: list[str]
    constraints: list[str]


class RawBlockObservation(BaseModel):
    block_index: int = Field(ge=0)
    current_mode: str = Field(min_length=3)
    evidence: list[str] = Field(default_factory=list)


class ObservationSignal(BaseModel):
    signal_type: ObservationSignalType
    strength: ObservationStrength
    evidence: list[str] = Field(default_factory=list)
    support_context: list[SupportNeed] = Field(default_factory=list)
    block_index: int = Field(ge=0)


class SignalInterpretationResult(BaseModel):
    raw_observation: RawBlockObservation
    signals: list[ObservationSignal] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class ModeAdaptationDecision(BaseModel):
    selected_mode: str
    changed: bool = False
    trigger_signals: list[str] = Field(default_factory=list)
    transition_family: TransitionFamily | None = None
    transition_message: str | None = None
    notes: list[str] = Field(default_factory=list)


class PlannedTeachingBlock(BaseModel):
    block_index: int = Field(ge=1)
    mode: str
    goal: str
    focus: list[str] = Field(default_factory=list)
    transition_message: str | None = None
    observed_evidence: list[str] = Field(default_factory=list)


class ModeAdaptationTraceEntry(BaseModel):
    block_index: int = Field(ge=1)
    mode_before: str
    mode_after: str
    changed: bool
    trigger_signals: list[str] = Field(default_factory=list)
    transition_message: str | None = None
    notes: list[str] = Field(default_factory=list)


class TeachingPlan(BaseModel):
    session_id: str | None = None
    lesson_mode: str
    audience_mode: str
    tone: str
    teaching_pattern: list[str]
    response_arc: list[str]
    mode_selection: ModeSelection
    mode_adaptation_state: ModeAdaptationState
    mode_adaptation_checkpoint: ModeAdaptationCheckpoint
    planned_blocks: list[PlannedTeachingBlock] = Field(default_factory=list)
    mode_adaptation_trace: list[ModeAdaptationTraceEntry] = Field(default_factory=list)
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
