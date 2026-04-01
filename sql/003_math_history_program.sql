create table if not exists knowledge.historical_era (
    id bigserial primary key,
    slug text not null unique,
    name text not null,
    sequence_no integer not null unique,
    focus text not null,
    created_at timestamptz not null default now()
);

create table if not exists knowledge.historical_figure (
    id bigserial primary key,
    slug text not null unique,
    historical_era_id bigint not null references knowledge.historical_era(id) on delete cascade,
    name text not null,
    region_label text,
    contribution_summary text not null,
    birth_year_label text,
    death_year_label text,
    created_at timestamptz not null default now()
);

create table if not exists knowledge.historical_work (
    id bigserial primary key,
    slug text not null unique,
    historical_era_id bigint not null references knowledge.historical_era(id) on delete cascade,
    historical_figure_id bigint references knowledge.historical_figure(id) on delete set null,
    title text not null,
    work_type text not null,
    contribution_summary text not null,
    created_at timestamptz not null default now()
);

create table if not exists knowledge.proof_story (
    id bigserial primary key,
    slug text not null unique,
    historical_era_id bigint not null references knowledge.historical_era(id) on delete cascade,
    title text not null,
    related_entity_type text,
    related_entity_slug text,
    story_focus text not null,
    origin_problem text,
    proof_summary text,
    transmission_summary text,
    created_at timestamptz not null default now()
);

create table if not exists knowledge.proof_story_artifact (
    id bigserial primary key,
    proof_story_id bigint not null references knowledge.proof_story(id) on delete cascade,
    artifact_label text not null,
    sort_order integer not null default 0,
    created_at timestamptz not null default now()
);

create table if not exists knowledge.equation_story (
    id bigserial primary key,
    slug text not null unique,
    historical_era_id bigint not null references knowledge.historical_era(id) on delete cascade,
    title text not null,
    related_equation_slug text,
    story_focus text not null,
    origin_summary text,
    notation_summary text,
    later_standard_form text,
    created_at timestamptz not null default now()
);

create index if not exists idx_historical_figure_era
    on knowledge.historical_figure (historical_era_id);

create index if not exists idx_historical_work_era
    on knowledge.historical_work (historical_era_id);

create index if not exists idx_proof_story_era
    on knowledge.proof_story (historical_era_id);

create index if not exists idx_equation_story_era
    on knowledge.equation_story (historical_era_id);
