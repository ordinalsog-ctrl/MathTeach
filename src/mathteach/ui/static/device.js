const STORAGE_KEY = "mathteach-device-shell";
const ONBOARDING_STEPS = ["goal", "presentation", "confirmation"];
const LINEAR_EQUATIONS_STATIONS = [
  "relationship_intro",
  "equation_form",
  "same_operation",
  "result",
  "similar_example",
];

const defaultState = {
  profile: {
    learnerName: "",
    ageGroup: "teen",
    mathLevel: "middle_school",
    preferredPace: "gentle",
    wantsVisuals: true,
    wantsHistory: false,
    supports: [],
    objective: "",
  },
  onboarding: {
    step: "goal",
  },
  sessionId: null,
  lastPlan: null,
  lastUpdatedAt: null,
};

const state = loadState();

document.addEventListener("DOMContentLoaded", () => {
  bindActions();
  bindOnboardingInputs();
  updateClock();
  window.setInterval(updateClock, 30_000);
  renderOnboarding();
  renderStartScreen();

  if (state.lastPlan) {
    renderLearningScreen(state.lastPlan, "default");
  }
});

function loadState() {
  const raw = window.localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    return structuredClone(defaultState);
  }
  try {
    return {
      ...structuredClone(defaultState),
      ...JSON.parse(raw),
      profile: {
        ...defaultState.profile,
        ...(JSON.parse(raw).profile || {}),
      },
      onboarding: {
        ...defaultState.onboarding,
        ...(JSON.parse(raw).onboarding || {}),
      },
    };
  } catch {
    return structuredClone(defaultState);
  }
}

