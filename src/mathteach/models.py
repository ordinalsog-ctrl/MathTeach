from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Literal
from uuid import uuid4

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
EngagementLevel = Literal["high", "medium", "low"]
ErrorRateTrend = Literal["improving", "stable", "degrading"]
ObservationSignalType = Literal[
    "confusion_signal",
    "overload_signal",
    "stagnation_signal",
    "breakthrough_signal",
    "confidence_recovery_signal",
]
TransitionFamily = Literal["simplifying", "reframing", "stretching"]
ModeAdaptationCheckpointVersion = str
ResumeSource = Literal[
    "fresh_start",
    "inline_state",
    "inline_checkpoint",
    "stored_checkpoint",
]


class BlockType(StrEnum):
    CONCEPT_INTRODUCTION = "concept_introduction"
    WORKED_EXAMPLE = "worked_example"
    GUIDED_PRACTICE = "guided_practice"
    ERROR_RECOVERY = "error_recovery"
    CONCEPT_CHECK = "concept_check"
    BRIDGE_TO_APPLICATION = "bridge_to_application"
    REFLECTION = "reflection"


class EvidenceCombinationPattern(StrEnum):
    RAPID_CONSECUTIVE_SUCCESS = "rapid_consecutive_success"
    STAGNATION_PATTERN = "stagnation_pattern"
    INCONSISTENT_SUCCESS = "inconsistent_success"
    VOCABULARY_GAP = "vocabulary_gap"
    CONFIDENCE_BUILDUP = "confidence_buildup"
    CONCEPT_CONFUSION = "concept_confusion"


class BlockTransitionReason(StrEnum):
    EVIDENCE_PATTERN = "evidence_pattern"
    SUPPORT_PROFILE = "support_profile"
    SEQUENCE_BALANCE = "sequence_balance"
    LOOKAHEAD_FALLBACK = "lookahead_fallback"


class BlockSequenceIntent(StrEnum):
    CONCEPT_BUILDUP = "concept_buildup"
    CONFIDENCE_BUILDING = "confidence_building"
    ERROR_RECOVERY_CYCLE = "error_recovery_cycle"
    MASTERY_PATH = "mastery_path"
    ADAPTIVE_REMEDIATION = "adaptive_remediation"


class LearningGoalCategory(StrEnum):
    CONCEPT_MASTERY = "concept_mastery"
    PROCEDURAL_FLUENCY = "procedural_fluency"
    CONCEPTUAL_UNDERSTANDING = "conceptual_understanding"
    TRANSFER_ABILITY = "transfer_ability"


class ConceptComplexityLevel(StrEnum):
    FOUNDATIONAL = "foundational"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


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
    resume_source: ResumeSource | None = None
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
    duration_seconds: float | None = Field(default=None, ge=0.0)
    accuracy_estimate: float | None = Field(default=None, ge=0.0, le=1.0)
    engagement_estimate: EngagementLevel | None = None


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


class EvidenceCombination(BaseModel):
    patterns: list[EvidenceCombinationPattern] = Field(default_factory=list)
    current_evidence: list[str] = Field(default_factory=list)
    previous_evidence: list[str] = Field(default_factory=list)
    block_type: BlockType
    block_sequence: int = Field(ge=1)


class LongTermLearningGoal(BaseModel):
    goal_id: str = Field(min_length=3)
    category: LearningGoalCategory
    concept: str = Field(min_length=2)
    description: str = Field(min_length=3)
    complexity_level: ConceptComplexityLevel
    target_mastery_threshold: float = Field(default=0.85, ge=0.0, le=1.0)
    estimated_blocks_needed: int = Field(default=4, ge=1)


class SessionHistoryEntry(BaseModel):
    block_index: int = Field(ge=1)
    block_type: BlockType
    evidence_patterns: list[EvidenceCombinationPattern] = Field(default_factory=list)
    observed_evidence: list[str] = Field(default_factory=list)
    success_indicators: list[str] = Field(default_factory=list)
    difficulty_rating: float = Field(default=0.5, ge=0.0, le=1.0)
    concept_target: str | None = None


class SessionProgressTracker(BaseModel):
    session_id: str | None = None
    current_concept: str = Field(min_length=2)
    learning_goals: list[LongTermLearningGoal] = Field(default_factory=list)
    history_entries: list[SessionHistoryEntry] = Field(default_factory=list)
    concept_mastery_tracking: dict[str, float] = Field(default_factory=dict)


