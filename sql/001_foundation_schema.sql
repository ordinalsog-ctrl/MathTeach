create schema if not exists knowledge;
create schema if not exists teacher;

create table if not exists knowledge.source_document (
    id bigserial primary key,
    slug text not null unique,
    title text not null,
    authors text[] not null default '{}',
    publication_year integer,
    language_code text not null default 'en',
    document_type text not null,
    source_url text,
    trust_level text not null default 'standard',
    license_name text,
    created_at timestamptz not null default now()
);

create table if not exists knowledge.source_segment (
    id bigserial primary key,
    source_document_id bigint not null references knowledge.source_document(id) on delete cascade,
    segment_key text not null,
    page_label text,
    location_hint text,
    raw_text text not null,
    normalized_text text not null,
    created_at timestamptz not null default now(),
    unique (source_document_id, segment_key)
);

create table if not exists knowledge.concept (
    id bigserial primary key,
    slug text not null unique,
    name text not null,
    short_definition text not null,
    formal_definition text,
    intuition text,
    canonical_notation text,
    difficulty_band text not null,
    created_at timestamptz not null default now()
);

create table if not exists knowledge.equation (
    id bigserial primary key,
    slug text not null unique,
    name text not null,
    equation_latex text not null,
    equation_plain text,
    origin_note text,
    notation_notes text,
    created_at timestamptz not null default now()
);

create table if not exists knowledge.theorem (
    id bigserial primary key,
    slug text not null unique,
    name text not null,
    statement_text text not null,
    assumptions_text text,
    proof_sketch text,
    created_at timestamptz not null default now()
);

create table if not exists knowledge.application (
    id bigserial primary key,
    slug text not null unique,
    name text not null,
    domain_name text not null,
    summary text not null,
    modern_relevance text,
    created_at timestamptz not null default now()
);

create table if not exists knowledge.knowledge_edge (
    id bigserial primary key,
    from_entity_type text not null,
    from_entity_id bigint not null,
    relation_type text not null,
    to_entity_type text not null,
    to_entity_id bigint not null,
    weight numeric(6,3) not null default 1.000,
    created_at timestamptz not null default now()
);

create table if not exists knowledge.claim_evidence (
    id bigserial primary key,
    entity_type text not null,
    entity_id bigint not null,
    claim_label text not null,
    source_segment_id bigint not null references knowledge.source_segment(id) on delete cascade,
    evidence_role text not null default 'support',
    confidence numeric(4,3) not null default 1.000,
    created_at timestamptz not null default now()
);

create table if not exists teacher.teacher_profile (
    id bigserial primary key,
    slug text not null unique,
    name text not null,
    description text not null,
    tone_profile text not null,
    encouragement_style text not null,
    created_at timestamptz not null default now()
);

create table if not exists teacher.teaching_strategy (
    id bigserial primary key,
    slug text not null unique,
    name text not null,
    objective text not null,
    target_age_band text not null,
    target_confidence_band text not null,
    explanation_mode text not null,
    pacing_mode text not null,
    created_at timestamptz not null default now()
);

create table if not exists teacher.teacher_rule (
    id bigserial primary key,
    teacher_profile_id bigint not null references teacher.teacher_profile(id) on delete cascade,
    rule_type text not null,
    rule_text text not null,
    priority integer not null default 100,
    created_at timestamptz not null default now()
);

create table if not exists teacher.misconception_pattern (
    id bigserial primary key,
    slug text not null unique,
    concept_slug text not null,
    learner_signal text not null,
    diagnostic_question text not null,
    correction_strategy text not null,
    created_at timestamptz not null default now()
);

create table if not exists teacher.lesson_template (
    id bigserial primary key,
    slug text not null unique,
    name text not null,
    opening_move text not null,
    explanation_sequence jsonb not null default '[]'::jsonb,
    checkpoint_sequence jsonb not null default '[]'::jsonb,
    closing_move text not null,
    created_at timestamptz not null default now()
);

create index if not exists idx_source_segment_document
    on knowledge.source_segment (source_document_id);

create index if not exists idx_claim_evidence_entity
    on knowledge.claim_evidence (entity_type, entity_id);

create index if not exists idx_knowledge_edge_from
    on knowledge.knowledge_edge (from_entity_type, from_entity_id);

create index if not exists idx_knowledge_edge_to
    on knowledge.knowledge_edge (to_entity_type, to_entity_id);

create index if not exists idx_teacher_rule_profile
    on teacher.teacher_rule (teacher_profile_id, priority);
