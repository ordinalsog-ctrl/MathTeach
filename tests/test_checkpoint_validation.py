import pytest

from mathteach.models import ModeAdaptationCheckpoint, ModeAdaptationState
from mathteach.services.checkpoint_validation import (
    CURRENT_MODE_ADAPTATION_CHECKPOINT_VERSION,
    CheckpointMigrationRequired,
    SessionValidationError,
    validate_checkpoint_for_persist,
    validate_checkpoint_for_resume,
)


def test_validate_checkpoint_for_resume_accepts_current_checkpoint() -> None:
    checkpoint = ModeAdaptationCheckpoint(
        schema_version=CURRENT_MODE_ADAPTATION_CHECKPOINT_VERSION,
        mode_adaptation_state=ModeAdaptationState(
            current_mode="guided_concept_explanation",
            blocks_in_current_mode=1,
            mode_changes_in_session=0,
        ),
    )

    validate_checkpoint_for_resume(checkpoint)


def test_validate_checkpoint_for_resume_requires_migration_for_known_old_version() -> None:
    checkpoint = ModeAdaptationCheckpoint(
        schema_version="phase_h0_v1",
        mode_adaptation_state=ModeAdaptationState(
            current_mode="guided_concept_explanation",
            blocks_in_current_mode=1,
            mode_changes_in_session=0,
        ),
    )

    with pytest.raises(CheckpointMigrationRequired):
        validate_checkpoint_for_resume(checkpoint)


def test_validate_checkpoint_for_resume_requires_migration_for_known_legacy_chain_version() -> None:
    checkpoint = ModeAdaptationCheckpoint(
        schema_version="phase_h0_v0",
        mode_adaptation_state=ModeAdaptationState(
            current_mode="guided_concept_explanation",
            blocks_in_current_mode=1,
            mode_changes_in_session=0,
        ),
    )

    with pytest.raises(CheckpointMigrationRequired):
        validate_checkpoint_for_resume(checkpoint)


def test_validate_checkpoint_for_resume_rejects_unknown_version() -> None:
    checkpoint = ModeAdaptationCheckpoint(
        schema_version="phase_future_v99",
        mode_adaptation_state=ModeAdaptationState(
            current_mode="guided_concept_explanation",
            blocks_in_current_mode=1,
            mode_changes_in_session=0,
        ),
    )

    with pytest.raises(SessionValidationError) as exc_info:
        validate_checkpoint_for_resume(checkpoint)

    assert "Unknown schema_version" in str(exc_info.value)


def test_validate_checkpoint_for_persist_rejects_state_beyond_h1_limits() -> None:
    checkpoint = ModeAdaptationCheckpoint(
        schema_version=CURRENT_MODE_ADAPTATION_CHECKPOINT_VERSION,
        mode_adaptation_state=ModeAdaptationState(
            current_mode="guided_concept_explanation",
            blocks_in_current_mode=1,
            mode_changes_in_session=4,
            cooldown_blocks_remaining=0,
        ),
    )

    with pytest.raises(SessionValidationError) as exc_info:
        validate_checkpoint_for_persist(checkpoint)

    assert "change budget" in str(exc_info.value)