function saveState() {
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function bindActions() {
  document.querySelectorAll("[data-action]").forEach((button) => {
    button.addEventListener("click", async () => {
      const action = button.getAttribute("data-action");
      if (action === "continue") {
        if (state.lastPlan) {
          switchScreen("learning");
          renderLearningScreen(state.lastPlan, "default");
          return;
        }
        openOnboarding("goal");
        return;
      }

      if (action === "onboarding") {
        openOnboarding("goal");
        return;
      }

      if (action === "reset-session") {
        state.sessionId = null;
        state.lastPlan = null;
        state.lastUpdatedAt = null;
        state.onboarding.step = "goal";
        saveState();
        renderOnboarding();
        renderStartScreen();
        switchScreen("start");
        return;
      }

      if (action === "onboarding-next") {
        await advanceOnboarding();
        return;
      }

      if (action === "onboarding-back") {
        retreatOnboarding();
        return;
      }

      if (action === "again") {
        await requestPlan(
          [{ evidence: ["repeated_concept_error", "text_overload"] }],
          "repeat"
        );
        return;
      }

      if (action === "example") {
        await requestPlan(
          [{ evidence: ["repeated_concept_error", "no_progress_two_blocks"] }],
          "example"
        );
        return;
      }

      if (action === "advance") {
        await requestPlan(
          [{ evidence: ["visible_small_success", "transfer_success"] }],
          "advance"
        );
      }
    });
  });
}

function bindOnboardingInputs() {
  const objectiveInput = document.querySelector("[data-role='onboarding-objective']");

  objectiveInput?.addEventListener("input", (event) => {
    state.profile.objective = event.target.value;
    saveState();
    clearOnboardingValidation();
    if (normalizeOnboardingStep(state.onboarding?.step) === "confirmation") {
      renderOnboarding();
    }
  });

  objectiveInput?.addEventListener("keydown", async (event) => {
    if (event.key !== "Enter" || event.shiftKey) {
      return;
    }
    if (normalizeOnboardingStep(state.onboarding?.step) !== "goal") {
      return;
    }
    event.preventDefault();
    await advanceOnboarding();
  });

  document.querySelectorAll("[data-choice='presentation']").forEach((option) => {
    option.addEventListener("click", () => {
      state.profile.wantsVisuals = option.dataset.value === "visual";
      saveState();
      clearOnboardingValidation();
      renderOnboarding({ shouldFocus: false });
    });
  });
}

function renderOnboarding({ shouldFocus = false } = {}) {
  const step = normalizeOnboardingStep(state.onboarding?.step);
  const meta = onboardingMeta(step);
  const objectiveInput = document.querySelector("[data-role='onboarding-objective']");
  const secondaryAction = document.querySelector("[data-role='onboarding-secondary-action']");

  document.querySelectorAll(".onboarding-step[data-onboarding-step]").forEach((node) => {
    node.classList.toggle("is-hidden", node.dataset.onboardingStep !== step);
  });

  if (objectiveInput && objectiveInput.value !== state.profile.objective) {
    objectiveInput.value = state.profile.objective;
  }

  document.querySelectorAll("[data-choice='presentation']").forEach((option) => {
    option.classList.toggle(
      "is-active",
      (state.profile.wantsVisuals && option.dataset.value === "visual") ||
        (!state.profile.wantsVisuals && option.dataset.value === "words")
    );
  });

  text("[data-role='onboarding-screen-label']", meta.label);
  text("[data-role='onboarding-step-indicator']", meta.indicator);
  text("[data-role='onboarding-primary-action']", meta.primaryAction);
  text("[data-role='onboarding-secondary-action']", meta.secondaryAction);
  text("[data-role='onboarding-summary']", buildOnboardingSummary());

  if (secondaryAction) {
    secondaryAction.hidden = Boolean(meta.hideSecondaryAction);
  }

  const screen = document.querySelector("[data-screen='onboarding']");
  if (screen) {
    screen.dataset.onboardingStep = step;
  }

  if (step !== "goal") {
    clearOnboardingValidation();
  }

  if (shouldFocus) {
    window.requestAnimationFrame(() => applyOnboardingFocus(step));
  }
}

async function advanceOnboarding() {
  const step = normalizeOnboardingStep(state.onboarding?.step);

  if (step === "goal") {
    const objective = document
      .querySelector("[data-role='onboarding-objective']")
      ?.value.trim();

    if (!objective) {
      setOnboardingValidation("Schreib nur kurz, womit wir anfangen sollen.");
      document.querySelector("[data-role='onboarding-objective']")?.focus();
      return;
    }

    state.profile.objective = objective;
    saveState();
    setOnboardingStep("presentation");
    return;
  }

  if (step === "presentation") {
    setOnboardingStep("confirmation");
    return;
  }

  if (step === "confirmation") {
    clearOnboardingValidation();
    state.sessionId = state.sessionId || buildSessionId();
    saveState();
    await requestPlan([]);
  }
}

function retreatOnboarding() {
  const step = normalizeOnboardingStep(state.onboarding?.step);

  if (step === "goal") {
    clearOnboardingValidation();
    switchScreen("start");
    return;
  }

  if (step === "presentation") {
    setOnboardingStep("goal");
    return;
  }

  setOnboardingStep("presentation");
}

function openOnboarding(step = "goal") {
  state.onboarding.step = normalizeOnboardingStep(step);
  saveState();
  clearOnboardingValidation();
  switchScreen("onboarding");
  renderOnboarding({ shouldFocus: true });
}

function setOnboardingStep(step) {
  state.onboarding.step = normalizeOnboardingStep(step);
  saveState();
  clearOnboardingValidation();
  renderOnboarding({ shouldFocus: true });
}

function normalizeOnboardingStep(step) {
  return ONBOARDING_STEPS.includes(step) ? step : "goal";
}

function onboardingMeta(step) {
  if (step === "presentation") {
    return {
      label: "Naechster Schritt",
      indicator: "2 von 3",
      primaryAction: "Weiter",
      secondaryAction: "Zurueck",
    };
  }

  if (step === "confirmation") {
    return {
      label: "Dann starten wir",
      indicator: "3 von 3",
      primaryAction: "Jetzt starten",
      secondaryAction: "Zurueck",
    };
  }

  return {
    label: "Erster Schritt",
    indicator: "1 von 3",
    primaryAction: "Weiter",
    secondaryAction: "Zurueck zum Start",
  };
}

function buildOnboardingSummary() {
  const topic = compactOnboardingTopic(state.profile.objective) || "Ruhiger Einstieg";
  const presentation = state.profile.wantsVisuals
    ? "zuerst mit Bild"
    : "zuerst mit Worten";
  return `${topic}, ${presentation}.`;
}

function compactOnboardingTopic(value) {
  const normalized = String(value || "")
    .replace(/\s+/g, " ")
    .trim()
    .replace(/[.!?]+$/g, "");

  if (!normalized) {
    return "";
  }

  if (normalized.length <= 44) {
    return normalized;
  }

  return `${normalized.slice(0, 41).trimEnd()}...`;
}

function applyOnboardingFocus(step) {
  if (step === "goal") {
    document.querySelector("[data-role='onboarding-objective']")?.focus();
    return;
  }

  if (step === "presentation") {
    document
      .querySelector("[data-choice='presentation'].is-active")
      ?.focus();
    return;
  }

  document.querySelector("[data-role='onboarding-primary-action']")?.focus();
}

function setOnboardingValidation(message) {
  const node = document.querySelector("[data-role='onboarding-validation']");
  if (!node) {
    return;
  }
  node.hidden = !message;
  node.textContent = message;
}

function clearOnboardingValidation() {
  setOnboardingValidation("");
}

async function requestPlan(runtimeObservations, actionTone = "default") {
  if (!state.profile.objective?.trim()) {
    openOnboarding("goal");
    return;
  }

  if (matchesLinearEquationsPilot(state.profile.objective)) {
    const localPlan = buildLinearEquationsPilotPlan(actionTone);
    state.sessionId = state.sessionId || buildSessionId();
    state.lastPlan = localPlan;
    state.lastUpdatedAt = new Date().toISOString();
    saveState();
    renderStartScreen();
    renderLearningScreen(localPlan, actionTone);
    switchScreen("learning");
    return;
  }

  const payload = {
    objective: state.profile.objective,
    session_id: state.sessionId || buildSessionId(),
    learner_profile: {
      age_group: state.profile.ageGroup,
      math_level: state.profile.mathLevel,
      confidence: "low",
      preferred_pace: state.profile.preferredPace,
      language: "de",
      wants_visuals: state.profile.wantsVisuals,
      wants_history: state.profile.wantsHistory,
      declared_support_needs: state.profile.supports,
    },
    runtime_observations: runtimeObservations,
  };

  state.sessionId = payload.session_id;
  saveState();
  setStatus(buildLessonRequestMessage(actionTone));

  try {
    const response = await window.fetch("/api/v1/tutoring/plan", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`Plan request failed: ${response.status}`);
    }

    const plan = await response.json();
    state.lastPlan = plan;
    state.lastUpdatedAt = new Date().toISOString();
    saveState();
    renderStartScreen();
    renderLearningScreen(plan, actionTone);
    switchScreen("learning");
  } catch (error) {
    setStatus(buildLessonFailureMessage(actionTone));
    console.error(error);
  }
}

