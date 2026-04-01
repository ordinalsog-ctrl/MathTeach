create table if not exists knowledge.source_registry (
    id bigserial primary key,
    slug text not null unique,
    historical_era_slug text not null,
    title text not null,
    date_label text not null,
    source_kind text not null,
    significance text not null,
    proof_or_equation_value text not null,
    rights_class text not null,
    storage_class text not null,
    storage_path_hint text not null,
    created_at timestamptz not null default now()
);

create table if not exists knowledge.source_access_route (
    id bigserial primary key,
    source_registry_id bigint not null references knowledge.source_registry(id) on delete cascade,
    provider text not null,
    access_type text not null,
    url text not null,
    availability text not null,
    notes text,
    created_at timestamptz not null default now()
);

create table if not exists knowledge.source_storage_audit (
    id bigserial primary key,
    source_registry_id bigint not null references knowledge.source_registry(id) on delete cascade,
    raw_asset_present boolean not null default false,
    normalized_asset_present boolean not null default false,
    metadata_present boolean not null default false,
    rights_checked boolean not null default false,
    checksum_value text,
    notes text,
    created_at timestamptz not null default now()
);

create index if not exists idx_source_registry_era
    on knowledge.source_registry (historical_era_slug);

create index if not exists idx_source_access_route_source
    on knowledge.source_access_route (source_registry_id);

create index if not exists idx_source_storage_audit_source
    on knowledge.source_storage_audit (source_registry_id);
