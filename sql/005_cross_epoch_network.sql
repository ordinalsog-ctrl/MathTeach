CREATE TYPE network_track_kind AS ENUM (
    'proof_line',
    'equation_line',
    'transmission_path',
    'domain_line',
    'application_bridge'
);

CREATE TABLE network_track (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug TEXT NOT NULL UNIQUE,
    kind network_track_kind NOT NULL,
    title TEXT NOT NULL,
    throughline TEXT NOT NULL,
    learner_value TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE network_track_era (
    id BIGSERIAL PRIMARY KEY,
    track_id UUID NOT NULL REFERENCES network_track(id) ON DELETE CASCADE,
    era_slug TEXT NOT NULL,
    sequence_index INTEGER NOT NULL,
    UNIQUE (track_id, era_slug)
);

CREATE TABLE network_anchor (
    id BIGSERIAL PRIMARY KEY,
    track_id UUID NOT NULL REFERENCES network_track(id) ON DELETE CASCADE,
    era_slug TEXT NOT NULL,
    label TEXT NOT NULL,
    anchor_type TEXT NOT NULL,
    contribution TEXT NOT NULL,
    sequence_index INTEGER NOT NULL
);

CREATE TABLE network_principle (
    id BIGSERIAL PRIMARY KEY,
    principle_text TEXT NOT NULL UNIQUE
);

CREATE INDEX network_track_kind_idx ON network_track(kind);
CREATE INDEX network_track_era_track_idx ON network_track_era(track_id, sequence_index);
CREATE INDEX network_anchor_track_idx ON network_anchor(track_id, sequence_index);