function renderStartScreen() {
  const input = collectStartscreenInput();
  const normalized = normalizeStartscreenInput(input);
  const stateKind = resolveStartscreenState(normalized);
  const slots = buildStartscreenSlots(stateKind, normalized);

  renderStartscreenResolved({
    state_kind: stateKind,
    slots,
  });
}

function renderLearningScreen(plan, actionTone = "default") {
  const activeBlock = pickActiveBlock(plan);
  const carrierTone = resolveLearningCarrierTone(activeBlock, actionTone);
  text("[data-role='lesson-goal']", activeBlock.goal || state.profile.objective);
  text("[data-role='lesson-transition']", buildLessonTransition(activeBlock));
  text("[data-role='board-label']", buildBoardLabel(activeBlock, carrierTone));
  text("[data-role='board-meaning']", buildBoardMeaning(activeBlock, carrierTone));
  renderBoardMath(activeBlock, carrierTone);
  text("[data-role='board-action-cue']", buildBoardActionCue(activeBlock, carrierTone));
  text("[data-role='visual-hint']", buildVisualHint(activeBlock, carrierTone));
  renderBoardRecoveryNote(activeBlock, carrierTone);
  renderLearningCarrierState(carrierTone);
  text(
    "[data-role='focus-note']",
    buildFocusNote(activeBlock)
  );
  text(
    "[data-role='scaffold-note']",
    buildScaffoldNote(activeBlock)
  );
  renderLearningActions(activeBlock);
}

function resolveLearningCarrierTone(block, actionTone) {
  if (isLinearEquationsPilotBlock(block)) {
    return block.device_variant || "default";
  }

  if (actionTone === "repeat") {
    return "repeat";
  }

  if (actionTone === "example" || block?.block_type === "worked_example") {
    return "example";
  }

  return "default";
}

function buildBoardLabel(block, carrierTone) {
  if (isLinearEquationsPilotBlock(block)) {
    return block.device_board_label || "Visueller Einstieg";
  }

  if (carrierTone === "repeat") {
    return "Noch kleinerer Schritt";
  }

  if (carrierTone === "example") {
    return block?.block_type === "worked_example"
      ? "Aehnliches Beispiel"
      : "Aehnlicher Schritt";
  }

  return "Visueller Einstieg";
}

function renderBoardMath(block, carrierTone) {
  const structure = buildBoardStructure(block, carrierTone);
  text("[data-role='board-left']", structure.primary_left);
  text("[data-role='board-right']", structure.primary_right);
  text("[data-role='board-left-operation']", structure.operation_left);
  text("[data-role='board-right-operation']", structure.operation_right);
  text("[data-role='board-left-result']", structure.result_left);
  text("[data-role='board-right-result']", structure.result_right);

  const operationRow = document.querySelector("[data-role='board-operation-row']");
  const resultRow = document.querySelector("[data-role='board-result-row']");

  if (operationRow) {
    operationRow.hidden = !structure.show_operation;
  }

  if (resultRow) {
    resultRow.hidden = !structure.show_result;
  }
}

function buildBoardStructure(block, carrierTone) {
  if (isLinearEquationsPilotBlock(block) && block.device_board_structure) {
    return block.device_board_structure;
  }

  if (carrierTone === "repeat") {
    return {
      primary_left: "x + 3",
      primary_right: "7",
      operation_left: "- 3",
      operation_right: "- 3",
      result_left: "x",
      result_right: "4",
      show_operation: true,
      show_result: true,
    };
  }

  if (carrierTone === "example") {
    return {
      primary_left: "5 + 2",
      primary_right: "7",
      operation_left: "- 2",
      operation_right: "- 2",
      result_left: "5",
      result_right: "5",
      show_operation: true,
      show_result: true,
    };
  }

  return {
    primary_left: "x + 3",
    primary_right: "7",
    operation_left: "",
    operation_right: "",
    result_left: "",
    result_right: "",
    show_operation: false,
    show_result: false,
  };
}

function renderBoardRecoveryNote(block, carrierTone) {
  const node = document.querySelector("[data-role='board-recovery-note']");
  if (!node) {
    return;
  }

  const note = buildBoardRecoveryNote(block, carrierTone);
  node.hidden = !note;
  node.textContent = note;
}