class PathScoringCriteria(BaseModel):
    heuristic_weight: float = Field(default=0.35, ge=0.0, le=1.0)
    goal_alignment_weight: float = Field(default=0.2, ge=0.0, le=1.0)
    history_alignment_weight: float = Field(default=0.15, ge=0.0, le=1.0)
    evidence_continuity_weight: float = Field(default=0.1, ge=0.0, le=1.0)
    profile_match_weight: float = Field(default=0.1, ge=0.0, le=1.0)
    pilot_data_adjustment_weight: float = Field(default=0.1, ge=0.0, le=1.0)

    @model_validator(mode="after")
    def validate_total_weight(self) -> "PathScoringCriteria":
        total = (
            self.heuristic_weight
            + self.goal_alignment_weight
            + self.history_alignment_weight
            + self.evidence_continuity_weight
            + self.profile_match_weight
            + self.pilot_data_adjustment_weight
        )
        if abs(total - 1.0) > 0.001:
            raise ValueError("Path scoring weights must sum to 1.0.")
        return self


class DecisionAlternative(BaseModel):
    path_id: str = Field(min_length=3)
    score: float = Field(ge=0.0, le=1.0)
    score_breakdown: dict[str, float] = Field(default_factory=dict)


class OutcomeMetrics(BaseModel):
    observed_evidence: list[str] = Field(default_factory=list)
    observed_evidence_patterns: list[EvidenceCombinationPattern] = Field(
        default_factory=list
    )
    duration_seconds: float | None = Field(default=None, ge=0.0)
    accuracy_estimate: float | None = Field(default=None, ge=0.0, le=1.0)
    confidence_change: float = 0.0
    mastery_gain_estimate: float = Field(default=0.0, ge=0.0, le=1.0)
    error_rate_trend: ErrorRateTrend = "stable"
    observed_engagement: EngagementLevel = "medium"


class CalibrationWeights(BaseModel):
    baseline_weights: dict[str, float] = Field(
        default_factory=lambda: {
            "heuristic": 0.35,
            "goal_alignment": 0.2,
            "history_alignment": 0.15,
            "evidence_continuity": 0.1,
            "profile_match": 0.1,
            "pilot_data_adjustment": 0.1,
        }
    )
    adjusted_weights: dict[str, float] = Field(default_factory=dict)
    calibration_rounds: int = Field(default=0, ge=0)
    last_calibration: datetime | None = None
    mean_squared_error_history: list[float] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_weight_sets(self) -> "CalibrationWeights":
        for weights in (self.baseline_weights, self.adjusted_weights):
            if not weights:
                continue
            total = sum(weights.values())
            if abs(total - 1.0) > 0.001:
                raise ValueError("Calibration weights must sum to 1.0.")
        return self

    def get_current_weights(self) -> dict[str, float]:
        return self.adjusted_weights.copy() if self.adjusted_weights else self.baseline_weights.copy()


class DecisionRecord(BaseModel):
    decision_id: str = Field(default_factory=lambda: uuid4().hex)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    session_id: str | None = None
    current_block_type: BlockType
    evidence_patterns: list[EvidenceCombinationPattern] = Field(default_factory=list)
    active_supports: list[SupportNeed] = Field(default_factory=list)
    available_candidate_paths: list[str] = Field(default_factory=list)
    chosen_path_id: str = Field(min_length=3)
    chosen_path_score: float = Field(ge=0.0, le=1.0)
    chosen_path_score_breakdown: dict[str, float] = Field(default_factory=dict)
    alternative_paths: list[DecisionAlternative] = Field(default_factory=list)
    observed_outcome: OutcomeMetrics | None = None
    outcome_timestamp: datetime | None = None
    used_for_calibration: bool = False
    calibration_weight_updates: dict[str, float] | None = None


class CalibrationContext(BaseModel):
    decision_id: str | None = None
    calibration_rounds: int = Field(default=0, ge=0)
    logged_decision_count: int = Field(default=0, ge=0)
    last_calibration: datetime | None = None
    active_weights: dict[str, float] = Field(default_factory=dict)


class BlockSequenceDecision(BaseModel):
    current_block_type: BlockType
    suggested_next_block_type: BlockType
    alternative_next_block_types: list[BlockType] = Field(default_factory=list)
    transition_reason: BlockTransitionReason
    sequence_intent: BlockSequenceIntent
    rationale: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    lookahead_block_types: list[BlockType] = Field(default_factory=list)
    selected_path_score: float | None = Field(default=None, ge=0.0, le=1.0)
    candidate_paths: list["BlockSequencePathOption"] = Field(default_factory=list)


class BlockSequencePathOption(BaseModel):
    block_types: list[BlockType] = Field(default_factory=list)
    score: float = Field(default=0.0, ge=0.0, le=1.0)
    rationale: list[str] = Field(default_factory=list)


