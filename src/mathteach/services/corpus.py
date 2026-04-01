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
    ProofThread,
    SourceFamily,
)


def _manifest_path() -> Path:
    return Path(__file__).resolve().parents[3] / "data" / "math_core" / "foundation_manifest.json"


def _chronology_manifest_path() -> Path:
    return Path(__file__).resolve().parents[3] / "data" / "math_core" / "chronology_manifest.json"


@lru_cache(maxsize=1)
def _load_manifest() -> dict:
    with _manifest_path().open("r", encoding="utf-8") as handle:
        return json.load(handle)


@lru_cache(maxsize=1)
def _load_chronology_manifest() -> dict:
    with _chronology_manifest_path().open("r", encoding="utf-8") as handle:
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