function buildBoardRecoveryNote(block, carrierTone) {
  if (isLinearEquationsPilotBlock(block)) {
    return block.device_board_recovery_note || "";
  }

  if (carrierTone === "repeat") {
    return "Wir verkleinern nur diesen einen Zug.";
  }

  if (carrierTone === "example") {
    return block?.block_type === "worked_example"
      ? "Wir halten dieselbe Regel erst an einem nahen Beispiel fest."
      : "Wir sehen dieselbe Struktur erst an einem aehnlichen Schritt.";
  }

  return "";
}

function renderLearningCarrierState(carrierTone) {
  const board = document.querySelector("[data-role='visual-board']");
  if (board) {
    board.dataset.learningTone = carrierTone;
  }

  const math = document.querySelector("[data-role='board-math']");
  if (math) {
    math.dataset.learningTone = carrierTone;
  }
}

function pickActiveBlock(plan) {
  if (!plan || !Array.isArray(plan.planned_blocks) || plan.planned_blocks.length === 0) {
    return {
      goal: state.profile.objective,
      focus: [],
      support_moves: [],
      support_scaffolds: [],
      block_type: null,
      transition_message: null,
    };
  }

  if (Array.isArray(plan.planned_blocks) && plan.planned_blocks.length > 0) {
    return plan.planned_blocks[0];
  }
}

function buildLessonTransition(block) {
  return (
    block.transition_message ||
    "Wir schauen auf genau einen kleinen Schritt und koennen danach ruhig weitergehen."
  );
}

function buildBoardMeaning(block, carrierTone = "default") {
  if (isLinearEquationsPilotBlock(block)) {
    return (
      block.device_board_meaning ||
      "Beide Seiten gehoeren zusammen und muessen im Gleichgewicht bleiben."
    );
  }

  if (carrierTone === "repeat") {
    return "Wir schauen nur auf eine Sache: Was wir links tun, tun wir auch rechts.";
  }

  if (carrierTone === "example") {
    return "Wir halten dieselbe Beziehung erst klein und klar fest, bevor wir wieder zum eigentlichen Schritt gehen.";
  }

  if (Array.isArray(block.focus) && block.focus.length > 0) {
    return "Wir halten die zugrunde liegende Beziehung zuerst sichtbar, bevor wir nur auf Symbole schauen.";
  }

  return "Beide Seiten gehoeren zusammen und muessen im Gleichgewicht bleiben.";
}

function buildBoardActionCue(block, carrierTone = "default") {
  if (isLinearEquationsPilotBlock(block)) {
    return (
      block.device_board_action_cue ||
      "Darum machen wir denselben kleinen Zug links und rechts."
    );
  }

  if (carrierTone === "repeat") {
    return "Noch kleiner: erst beide Seiten sehen, dann denselben Zug links und rechts machen.";
  }

  if (carrierTone === "example") {
    return "Wir nehmen dieselbe Regel in einen aehnlichen Zug mit, damit der naechste Schritt leichter lesbar wird.";
  }

  if (Array.isArray(block.support_scaffolds) && block.support_scaffolds.length > 0) {
    return "Wir machen denselben kleinen Zug links und rechts, damit die Beziehung stabil bleibt.";
  }

  return "Darum machen wir denselben kleinen Zug links und rechts.";
}

function renderLearningActions(block) {
  const labels = buildLearningActionLabels(block);
  text("[data-role='lesson-repeat-action']", labels.repeat);
  text("[data-role='lesson-example-action']", labels.example);
  text("[data-role='lesson-advance-action']", labels.advance);
}

function buildLearningActionLabels(block) {
  if (isLinearEquationsPilotBlock(block) && block.device_action_labels) {
    return block.device_action_labels;
  }

  if (block?.block_type === "worked_example") {
    return {
      repeat: "Zeig diesen Schritt noch einmal",
      example: "Zeig mir noch ein Beispiel",
      advance: "Zum naechsten Schritt",
    };
  }

  return {
    repeat: "Diesen Schritt noch einmal sehen",
    example: "Zeig mir ein Beispiel",
    advance: "Zum naechsten Schritt",
  };
}

function firstLearningNote(items, fallback) {
  if (Array.isArray(items) && items.length > 0) {
    return prettify(items[0]);
  }
  return fallback;
}

function buildLessonRequestMessage(actionTone) {
  if (actionTone === "repeat") {
    return "Lass uns genau diesen Schritt noch einmal kleiner aufmachen.";
  }

  if (actionTone === "example") {
    return "Ich suche jetzt ein Beispiel fuer genau diesen Schritt.";
  }

  if (actionTone === "advance") {
    return "Ich bereite den naechsten kleinen Schritt fuer dich vor.";
  }

  return "Ich bereite den naechsten Schritt fuer dich vor ...";
}

