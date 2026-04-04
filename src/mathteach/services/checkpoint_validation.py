from __future__ import annotations

from mathteach.models import ModeAdaptationCheckpoint, ModeAdaptationState


CURRENT_MODE_ADAPTATION_CHECKPOINT_VERSION = "phase_h1_v1"
MIGRATABLE_MODE_ADAPTATION_CHECKPOINT_VERSIONS = frozenset({"phase_h0_v1"})
KNOWN_MODE_ADAPTATION_CHECKPOINT_VERSIONS = frozenset(
    {CURRENT_MODE_ADAPTATION_CHECKPOINT_VERSION}
    | MIGRATABLE_MODE_ADAPTATION_CHECKPOINT_VERSIONS
)

MAX_MODE_CHANGES_PER_SESSION = 3
MAX_COOLDOWN_BLOCKS_AFTER_CHANGE = 1


class SessionValidationError(ValueError):
    pass


class CheckpointMigrationRequired(ValueError):
    pass


def validate_checkpoint_for_resume(checkpoint: ModeAdaptationCheckpoint) -> None:
    _validate_checkpoint_schema_version(checkpoint)
    _validate_checkpoint_state(checkpoint.mode_adaptation_state)


def validate_checkpoint_for_persist(checkpoint: ModeAdaptationCheckpoint) -> None:
    if checkpoint.schema_version != CURRENT_MODE_ADAPTATION_CHECKPOINT_VERSION:
        raise SessionValidationError(
            "Only the current mode adaptation checkpoint version can be persisted: "
            f"{CURRENT_MODE_ADAPTATION_CHECKPOINT_VERSION}."
        )
    _validate_checkpoint_state(checkpoint.mode_adaptation_state)


def _validate_checkpoint_schema_version(checkpoint: ModeAdaptationCheckpoint) -> None:
    schema_version = checkpoint.schema_version
    if schema_version not in KNOWN_MODE_ADAPTATION_CHECKPOINT_VERSIONS:
        raise SessionValidationError(
            f"Unknown schema_version: {schema_version}. "
            f"Known versions: {sorted(KNOWN_MODE_ADAPTATION_CHECKPOINT_VERSIONS)}."
        )
    if schema_version != CURRENT_MODE_ADAPTATION_CHECKPOINT_VERSION:
        raise CheckpointMigrationRequired(
            f"Checkpoint version {schema_version} requires migration to "
            f"{CURRENT_MODE_ADAPTATION_CHECKPOINT_VERSION}."
        )


def _validate_checkpoint_state(state: ModeAdaptationState) -> None:
    if not state.current_mode.strip():
        raise SessionValidationError("Mode adaptation state must include a current mode.")
    if state.mode_changes_in_session > MAX_MODE_CHANGES_PER_SESSION:
        raise SessionValidationError(
            "Invalid mode_changes_in_session: "
            f"{state.mode_changes_in_session} exceeds the H.1 change budget of "
            f"{MAX_MODE_CHANGES_PER_SESSION}."
        )
    if state.cooldown_blocks_remaining > MAX_COOLDOWN_BLOCKS_AFTER_CHANGE:
        raise SessionValidationError(
            "Invalid cooldown_blocks_remaining: "
            f"{state.cooldown_blocks_remaining} exceeds the H.1 cooldown limit of "
            f"{MAX_COOLDOWN_BLOCKS_AFTER_CHANGE}."
        )
