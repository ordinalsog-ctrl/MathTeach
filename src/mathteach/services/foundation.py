from mathteach.models import FoundationLayer, FoundationResponse


def build_foundation() -> FoundationResponse:
    return FoundationResponse(
        architecture_name="Dual-Layer Teaching Intelligence",
        separation_principle=(
            "The factual math corpus and the pedagogical teacher mind are stored "
            "separately so teaching style can adapt without changing mathematical truth."
        ),
        knowledge_core=FoundationLayer(
            name="Knowledge Core",
            mission=(
                "Store mathematics as a sourceable, historically grounded, and "
                "structurally linked body of knowledge."
            ),
            stores=[
                "concepts",
                "equations",
                "theorems",
                "applications",
                "source documents",
                "source segments",
                "knowledge edges",
                "claim evidence",
            ],
            invariants=[
                "Every nontrivial claim must be traceable to evidence.",
                "Historical statements must remain source-bound.",
                "Uncertainty must be explicit and never hidden by style.",
                "Pedagogical tone cannot overwrite mathematical content.",
            ],
        ),
        teacher_mind=FoundationLayer(
            name="Teacher Mind",
            mission=(
                "Choose the best explanation strategy for a learner without becoming "
                "the authority on mathematical truth."
            ),
            stores=[
                "teacher profiles",
                "teaching strategies",
                "teacher rules",
                "misconception patterns",
                "lesson templates",
                "adaptation tactics by age, confidence, and pace",
            ],
            invariants=[
                "The teacher layer cannot invent sources.",
                "The teacher layer cannot change theorem meaning or prerequisites.",
                "Simplification is allowed only if correctness is preserved.",
                "Emotional support must not replace factual grounding.",
            ],
        ),
        handoff_contract=[
            "Retrieve facts, proofs, and history from the Knowledge Core first.",
            "Select framing, pacing, and intervention from the Teacher Mind second.",
            "Generate answers only after both layers are aligned.",
            "Evaluate both correctness and pedagogical fit after each response.",
        ],
        first_build_order=[
            "Build source catalog and segment-level citation storage.",
            "Extract concepts, equations, theorems, and applications.",
            "Add graph edges for prerequisites, derivations, and history.",
            "Model teaching strategies and misconception handling separately.",
            "Join both layers in the runtime tutor loop.",
        ],
    )
