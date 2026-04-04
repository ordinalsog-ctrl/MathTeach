import pytest

from mathteach.models import ModeAdaptationCheckpoint, ModeAdaptationState
from mathteach.services.checkpoint_migrator import (
    CheckpointMigrationError,
    CheckpointMigrator,
)
from mathteach.services.checkpoint_validation import (
    CURRENT_MODE_ADAPTATION_CHECKPOINT_VERSION,
)


def test_checkpoint_migrator_upgrades_h0_checkpoint_to_h1() -> None:
    migrator = CheckpointMigrator()
    checkpoint = ModeAdaptationCheckpoint(
        schema_version="phase_h0_v1",
        mode_adaptation_state=ModeAdaptationState(
            current_mode="worked_example_tutoring",
            blocks_in_current_mode=2,
            mode_changes_in_session=1,
            cooldown_blocks_remaining=1,
            last_observation_evidence=["transfer_success_two_blocks"],
        ),
    )

    migration = migrator.migrate_checkpoint(checkpoint)
    migrated = migration.checkpoint

    assert migrated.schema_version == CURRENT_MODE_ADAPTATION_CHECKPOINT_VERSION
    assert migrated.mode_adaptation_state.current_mode == "worked_example_tutoring"
    assert migrated.mode_adaptation_state.blocks_in_current_mode == 2
    assert migrated.mode_adaptation_state.mode_changes_in_session == 1
    assert migrated.mode_adaptation_state.cooldown_blocks_remaining == 1
    assert migrated.mode_adaptation_state.last_observation_evidence == [
        "transfer_success_two_blocks"
    ]
    assert [step.model_dump() for step in migration.steps] == [
        {
            "source_version": "phase_h0_v1",
            "target_version": CURRENT_MODE_ADAPTATION_CHECKPOINT_VERSION,
        }
    ]


def test_checkpoint_migrator_chains_h0_0_to_h1() -> None:
    migrator = CheckpointMigrator()
    checkpoint = ModeAdaptationCheckpoint(
        schema_version="phase_h0_v0",
        mode_adaptation_state=ModeAdaptationState(
            current_mode="worked_example_tutoring",
            blocks_in_current_mode=2,
            mode_changes_in_session=1,
            cooldown_blocks_remaining=1,
            last_observation_evidence=["legacy_signal_should_be_reset"],
        ),
    )

    migration = migrator.migrate_checkpoint(checkpoint)
    migrated = migration.checkpoint

    assert migrated.schema_version == CURRENT_MODE_ADAPTATION_CHECKPOINT_VERSION
    assert migrated.mode_adaptation_state.current_mode == "worked_example_tutoring"
    assert migrated.mode_adaptation_state.blocks_in_current_mode == 2
    assert migrated.mode_adaptation_state.mode_changes_in_session == 1
    assert migrated.mode_adaptation_state.cooldown_blocks_remaining == 1
    assert migrated.mode_adaptation_state.last_observation_evidence == []
    assert [step.model_dump() for step in migration.steps] == [
        {
            "source_version": "phase_h0_v0",
            "target_version": "phase_h0_v1",
        },
        {
            "source_version": "phase_h0_v1",
            "target_version": CURRENT_MODE_ADAPTATION_CHECKPOINT_VERSION,
        },
    ]


def test_checkpoint_migrator_is_idempotent_for_current_checkpoint() -> None:
    migrator = CheckpointMigrator()
    checkpoint = ModeAdaptationCheckpoint(
        schema_version=CURRENT_MODE_ADAPTATION_CHECKPOINT_VERSION,
        mode_adaptation_state=ModeAdaptationState(
            current_mode="guided_concept_explanation",
            blocks_in_current_mode=1,
            mode_changes_in_session=0,
        ),
    )

    migration = migrator.migrate_checkpoint(checkpoint)

    assert migration.checkpoint == checkpoint
    assert migration.steps == []


def test_checkpoint_migrator_rejects_unknown_version() -> None:
    migrator = CheckpointMigrator()
    checkpoint = ModeAdaptationCheckpoint(
        schema_version="phase_future_v99",
        mode_adaptation_state=ModeAdaptationState(
            current_mode="guided_concept_explanation",
            blocks_in_current_mode=1,
            mode_changes_in_session=0,
        ),
    )

    with pytest.raises(CheckpointMigrationError) as exc_info:
        migrator.migrate_checkpoint(checkpoint)

    assert "No migration path" in str(exc_info.value)
