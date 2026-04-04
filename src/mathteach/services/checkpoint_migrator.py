from __future__ import annotations

from mathteach.models import ModeAdaptationCheckpoint, ModeAdaptationState
from mathteach.services.checkpoint_validation import (
    CURRENT_MODE_ADAPTATION_CHECKPOINT_VERSION,
)


class CheckpointMigrationError(ValueError):
    pass


class CheckpointMigrator:
    def __init__(self) -> None:
        self._migration_paths = {
            "phase_h0_v1": self._migrate_h0_to_h1,
        }

    def migrate_checkpoint(
        self,
        checkpoint: ModeAdaptationCheckpoint,
    ) -> ModeAdaptationCheckpoint:
        if checkpoint.schema_version == CURRENT_MODE_ADAPTATION_CHECKPOINT_VERSION:
            return checkpoint

        migration = self._migration_paths.get(checkpoint.schema_version)
        if migration is None:
            raise CheckpointMigrationError(
                "No migration path from "
                f"{checkpoint.schema_version} to "
                f"{CURRENT_MODE_ADAPTATION_CHECKPOINT_VERSION}."
            )
        return migration(checkpoint)

    def _migrate_h0_to_h1(
        self,
        checkpoint: ModeAdaptationCheckpoint,
    ) -> ModeAdaptationCheckpoint:
        if checkpoint.schema_version != "phase_h0_v1":
            raise CheckpointMigrationError(
                f"Cannot migrate {checkpoint.schema_version} with the h0-to-h1 path."
            )

        old_state = checkpoint.mode_adaptation_state

        # H.0 persisted a subset of the current runtime state. H.1 keeps the
        # same core counters and backfills later-added fields through the
        # canonical state model defaults.
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
