import json
from functools import lru_cache
from pathlib import Path

from mathteach.models import (
    CollectionQueueItem,
    ChronologyEra,
    ChronologyProgramResponse,
    CorpusBlueprintResponse,
    CorpusDomain,
    EquationThread,
    NetworkProgramResponse,
    NetworkTrack,
    NetworkAnchor,
    ProofThread,
    SourceAccessProgramResponse,
    SourceAccessRoute,
    SourceRegistryEntry,
    SourceFamily,
)


def _manifest_path() -> Path:
    return Path(__file__).resolve().parents[3] / "data" / "math_core" / "foundation_manifest.json"


def _chronology_manifest_path() -> Path:
    return Path(__file__).resolve().parents[3] / "data" / "math_core" / "chronology_manifest.json"


def _source_access_manifest_path() -> Path:
    return Path(__file__).resolve().parents[3] / "data" / "math_core" / "source_access_manifest.json"


def _network_manifest_path() -> Path:
    return Path(__file__).resolve().parents[3] / "data" / "math_core" / "network_manifest.json"


@lru_cache(maxsize=1)
def _load_manifest() -> dict:
    with _manifest_path().open("r", encoding="utf-8") as handle:
        return json.load(handle)


@lru_cache(maxsize=1)
def _load_chronology_manifest() -> dict:
    with _chronology_manifest_path().open("r", encoding="utf-8") as handle:
        return json.load(handle)


@lru_cache(maxsize=1)
def _load_source_access_manifest() -> dict:
    with _source_access_manifest_path().open("r", encoding="utf-8") as handle:
        return json.load(handle)


@lru_cache(maxsize=1)
def _load_network_manifest() -> dict:
    with _network_manifest_path().open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_corpus_blueprint() -> CorpusBlueprintResponse:
    manifest = _load_manifest()
    return CorpusBlueprintResponse(
        checked_on=manifest["checked_on"],
        mission=manifest["mission"],
        collection_principles=manifest["collection_principles"],
        domains=[CorpusDomain(**item) for item in manifest["domain_sequence"]],
        source_families=[SourceFamily(**item) for item in manifest["source_families"]],
        starter_collection_queue=[
            CollectionQueueItem(**item) for item in manifest["starter_collection_queue"]
        ],
        out_of_scope_for_now=manifest["out_of_scope_for_now"],
    )


def build_chronology_program() -> ChronologyProgramResponse:
    manifest = _load_chronology_manifest()
    return ChronologyProgramResponse(
        checked_on=manifest["checked_on"],
        mission=manifest["mission"],
        organizing_rule=manifest["organizing_rule"],
        eras=[
            ChronologyEra(
                slug=era["slug"],
                name=era["name"],
                sequence=era["sequence"],
                focus=era["focus"],
                canonical_figures=era["canonical_figures"],
                canonical_works=era["canonical_works"],
                proof_threads=[ProofThread(**item) for item in era["proof_threads"]],
                equation_threads=[EquationThread(**item) for item in era["equation_threads"]],
            )
            for era in manifest["eras"]
        ],
        collection_rules=manifest["collection_rules"],
    )


def build_source_access_program() -> SourceAccessProgramResponse:
    manifest = _load_source_access_manifest()
    return SourceAccessProgramResponse(
        checked_on=manifest["checked_on"],
        mission=manifest["mission"],
        storage_rule=manifest["storage_rule"],
        sources=[
            SourceRegistryEntry(
                slug=item["slug"],
                era=item["era"],
                title=item["title"],
                date_label=item["date_label"],
                figures=item["figures"],
                source_kind=item["source_kind"],
                significance=item["significance"],
                proof_or_equation_value=item["proof_or_equation_value"],
                rights_class=item["rights_class"],
                storage_class=item["storage_class"],
                storage_path_hint=item["storage_path_hint"],
                access_routes=[SourceAccessRoute(**route) for route in item["access_routes"]],
            )
            for item in manifest["sources"]
        ],
    )


def _build_network_tracks(items: list[dict]) -> list[NetworkTrack]:
    return [
        NetworkTrack(
            slug=item["slug"],
            title=item["title"],
            throughline=item["throughline"],
            eras=item["eras"],
            anchors=[NetworkAnchor(**anchor) for anchor in item["anchors"]],
            learner_value=item["learner_value"],
        )
        for item in items
    ]


def build_network_program() -> NetworkProgramResponse:
    manifest = _load_network_manifest()
    return NetworkProgramResponse(
        checked_on=manifest["checked_on"],
        mission=manifest["mission"],
        networking_principles=manifest["networking_principles"],
        proof_lines=_build_network_tracks(manifest["proof_lines"]),
        equation_lines=_build_network_tracks(manifest["equation_lines"]),
        transmission_paths=_build_network_tracks(manifest["transmission_paths"]),
        domain_lines=_build_network_tracks(manifest["domain_lines"]),
        application_bridges=_build_network_tracks(manifest["application_bridges"]),
        build_order=manifest["build_order"],
    )
