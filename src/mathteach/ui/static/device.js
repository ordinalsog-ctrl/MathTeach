const STORAGE_KEY = "mathteach-device-shell";

const defaultState = {
  profile: {
    learnerName: "",
    ageGroup: "teen",
    mathLevel: "middle_school",
    preferredPace: "gentle",
    wantsVisuals: true,
    wantsHistory: false,
    supports: [],
    objective: "Erklaere mir lineare Gleichungen ruhig und mit Beispiel.",
  },
  sessionId: null,
  lastPlan: null,
  lastUpdatedAt: null,
};

const state = loadState();

document.addEventListener("DOMContentLoaded", () => {
  bindActions();
  bindPreferenceChips();
  updateClock();
  window.setInterval(updateClock, 30_000);
  hydrateForm();
  renderStartScreen();

  if (state.lastPlan) {
    renderLearningScreen(state.lastPlan);
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
          renderLearningScreen(state.lastPlan);
          return;
        }
        if (state.profile.learnerName) {
          await requestPlan([]);
          return;
        }
        switchScreen("onboarding");
        return;
      }

      if (action === "onboarding") {
        switchScreen("onboarding");
        return;
      }

      if (action === "back-home") {
        switchScreen("start");
        return;
      }

      if (action === "reset-session") {
        state.sessionId = null;
        state.lastPlan = null;
        state.lastUpdatedAt = null;
        saveState();
        renderStartScreen();
        switchScreen("start");
        return;
      }

      if (action === "start-learning") {
        readFormIntoState();
        if (!state.profile.learnerName.trim()) {
          window.alert("Bitte gib zuerst einen Namen ein.");
          return;
        }
        if (!state.profile.objective.trim()) {
          window.alert("Bitte gib ein Thema oder Ziel ein.");
          return;
        }
        state.sessionId = state.sessionId || buildSessionId();
        saveState();
        await requestPlan([]);
        return;
      }

      if (action === "again") {
        await requestPlan([{ evidence: ["repeated_concept_error", "text_overload"] }]);
        return;
      }

      if (action === "example") {
        await requestPlan([{ evidence: ["repeated_concept_error", "no_progress_two_blocks"] }]);
        return;
      }

      if (action === "advance") {
        await requestPlan([{ evidence: ["visible_small_success", "transfer_success"] }]);
      }
    });
  });
}

function bindPreferenceChips() {
  document.querySelectorAll(".chip").forEach((chip) => {
    chip.addEventListener("click", () => {
      const pref = chip.dataset.pref;
      const value = chip.dataset.value;
      document
        .querySelectorAll(`.chip[data-pref="${pref}"]`)
        .forEach((item) => item.classList.remove("is-active"));
      chip.classList.add("is-active");

      if (pref === "visuals") {
        state.profile.wantsVisuals = value === "true";
      } else if (pref === "pace") {
        state.profile.preferredPace = value;
      }
      saveState();
    });
  });
}

function hydrateForm() {
  const nameInput = document.querySelector('input[name="learnerName"]');
  const levelSelect = document.querySelector('select[name="mathLevel"]');
  const objectiveInput = document.querySelector('input[name="objective"]');

  nameInput.value = state.profile.learnerName || "";
  levelSelect.value = state.profile.mathLevel || "middle_school";
  objectiveInput.value = state.profile.objective || defaultState.profile.objective;

  document
    .querySelectorAll('.chip[data-pref="visuals"]')
    .forEach((chip) => chip.classList.toggle("is-active", String(state.profile.wantsVisuals) === chip.dataset.value));

  document
    .querySelectorAll('.chip[data-pref="pace"]')
    .forEach((chip) => chip.classList.toggle("is-active", state.profile.preferredPace === chip.dataset.value));

  document.querySelectorAll('input[name="support"]').forEach((checkbox) => {
    checkbox.checked = state.profile.supports.includes(checkbox.value);
  });
}

function readFormIntoState() {
  state.profile.learnerName = document.querySelector('input[name="learnerName"]').value.trim();
  state.profile.mathLevel = document.querySelector('select[name="mathLevel"]').value;
  state.profile.objective = document.querySelector('input[name="objective"]').value.trim();
  state.profile.supports = Array.from(
    document.querySelectorAll('input[name="support"]:checked')
  ).map((input) => input.value);
  saveState();
}

async function requestPlan(runtimeObservations) {
  if (!state.profile.learnerName) {
    switchScreen("onboarding");
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
  setStatus("Ich bereite den naechsten Schritt fuer dich vor ...");

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
    renderLearningScreen(plan);
    switchScreen("learning");
  } catch (error) {
    setStatus("Der lokale Plan konnte gerade nicht geladen werden. Wir koennen es gleich noch einmal versuchen.");
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

function renderLearningScreen(plan) {
  const activeBlock = pickActiveBlock(plan);
  text("[data-role='lesson-goal']", activeBlock.goal || state.profile.objective);
  text("[data-role='lesson-mode']", friendlyMode(plan.lesson_mode));
  text("[data-role='lesson-block']", friendlyBlock(activeBlock.block_type));
  text("[data-role='visual-hint']", buildVisualHint(activeBlock));
  setStatus(
    activeBlock.transition_message ||
      "Du kannst dir denselben Gedanken noch einmal zeigen lassen oder ruhig zum naechsten Schritt gehen."
  );

  fillList("[data-role='focus-list']", activeBlock.focus, [
    "Wir halten nur den naechsten Gedanken auf dem Bildschirm.",
  ]);
  fillList("[data-role='support-moves']", activeBlock.support_moves, [
    "Ich halte die Erklaerung knapp und gut lesbar.",
  ]);
  fillList("[data-role='support-scaffolds']", activeBlock.support_scaffolds, [
    "Bei Bedarf gehe ich noch einen Schritt kleiner.",
  ]);
}

function pickActiveBlock(plan) {
  if (Array.isArray(plan.planned_blocks) && plan.planned_blocks.length > 0) {
    return plan.planned_blocks[0];
  }
  return {
    goal: state.profile.objective,
    focus: [],
    support_moves: [],
    support_scaffolds: [],
    block_type: null,
    transition_message: null,
  };
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
    support_line: "Du kannst mit einem kleinen Schritt wieder einsteigen.",
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
    support_line: "Wir koennen klein und ruhig anfangen.",
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
    support_line: "Wir nehmen nur den letzten stabilen Schritt.",
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
  const tertiaryAction = document.querySelector("[data-role='start-tertiary-action']");

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

  if (tertiaryAction) {
    tertiaryAction.hidden = true;
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

function setStatus(message) {
  text("[data-role='status-copy']", message);
}

function fillList(selector, items, fallback) {
  const node = document.querySelector(selector);
  node.innerHTML = "";
  const values = Array.isArray(items) && items.length > 0 ? items : fallback;
  values.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = prettify(item);
    node.appendChild(li);
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

function friendlyMode(mode) {
  if (!mode) {
    return "Ruhiger Start";
  }
  return prettify(mode);
}

function friendlyBlock(blockType) {
  if (!blockType) {
    return "Naechster Schritt";
  }
  return prettify(blockType);
}

function buildVisualHint(block) {
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