function buildLessonFailureMessage(actionTone) {
  if (actionTone === "repeat") {
    return "Wir konnten genau diesen Schritt gerade nicht noch einmal aufbauen. Wir koennen es gleich wieder versuchen.";
  }

  if (actionTone === "example") {
    return "Das Beispiel konnte gerade nicht geladen werden. Wir koennen es gleich noch einmal versuchen.";
  }

  if (actionTone === "advance") {
    return "Der naechste kleine Schritt konnte gerade nicht geladen werden. Wir koennen es gleich noch einmal versuchen.";
  }

  return "Der lokale Plan konnte gerade nicht geladen werden. Wir koennen es gleich noch einmal versuchen.";
}

function setStatus(message) {
  const onboardingScreen = document.querySelector("[data-screen='onboarding']");
  if (onboardingScreen && !onboardingScreen.classList.contains("is-hidden")) {
    setOnboardingValidation(message);
    return;
  }

  text("[data-role='lesson-transition']", message);
}

function collectStartscreenInput() {
  return {
    learnerName: state.profile.learnerName,
    sessionId: state.sessionId,
    lastPlan: state.lastPlan,
    lastUpdatedAt: state.lastUpdatedAt,
    resumeContext: state.lastPlan?.resume_context ?? null,
    resumeBlock: pickStartscreenResumeBlock(state.lastPlan),
  };
}

function normalizeStartscreenInput(input) {
  const resumeContext = input.resumeContext;
  const resumeBlock = input.resumeBlock;

  return {
    ...input,
    has_name: Boolean(input.learnerName),
    has_last_plan: Boolean(input.lastPlan),
    has_resume_context: Boolean(resumeContext),
    resume_active: Boolean(resumeContext?.resume_active),
    resume_source: resumeContext?.resume_source || "fresh_start",
    has_first_block: Boolean(resumeBlock),
    has_resume_goal: Boolean(resumeBlock?.goal),
    has_resume_transition_message: Boolean(resumeBlock?.transition_message),
    has_explicit_unsafe_signal: hasExplicitUnsafeSignal(input),
  };
}

function resolveStartscreenState(normalized) {
  if (normalized.has_explicit_unsafe_signal) {
    return "unsafe_history";
  }

  if (
    normalized.resume_active ||
    (normalized.has_last_plan && normalized.has_first_block && normalized.has_resume_goal)
  ) {
    return "resume";
  }

  return "no_history";
}

function buildStartscreenSlots(stateKind, normalized) {
  if (stateKind === "unsafe_history") {
    return buildUnsafeHistoryStartscreenSlots(normalized);
  }
  if (stateKind === "resume") {
    return buildResumeStartscreenSlots(normalized);
  }
  return buildNoHistoryStartscreenSlots(normalized);
}

function buildResumeStartscreenSlots(normalized) {
  const block = normalized.resumeBlock;
  return {
    welcome_line: normalized.has_name
      ? `${normalized.learnerName}, wir lernen in deinem Tempo.`
      : "Wir lernen in deinem Tempo.",
    support_line: "Du kannst genau hier mit einem kleinen Schritt weitermachen.",
    resume_label: "Letzter Stand",
    resume_title:
      block?.goal || state.profile.objective || "Letzte Lerneinheit",
    resume_summary: buildResumeSummary(normalized),
    primary_cta_label: "Weiterlernen",
    secondary_action_label: "Neues Profil einrichten",
    secondary_action: "onboarding",
  };
}

function buildNoHistoryStartscreenSlots(normalized) {
  return {
    welcome_line: normalized.has_name
      ? `${normalized.learnerName}, wir lernen in deinem Tempo.`
      : "Wir lernen in deinem Tempo.",
    support_line: "Wir koennen mit einem kleinen ersten Schritt anfangen.",
    resume_label: "Erster Schritt",
    resume_title: "Wir beginnen mit einem ruhigen Einstieg.",
    resume_summary: "Du musst noch nichts koennen oder vorbereiten.",
    primary_cta_label: "Jetzt anfangen",
    secondary_action_label: "Profil einrichten",
    secondary_action: "onboarding",
  };
}

function buildUnsafeHistoryStartscreenSlots(normalized) {
  return {
    welcome_line: normalized.has_name
      ? `${normalized.learnerName}, wir steigen ruhig wieder ein.`
      : "Wir steigen ruhig wieder ein.",
    support_line: "Wir nehmen einfach den letzten sicheren Schritt.",
    resume_label: "Sicherer Wiedereinstieg",
    resume_title: "Wir machen beim letzten sicheren Schritt weiter.",
    resume_summary: "Wir setzen an einem stabilen Punkt wieder an.",
    primary_cta_label: "Sicher weitermachen",
    secondary_action_label: "Neu beginnen",
    secondary_action: "reset-session",
  };
}

function buildResumeSummary(normalized) {
  if (normalized.resumeBlock?.transition_message) {
    return normalized.resumeBlock.transition_message;
  }

  const updated = formatStartscreenTimestamp(normalized.lastUpdatedAt);
  return `Letzte lokale Session: ${updated}. Du kannst ohne Neuaufsetzen wieder an derselben Stelle anfangen.`;
}

