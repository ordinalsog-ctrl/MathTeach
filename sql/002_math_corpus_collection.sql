create table if not exists knowledge.math_domain (
    id bigserial primary key,
    slug text not null unique,
    name text not null,
    priority_band text not null,
    goal text not null,
    created_at timestamptz not null default now()
);

create table if not exists knowledge.source_family (
    id bigserial primary key,
    slug text not null unique,
    name text not null,
    role_description text not null,
    created_at timestamptz not null default now()
);

create table if not exists knowledge.coverage_target (
    id bigserial primary key,
    math_domain_id bigint not null references knowledge.math_domain(id) on delete cascade,
    target_stage text not null,
    target_quality text not null,
    required_source_family_slugs text[] not null default '{}',
    created_at timestamptz not null default now()
);

create table if not exists knowledge.source_candidate (
    id bigserial primary key,
    slug text not null unique,
    title text not null,
    author_line text,
    source_family_id bigint references knowledge.source_family(id) on delete set null,
    candidate_status text not null default 'discovered',
    trust_level text not null default 'review_required',
    language_code text not null default 'en',
    notes text,
    created_at timestamptz not null default now()
);

create table if not exists knowledge.collection_queue (
    id bigserial primary key,
    slug text not null unique,
    priority_band text not null,
    queue_status text not null default 'planned',
    output_expectation text not null,
    domain_slugs text[] not null default '{}',
    source_family_slugs text[] not null default '{}',
    created_at timestamptz not null default now()
);

create table if not exists knowledge.ingestion_run (
    id bigserial primary key,
    source_candidate_id bigint references knowledge.source_candidate(id) on delete set null,
    run_status text not null default 'queued',
    extractor_name text not null,
    chunk_count integer,
    extracted_entity_count integer,
    notes text,
    started_at timestamptz,
    finished_at timestamptz,
    created_at timestamptz not null default now()
);

create index if not exists idx_math_domain_priority
    on knowledge.math_domain (priority_band);

create index if not exists idx_source_candidate_status
    on knowledge.source_candidate (candidate_status, trust_level);

create index if not exists idx_collection_queue_priority
    on knowledge.collection_queue (priority_band, queue_status);

create index if not exists idx_ingestion_run_status
    on knowledge.ingestion_run (run_status, created_at);
