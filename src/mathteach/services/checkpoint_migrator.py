from __future__ import annotations

from pydantic import BaseModel, Field

from mathteach.models import ModeAdaptationCheckpoint, ModeAdaptationState
from mathteach.services.checkpoint_validation import (
    CURRENT_MODE_ADAPTATION_CHECKPOINT_VERSION,
)


class CheckpointMigrationError(ValueError):
    pass


class CheckpointMigrationStep(BaseModel):
    source_version: str
    target_version: str


class CheckpointMigrationResult(BaseModel):
    checkpoint: ModeAdaptationCheckpoint
    steps: list[CheckpointMigrationStep] = Field(default_factory=list)


class CheckpointMigrator:
    def __init__(self) -> None:
        self._migration_chain = {
            "phase_h0_v0": "phase_h0_v1",
            "phase_h0_v1": CURRENT_MODE_ADAPTATION_CHECKPOINT_VERSION,
        }
        self._migration_functions = {
            ("phase_h0_v0", "phase_h0_v1"): self._migrate_h0_0_to_h0_1,
            ("phase_h0_v1", CURRENT_MODE_ADAPTATION_CHECKPOINT_VERSION): self._migrate_h0_to_h1,
        }

    def migrate_checkpoint(
        self,
        checkpoint: ModeAdaptationCheckpoint,
    ) -> CheckpointMigrationResult:
        current = checkpoint
        steps: list[CheckpointMigrationStep] = []

        if current.schema_version == CURRENT_MODE_ADAPTATION_CHECKPOINT_VERSION:
            return CheckpointMigrationResult(checkpoint=current, steps=steps)

        while current.schema_version != CURRENT_MODE_ADAPTATION_CHECKPOINT_VERSION:
            next_version = self._migration_chain.get(current.schema_version)
            if next_version is None:
                raise CheckpointMigrationError(
                    "No migration path from "
                    f"{current.schema_version} to "
                    f"{CURRENT_MODE_ADAPTATION_CHECKPOINT_VERSION}."
                )

            migration = self._migration_functions.get((current.schema_version, next_version))
            if migration is None:
                raise CheckpointMigrationError(
                    "Migration chain is incomplete for "
                    f"{current.schema_version} -> {next_version}."
                )

            source_version = current.schema_version
            current = migration(current)
            steps.append(
                CheckpointMigrationStep(
                    source_version=source_version,
                    target_version=current.schema_version,
                )
            )

        return CheckpointMigrationResult(checkpoint=current, steps=steps)

    def _migrate_h0_0_to_h0_1(
        self,
        checkpoint: ModeAdaptationCheckpoint,
    ) -> ModeAdaptationCheckpoint:
        if checkpoint.schema_version != "phase_h0_v0":
            raise CheckpointMigrationError(
                f"Cannot migrate {checkpoint.schema_version} with the h0.0-to-h0.1 path."
            )

        old_state = checkpoint.mode_adaptation_state

        # H.0.0 persisted only the core counters and current mode reliably.
        # H.0.1 introduced stable reason/evidence placeholders.
        migrated_state = ModeAdaptationState(
            current_mode=old_state.current_mode,
            blocks_in_current_mode=old_state.blocks_in_current_mode,
            mode_changes_in_session=old_state.mode_changes_in_session,
            last_change_reason=old_state.last_change_reason,
            cooldown_blocks_remaining=old_state.cooldown_blocks_remaining,
            pending_transition_message=None,
            last_observation_evidence=[],
        )

        return ModeAdaptationCheckpoint(
            schema_version="phase_h0_v1",
            mode_adaptation_state=migrated_state,
        )

    def _migrate_h0_to_h1(
        self,
        checkpoint: ModeAdaptationCheckpoint,
    ) -> ModeAdaptationCheckpoint:
        if checkpoint.schema_version != "phase_h0_v1":
            raise CheckpointMigrationError(
                f"Cannot migrate {checkpoint.schema_version} with the h0-to-h1 path."
            )

        old_state = checkpoint.mode_adaptation_state

        # H.0.1 already matches the H.1 core counters. H.1 keeps those values
        # and backfills later-added fields through the canonical state model.
        migrated_state = ModeAdaptationState(
            current_mode=old_state.current_mode,
            blocks_in_current_mode=old_state.blocks_in_current_mode,
            mode_changes_in_session=old_state.mode_changes_in_session,
            last_change_reason=old_state.last_change_reason,
            cooldown_blocks_remaining=old_state.cooldown_blocks_remaining,
            pending_transition_message=old_state.pending_transition_message,
            last_observation_evidence=list(old_state.last_observation_evidence),
        )

        return ModeAdaptationCheckpoint(
            schema_version=CURRENT_MODE_ADAPTATION_CHECKPOINT_VERSION,
            mode_adaptation_state=migrated_state,
        )
