import json
from functools import lru_cache
from pathlib import Path

from mathteach.models import (
    CollectionQueueItem,
    CorpusBlueprintResponse,
    CorpusDomain,
    SourceFamily,
)


def _manifest_path() -> Path:
    return Path(__file__).resolve().parents[3] / "data" / "math_core" / "foundation_manifest.json"


@lru_cache(maxsize=1)
def _load_manifest() -> dict:
    with _manifest_path().open("r", encoding="utf-8") as handle:
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