function renderStartscreenResolved(resolved) {
  const startScreen = document.querySelector("[data-screen='start']");
  const secondaryAction = document.querySelector("[data-role='start-secondary-action']");

  if (startScreen) {
    startScreen.dataset.startscreenState = resolved.state_kind;
  }

  text("[data-role='welcome-name']", resolved.slots.welcome_line);
  text("[data-role='start-support-line']", resolved.slots.support_line);
  text("[data-role='resume-label']", resolved.slots.resume_label);
  text("[data-role='resume-topic']", resolved.slots.resume_title);
  text("[data-role='resume-summary']", resolved.slots.resume_summary);
  text("[data-role='start-primary-action']", resolved.slots.primary_cta_label);

  if (secondaryAction) {
    secondaryAction.hidden = !resolved.slots.secondary_action_label;
    if (!secondaryAction.hidden) {
      secondaryAction.textContent = resolved.slots.secondary_action_label;
      secondaryAction.dataset.action = resolved.slots.secondary_action || "onboarding";
    }
  }
}

function pickStartscreenResumeBlock(plan) {
  if (!plan || !Array.isArray(plan.planned_blocks) || plan.planned_blocks.length === 0) {
    return null;
  }
  return plan.planned_blocks[0];
}

function hasExplicitUnsafeSignal(input) {
  const resumeContext = input.resumeContext;
  if (!resumeContext) {
    return false;
  }

  return (
    resumeContext.resume_status === "unsafe_history" ||
    resumeContext.resume_recovery_required === true
  );
}

