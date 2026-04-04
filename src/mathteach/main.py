from fastapi import FastAPI

from mathteach.config import get_settings
from mathteach.models import SessionRequest
from mathteach.services.corpus import (
    build_chronology_program,
    build_corpus_blueprint,
    build_network_program,
    build_source_access_program,
)
from mathteach.services.foundation import build_foundation
from mathteach.services.planner import build_stack, build_teaching_plan
from mathteach.services.session_store import SessionStore

settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0")
session_store = SessionStore(settings.session_store_dir)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}


@app.get("/api/v1/stack")
def stack():
    return build_stack(settings)


@app.get("/api/v1/foundation")
def foundation():
    return build_foundation()


@app.get("/api/v1/corpus/blueprint")
def corpus_blueprint():
    return build_corpus_blueprint()


@app.get("/api/v1/corpus/chronology")
def corpus_chronology():
    return build_chronology_program()


@app.get("/api/v1/corpus/source-access")
def corpus_source_access():
    return build_source_access_program()


@app.get("/api/v1/corpus/network")
def corpus_network():
    return build_network_program()


@app.post("/api/v1/tutoring/plan")
def tutoring_plan(request: SessionRequest):
    planner_request = request

    if request.session_id is not None:
        stored_checkpoint = session_store.load_checkpoint(request.session_id)
        if stored_checkpoint is not None:
            planner_request = request.model_copy(
                update={
                    "session_id": None,
                    "mode_adaptation_checkpoint": stored_checkpoint,
                }
            )

    plan = build_teaching_plan(planner_request)

    if request.session_id is not None:
        session_store.save_checkpoint(request.session_id, plan.mode_adaptation_checkpoint)
        plan = plan.model_copy(update={"session_id": request.session_id})

    return plan