class EnrichedPathEvaluation(BaseModel):
    path_id: str = Field(min_length=3)
    block_types: list[BlockType] = Field(default_factory=list)
    raw_score: float = Field(default=0.0, ge=0.0, le=1.0)
    uncalibrated_total_score: float | None = Field(default=None, ge=0.0, le=1.0)
    total_score: float = Field(default=0.0, ge=0.0, le=1.0)
    mastery_projection: float = Field(default=0.0, ge=0.0, le=1.0)
    calibration_applied: bool = False
    score_breakdown: dict[str, float] = Field(default_factory=dict)
    goal_alignment_explanation: str = ""
    history_alignment_explanation: str = ""
    evidence_continuity_explanation: str = ""
    profile_match_explanation: str = ""
    pilot_data_references: list[str] = Field(default_factory=list)


class BlockSequenceState(BaseModel):
    block_type_history: list[BlockType] = Field(default_factory=list)
    recent_evidence_patterns: list[EvidenceCombinationPattern] = Field(default_factory=list)
    active_sequence_intent: BlockSequenceIntent | None = None
    adaptive_transitions_applied: int = Field(default=0, ge=0)
    last_recommended_block_type: BlockType | None = None
    lookahead_block_types: list[BlockType] = Field(default_factory=list)


class SequencePlanningMetadata(BaseModel):
    active_sequence_intent: BlockSequenceIntent | None = None
    next_block_options: list[BlockType] = Field(default_factory=list)
    adaptive_transitions_applied: int = Field(default=0, ge=0)
    last_transition_reason: BlockTransitionReason | None = None
    last_routing_confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    lookahead_block_types: list[BlockType] = Field(default_factory=list)
    candidate_path_count: int = Field(default=0, ge=0)
    candidate_paths: list[BlockSequencePathOption] = Field(default_factory=list)
    calibration_decision_id: str | None = None
    calibration_rounds: int = Field(default=0, ge=0)


class LongTermContext(BaseModel):
    session_id: str | None = None
    current_concept: str = Field(min_length=2)
    learning_goals: list[LongTermLearningGoal] = Field(default_factory=list)
    concept_mastery_tracking: dict[str, float] = Field(default_factory=dict)
    history_entry_count: int = Field(default=0, ge=0)


class PlannedTeachingBlock(BaseModel):
    block_index: int = Field(ge=1)
    mode: str
    block_type: BlockType | None = None
    sequence_intent: BlockSequenceIntent | None = None
    transition_reason: BlockTransitionReason | None = None
    next_block_type: BlockType | None = None
    alternative_next_block_types: list[BlockType] = Field(default_factory=list)
    routing_confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    selected_path_score: float | None = Field(default=None, ge=0.0, le=1.0)
    routing_rationale: list[str] = Field(default_factory=list)
    candidate_paths: list[BlockSequencePathOption] = Field(default_factory=list)
    goal: str
    focus: list[str] = Field(default_factory=list)
    support_moves: list[str] = Field(default_factory=list)
    support_scaffolds: list[str] = Field(default_factory=list)
    evidence_combination: EvidenceCombination | None = None
    conflict_resolution_summary: ConflictResolutionSummary | None = None
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


class ResumeContext(BaseModel):
    resume_source: ResumeSource = "fresh_start"
    resume_active: bool = False
    carried_observation_evidence: list[str] = Field(default_factory=list)
    used_carried_observation_evidence: bool = False
    pending_transition_message_carried: bool = False
    pending_transition_message_consumed: bool = False


class ConflictResolutionSummary(BaseModel):
    pair_conflicts: list[str] = Field(default_factory=list)
    triad_group: str | None = None
    priority_ladder: list[str] = Field(default_factory=list)
    suppressed_moves: list[str] = Field(default_factory=list)
    adapted_moves: list[str] = Field(default_factory=list)
    generated_moves: list[str] = Field(default_factory=list)
    move_dependencies_applied: list[str] = Field(default_factory=list)
    lesson_mode_applied: str | None = None
    mode_evidence_adjustments: list[str] = Field(default_factory=list)
    block_type_applied: BlockType | None = None
    evidence_patterns_applied: list[EvidenceCombinationPattern] = Field(
        default_factory=list
    )
    evidence_combination_rules_applied: list[str] = Field(default_factory=list)
    blocktype_adjustments_applied: list[str] = Field(default_factory=list)
    resolution_notes: list[str] = Field(default_factory=list)
    evidence_used: list[str] = Field(default_factory=list)


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
    block_sequence_state: BlockSequenceState | None = None
    sequence_planning_metadata: SequencePlanningMetadata | None = None
    long_term_context: LongTermContext | None = None
    enriched_paths: list[EnrichedPathEvaluation] = Field(default_factory=list)
    recommended_path_id: str | None = None
    recommended_path_mastery_gain: float | None = Field(default=None, ge=0.0, le=1.0)
    calibration_context: CalibrationContext | None = None
    mode_adaptation_trace: list[ModeAdaptationTraceEntry] = Field(default_factory=list)
    resume_context: ResumeContext
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