function formatStartscreenTimestamp(timestamp) {
  if (!timestamp) {
    return "gerade eben";
  }

  return new Date(timestamp).toLocaleString("de-DE", {
    day: "2-digit",
    month: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function buildSessionId() {
  if (window.crypto && typeof window.crypto.randomUUID === "function") {
    return `device-${window.crypto.randomUUID()}`;
  }
  return `device-${Date.now()}`;
}

function switchScreen(screenName) {
  document.querySelectorAll("[data-screen]").forEach((screen) => {
    screen.classList.toggle("is-hidden", screen.dataset.screen !== screenName);
  });
}

function text(selector, value) {
  const node = document.querySelector(selector);
  if (node) {
    node.textContent = value;
  }
}

function updateClock() {
  const now = new Date();
  text(
    "[data-role='clock']",
    now.toLocaleTimeString("de-DE", { hour: "2-digit", minute: "2-digit" })
  );
}

function buildVisualHint(block, carrierTone = "default") {
  if (isLinearEquationsPilotBlock(block)) {
    return (
      block.device_visual_hint ||
      "Wir behandeln beide Seiten derselben Gleichung mit der gleichen Ruhe."
    );
  }

  if (carrierTone === "repeat") {
    return "Wenn es stockt, machen wir den Schritt kleiner statt die Flaeche groesser.";
  }

  if (carrierTone === "example") {
    return "Das Beispiel soll nur dieselbe Struktur zeigen, nicht ein neues Thema aufmachen.";
  }

  if (Array.isArray(block.focus) && block.focus.length > 0) {
    return `Wir schauen jetzt besonders auf: ${prettify(block.focus[0])}.`;
  }
  return "Wir behandeln beide Seiten derselben Gleichung mit der gleichen Ruhe.";
}

function prettify(value) {
  return String(value)
    .replaceAll("_", " ")
    .replace(/\b\w/g, (match) => match.toUpperCase());
}

function buildFocusNote(block) {
  if (isLinearEquationsPilotBlock(block) && block.device_focus_note) {
    return block.device_focus_note;
  }

  return firstLearningNote(
    block.focus,
    "Wir halten nur den naechsten Gedanken auf dem Bildschirm."
  );
}

function buildScaffoldNote(block) {
  if (isLinearEquationsPilotBlock(block) && block.device_scaffold_note) {
    return block.device_scaffold_note;
  }

  return firstLearningNote(
    block.support_scaffolds,
    firstLearningNote(
      block.support_moves,
      "Bei Bedarf gehe ich noch einen Schritt kleiner."
    )
  );
}

function matchesLinearEquationsPilot(objective) {
  const normalized = String(objective || "").toLowerCase();
  return (
    normalized.includes("lineare gleichung") ||
    normalized.includes("lineare gleichungen") ||
    normalized.includes("x + 3 = 7")
  );
}

function isLinearEquationsPilotBlock(block) {
  return block?.device_module_slug === "linear_equations_pilot";
}

function buildLinearEquationsPilotPlan(actionTone = "default") {
  const currentStage = getCurrentLinearEquationsStage();
  const nextStage = resolveLinearEquationsStage(currentStage, actionTone);
  const variant = resolveLinearEquationsVariant(nextStage, actionTone);
  const stageConfig = buildLinearEquationsStage(nextStage, variant);
  const sessionId = state.sessionId || buildSessionId();

  return {
    session_id: sessionId,
    lesson_mode: "device_linear_equations_pilot",
    audience_mode: "teen",
    planned_blocks: [
      {
        mode: "device_linear_equations_pilot",
        block_type: stageConfig.block_type,
        goal: stageConfig.goal,
        transition_message: stageConfig.transition_message,
        focus: stageConfig.focus,
        support_moves: stageConfig.support_moves,
        support_scaffolds: stageConfig.support_scaffolds,
        device_module_slug: "linear_equations_pilot",
        device_stage: nextStage,
        device_variant: variant,
        device_focus_note: stageConfig.focus_note,
        device_scaffold_note: stageConfig.scaffold_note,
        device_board_label: stageConfig.board_label,
        device_board_meaning: stageConfig.board_meaning,
        device_board_action_cue: stageConfig.board_action_cue,
        device_board_recovery_note: stageConfig.board_recovery_note,
        device_board_structure: stageConfig.board_structure,
        device_visual_hint: stageConfig.visual_hint,
        device_action_labels: stageConfig.action_labels,
      },
    ],
    resume_context: {
      resume_source: state.lastPlan ? "local_module_resume" : "fresh_start",
      resume_active: Boolean(state.lastPlan),
    },
  };
}

function getCurrentLinearEquationsStage() {
  const block = pickActiveBlock(state.lastPlan);
  if (!isLinearEquationsPilotBlock(block)) {
    return "relationship_intro";
  }
  return block.device_stage || "relationship_intro";
}

function resolveLinearEquationsStage(currentStage, actionTone) {
  if (actionTone === "example") {
    return currentStage === "relationship_intro" ? "equation_form" : "similar_example";
  }

  if (actionTone === "repeat") {
    return currentStage;
  }

  const currentIndex = LINEAR_EQUATIONS_STATIONS.indexOf(currentStage);
  if (currentIndex === -1) {
    return "relationship_intro";
  }

  return LINEAR_EQUATIONS_STATIONS[Math.min(currentIndex + 1, LINEAR_EQUATIONS_STATIONS.length - 1)];
}

function resolveLinearEquationsVariant(stage, actionTone) {
  if (stage === "similar_example") {
    return "example";
  }

  if (actionTone === "repeat" && stage !== "relationship_intro") {
    return "repeat";
  }

  return "default";
}

function buildLinearEquationsStage(stage, variant) {
  if (stage === "equation_form") {
    return {
      block_type: "worked_example",
      goal: "Wir sehen dieselbe Beziehung jetzt als kleine Gleichung.",
      transition_message: "Jetzt sehen wir dieselbe Beziehung als x + 3 = 7.",
      focus: ["meaning_before_symbol"],
      support_moves: ["bind_symbol_back_to_relationship"],
      support_scaffolds: ["single_equation_only"],
      focus_note: "Wir binden x + 3 = 7 direkt an dieselbe sichtbare Beziehung zurueck.",
      scaffold_note: "Nur eine Gleichung, noch kein neuer Rechenschritt.",
      board_label: "Dieselbe Beziehung als Gleichung",
      board_meaning:
        "x steht fuer den Teil, den wir noch nicht kennen. Die drei kommen links dazu. Rechts steht sieben gegenueber.",
      board_action_cue: "Wenn die Beziehung klar ist, koennen wir spaeter den gleichen Zug auf beiden Seiten sehen.",
      board_recovery_note:
        variant === "repeat" ? "Wir bleiben bei derselben Gleichung und schauen nur ruhiger hin." : "",
      board_structure: {
        primary_left: "x + 3",
        primary_right: "7",
        operation_left: "",
        operation_right: "",
        result_left: "",
        result_right: "",
        show_operation: false,
        show_result: false,
      },
      visual_hint:
        "Noch kein Trick. Erst dieselbe Beziehung als lesbare Gleichung.",
      action_labels: {
        repeat: "Diesen Schritt noch einmal sehen",
        example: "Zeig die gleiche Idee noch einmal",
        advance: "Den gleichen Zug auf beiden Seiten sehen",
      },
    };
  }

  if (stage === "same_operation") {
    return {
      block_type: "worked_example",
      goal: "Wir machen denselben kleinen Zug auf beiden Seiten.",
      transition_message:
        "Wenn die Beziehung gleich bleiben soll, braucht es links und rechts denselben Zug.",
      focus: ["same_operation_both_sides"],
      support_moves: ["keep_relationship_stable"],
      support_scaffolds: ["single_operation_row"],
      focus_note: "Nur dieser eine Gedanke zaehlt jetzt: links und rechts derselbe Zug.",
      scaffold_note: "Wir fuehren genau eine Operationsspur ein, nicht mehr.",
      board_label:
        variant === "repeat" ? "Derselbe Zug noch kleiner" : "Derselbe Zug auf beiden Seiten",
      board_meaning:
        "Wir nehmen nicht irgendwo etwas weg. Wir halten die Beziehung im Gleichgewicht.",
      board_action_cue:
        variant === "repeat"
          ? "Noch kleiner: links minus drei und rechts auch minus drei."
          : "Darum ziehen wir auf beiden Seiten drei ab.",
      board_recovery_note:
        variant === "repeat" ? "Wir machen nur diesen einen Zug deutlicher." : "",
      board_structure: {
        primary_left: "x + 3",
        primary_right: "7",
        operation_left: "- 3",
        operation_right: "- 3",
        result_left: "",
        result_right: "",
        show_operation: true,
        show_result: false,
      },
      visual_hint:
        "Der wichtige Punkt ist nicht das Wegnehmen, sondern dass der Zug links und rechts derselbe bleibt.",
      action_labels: {
        repeat: "Diesen Zug noch kleiner sehen",
        example: "Zeig mir ein aehnliches Beispiel",
        advance: "Zeig das Ergebnis dieses Zugs",
      },
    };
  }

  if (stage === "result") {
    return {
      block_type: "worked_example",
      goal: "Wir sehen, was nach demselben Zug uebrig bleibt.",
      transition_message:
        "Jetzt sehen wir, was nach diesem einen Zug uebrig bleibt.",
      focus: ["result_from_same_structure"],
      support_moves: ["link_result_back_to_operation"],
      support_scaffolds: ["show_result_in_same_carrier"],
      focus_note: "Das Ergebnis soll aus demselben Schritt kommen, nicht wie ein Sprung wirken.",
      scaffold_note: "Wir halten Gleichung, Zug und Ergebnis im selben Traeger zusammen.",
      board_label:
        variant === "repeat" ? "Derselbe Weg noch kleiner" : "Ergebnis aus demselben Schritt",
      board_meaning:
        "Nach demselben Zug auf beiden Seiten bleibt links nur noch x und rechts vier.",
      board_action_cue:
        variant === "repeat"
          ? "Wir schauen denselben Weg noch einmal in klein an."
          : "So wird aus derselben Beziehung sichtbar: x ist gleich vier.",
      board_recovery_note:
        variant === "repeat" ? "Wir gehen nicht zurueck. Wir machen nur den Weg klarer." : "",
      board_structure: {
        primary_left: "x + 3",
        primary_right: "7",
        operation_left: "- 3",
        operation_right: "- 3",
        result_left: "x",
        result_right: "4",
        show_operation: true,
        show_result: true,
      },
      visual_hint:
        "Das Ergebnis soll hergeleitet wirken, nicht ploetzlich erscheinen.",
      action_labels: {
        repeat: "Zeig den Weg noch einmal",
        example: "Zeig mir ein aehnliches Beispiel",
        advance: "Dieselbe Idee an einem Beispiel sehen",
      },
    };
  }

  if (stage === "similar_example") {
    return {
      block_type: "worked_example",
      goal: "Wir sichern dieselbe Struktur jetzt an einem aehnlichen Beispiel.",
      transition_message:
        "Jetzt sehen wir dieselbe Regel mit anderen Zahlen.",
      focus: ["same_structure_other_numbers"],
      support_moves: ["make_transfer_visible"],
      support_scaffolds: ["near_example_only"],
      focus_note: "Die Zahlen wechseln, die Struktur bleibt dieselbe.",
      scaffold_note: "Das Beispiel soll den Transfer sichern, kein neues Thema oeffnen.",
      board_label: "Aehnliches Beispiel",
      board_meaning:
        "Hier sind die Zahlen anders. Der Gedanke bleibt derselbe.",
      board_action_cue:
        "Wir machen wieder denselben Zug auf beiden Seiten, nur jetzt mit minus zwei.",
      board_recovery_note: "",
      board_structure: {
        primary_left: "5 + 2",
        primary_right: "7",
        operation_left: "- 2",
        operation_right: "- 2",
        result_left: "5",
        result_right: "5",
        show_operation: true,
        show_result: true,
      },
      visual_hint:
        "Das Beispiel soll zeigen: gleiche Struktur, andere Zahlen.",
      action_labels: {
        repeat: "Dieses Beispiel noch einmal sehen",
        example: "Bleib bei diesem Beispiel",
        advance: "Beim Beispiel bleiben",
      },
    };
  }

  return {
    block_type: "concept_intro",
    goal: "Wir sehen lineare Gleichungen zuerst als Beziehung.",
    transition_message:
      "Wir schauen zuerst nur darauf, dass beide Seiten zusammengehoeren.",
    focus: ["relationship_before_symbol"],
    support_moves: ["reduce_pressure_before_symbolic_step"],
    support_scaffolds: ["visual_relationship_first"],
    focus_note: "Noch keine Regel. Noch keine Umformung. Erst die Beziehung.",
    scaffold_note: "Wir halten den Einstieg ruhig und fuehren noch keinen Rechenschritt ein.",
    board_label: "Beziehung zuerst",
    board_meaning:
      "Beide Seiten gehoeren zusammen, noch bevor wir sie als Gleichung schreiben.",
    board_action_cue:
      "Wenn diese Beziehung klar ist, koennen wir sie als x + 3 = 7 aufschreiben.",
    board_recovery_note: "",
    board_structure: {
      primary_left: "ein Teil + 3",
      primary_right: "7",
      operation_left: "",
      operation_right: "",
      result_left: "",
      result_right: "",
      show_operation: false,
      show_result: false,
    },
    visual_hint:
      "Noch kein Rechentrick. Erst sehen, dass beide Seiten zusammengehoeren.",
    action_labels: {
      repeat: "Diesen Blick noch einmal sehen",
      example: "Zeig die Gleichung dazu",
      advance: "Jetzt als Gleichung sehen",
    },
  };
}
