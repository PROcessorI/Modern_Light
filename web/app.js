const ui = {
  statusBadge: document.getElementById("statusBadge"),
  modeBadge: document.getElementById("modeBadge"),
  themeToggleBtn: document.getElementById("themeToggleBtn"),

  portInput: document.getElementById("portInput"),
  baudInput: document.getElementById("baudInput"),

  connectBtn: document.getElementById("connectBtn"),
  disconnectBtn: document.getElementById("disconnectBtn"),
  refreshPortsBtn: document.getElementById("refreshPortsBtn"),
  saveConnBtn: document.getElementById("saveConnBtn"),

  comAddress: document.getElementById("comAddress"),
  comCode: document.getElementById("comCode"),
  sendComBtn: document.getElementById("sendComBtn"),

  readTimeBtn: document.getElementById("readTimeBtn"),
  localTimeBtn: document.getElementById("localTimeBtn"),
  writeTimeBtn: document.getElementById("writeTimeBtn"),
  timeValue: document.getElementById("timeValue"),
  dayValue: document.getElementById("dayValue"),
  dateValue: document.getElementById("dateValue"),

  readGeoBtn: document.getElementById("readGeoBtn"),
  writeGeoBtn: document.getElementById("writeGeoBtn"),
  latValue: document.getElementById("latValue"),
  lonValue: document.getElementById("lonValue"),
  zoneValue: document.getElementById("zoneValue"),

  brightAI: document.getElementById("brightAI"),
  brightAG: document.getElementById("brightAG"),
  brightLevel: document.getElementById("brightLevel"),
  brightLevelRange: document.getElementById("brightLevelRange"),
  brightLevelValue: document.getElementById("brightLevelValue"),
  brightScene: document.getElementById("brightScene"),
  brightSceneRange: document.getElementById("brightSceneRange"),
  brightSceneValue: document.getElementById("brightSceneValue"),
  brightCommand: document.getElementById("brightCommand"),
  brightCommandRange: document.getElementById("brightCommandRange"),
  brightCommandValue: document.getElementById("brightCommandValue"),
  sendBrightnessBtn: document.getElementById("sendBrightnessBtn"),
  brightModeButtons: Array.from(document.querySelectorAll("[data-bright-mode]")),
  brightModeLevelBox: document.getElementById("brightModeLevelBox"),
  brightModeSceneBox: document.getElementById("brightModeSceneBox"),
  brightModeCommandBox: document.getElementById("brightModeCommandBox"),
  brightLevelPresets: Array.from(document.querySelectorAll("[data-bright-level]")),
  brightScenePresets: Array.from(document.querySelectorAll("[data-bright-scene]")),

  fixtureAI: document.getElementById("fixtureAI"),
  fixtureAG: document.getElementById("fixtureAG"),
  specRed: document.getElementById("specRed"),
  specRedApplyBtn: document.getElementById("specRedApplyBtn"),
  specBlue: document.getElementById("specBlue"),
  specBlueApplyBtn: document.getElementById("specBlueApplyBtn"),
  specWhite: document.getElementById("specWhite"),
  specWhiteApplyBtn: document.getElementById("specWhiteApplyBtn"),
  specFarRed: document.getElementById("specFarRed"),
  specFarRedApplyBtn: document.getElementById("specFarRedApplyBtn"),
  sceneCurrentSimple: document.getElementById("sceneCurrentSimple"),
  sceneSaveSimple: document.getElementById("sceneSaveSimple"),
  scenePlaySimple: document.getElementById("scenePlaySimple"),
  applySpectrumBtn: document.getElementById("applySpectrumBtn"),
  saveScenarioBtn: document.getElementById("saveScenarioBtn"),
  playScenarioBtn: document.getElementById("playScenarioBtn"),
  stopScenarioRepeatBtn: document.getElementById("stopScenarioRepeatBtn"),
  scenarioRepeatEnabled: document.getElementById("scenarioRepeatEnabled"),
  scenarioRepeatHours: document.getElementById("scenarioRepeatHours"),
  scenarioRepeatMinutes: document.getElementById("scenarioRepeatMinutes"),
  scenarioRepeatSeconds: document.getElementById("scenarioRepeatSeconds"),
  scenarioRepeatStatus: document.getElementById("scenarioRepeatStatus"),

  aiProgramValue: document.getElementById("aiProgramValue"),
  adrPrgBtn: document.getElementById("adrPrgBtn"),
  setAiBtn: document.getElementById("setAiBtn"),

  grpAI: document.getElementById("grpAI"),
  grpAG: document.getElementById("grpAG"),
  grpSlot: document.getElementById("grpSlot"),
  grpNumber: document.getElementById("grpNumber"),
  grpClear: document.getElementById("grpClear"),
  grpApplyBtn: document.getElementById("grpApplyBtn"),

  astroYear: document.getElementById("astroYear"),
  astroMorningCorr: document.getElementById("astroMorningCorr"),
  astroEveningCorr: document.getElementById("astroEveningCorr"),
  generateAstronomyBtn: document.getElementById("generateAstronomyBtn"),
  astronomyResult: document.getElementById("astronomyResult"),

  keysA: document.getElementById("keysA"),
  keysB: document.getElementById("keysB"),
  keysC: document.getElementById("keysC"),
  readKeysBtn: document.getElementById("readKeysBtn"),
  writeKeysBtn: document.getElementById("writeKeysBtn"),

  maskA: document.getElementById("maskA"),
  maskB: document.getElementById("maskB"),
  maskC: document.getElementById("maskC"),
  readMaskBtn: document.getElementById("readMaskBtn"),
  writeMaskBtn: document.getElementById("writeMaskBtn"),

  sceneAI: document.getElementById("sceneAI"),
  sceneAG: document.getElementById("sceneAG"),
  sceneReadNo: document.getElementById("sceneReadNo"),
  sceneWriteNo: document.getElementById("sceneWriteNo"),
  sceneActivateBtn: document.getElementById("sceneActivateBtn"),
  sceneSaveBtn: document.getElementById("sceneSaveBtn"),
  sceneStartBtn: document.getElementById("sceneStartBtn"),
  sceneChannel: document.getElementById("sceneChannel"),
  scenePercent: document.getElementById("scenePercent"),
  scenePercentRange: document.getElementById("scenePercentRange"),
  scenePercentValue: document.getElementById("scenePercentValue"),
  sceneChannelBtn: document.getElementById("sceneChannelBtn"),
  scenePercentPresets: Array.from(document.querySelectorAll("[data-scene-percent]")),
  sceneGroupSlot: document.getElementById("sceneGroupSlot"),
  sceneGroupNumber: document.getElementById("sceneGroupNumber"),
  sceneGroupBtn: document.getElementById("sceneGroupBtn"),

  scheduleWriteBtn: document.getElementById("scheduleWriteBtn"),
  schedClockInput: document.getElementById("schedClockInput"),
  schedOffsetInput: document.getElementById("schedOffsetInput"),
  schedOffsetRange: document.getElementById("schedOffsetRange"),
  schedOffsetValue: document.getElementById("schedOffsetValue"),
  schedTimeFixedWrap: document.getElementById("schedTimeFixedWrap"),
  schedTimeOffsetWrap: document.getElementById("schedTimeOffsetWrap"),
  schedIndex: document.getElementById("schedIndex"),
  schedTimeType: document.getElementById("schedTimeType"),
  schedSign: document.getElementById("schedSign"),
  schedActive: document.getElementById("schedActive"),
  schedHour: document.getElementById("schedHour"),
  schedMin: document.getElementById("schedMin"),
  schedTargetMode: document.getElementById("schedTargetMode"),
  schedAiActionSection: document.getElementById("schedAiActionSection"),
  schedKeysSection: document.getElementById("schedKeysSection"),
  schedActionButtons: Array.from(document.querySelectorAll("[data-sched-action]")),
  schedActionBrightnessBox: document.getElementById("schedActionBrightnessBox"),
  schedActionSceneBox: document.getElementById("schedActionSceneBox"),
  schedActionCommandBox: document.getElementById("schedActionCommandBox"),
  schedLevel: document.getElementById("schedLevel"),
  schedAI: document.getElementById("schedAI"),
  schedAG: document.getElementById("schedAG"),
  schedBrightness: document.getElementById("schedBrightness"),
  schedBrightnessRange: document.getElementById("schedBrightnessRange"),
  schedBrightnessValue: document.getElementById("schedBrightnessValue"),
  schedScene: document.getElementById("schedScene"),
  schedSceneRange: document.getElementById("schedSceneRange"),
  schedSceneValue: document.getElementById("schedSceneValue"),
  schedCommandCode: document.getElementById("schedCommandCode"),
  schedCommandPresets: Array.from(document.querySelectorAll("[data-sched-command]")),
  schedD1: document.getElementById("schedD1"),
  schedD2: document.getElementById("schedD2"),
  schedD3: document.getElementById("schedD3"),
  schedD4: document.getElementById("schedD4"),
  schedD5: document.getElementById("schedD5"),
  schedD6: document.getElementById("schedD6"),
  schedD7: document.getElementById("schedD7"),
  schedDaysWork: document.getElementById("schedDaysWork"),
  schedDaysWeekend: document.getElementById("schedDaysWeekend"),
  schedDaysAll: document.getElementById("schedDaysAll"),
  schedKeyA: document.getElementById("schedKeyA"),
  schedKeyB: document.getElementById("schedKeyB"),
  schedKeyC: document.getElementById("schedKeyC"),

  rawCommand: document.getElementById("rawCommand"),
  rawResponse: document.getElementById("rawResponse"),
  sendRawBtn: document.getElementById("sendRawBtn"),
  readScheduleBtn: document.getElementById("readScheduleBtn"),
  commandHints: document.getElementById("commandHints"),

  scheduleBody: document.getElementById("scheduleBody"),
  scheduleCount: document.getElementById("scheduleCount"),
  scheduleFilter: document.getElementById("scheduleFilter"),

  logView: document.getElementById("logView"),
  logMeta: document.getElementById("logMeta"),
  refreshLogsBtn: document.getElementById("refreshLogsBtn"),
  portHints: document.getElementById("portHints"),
  portQuickList: document.getElementById("portQuickList"),

  toastStack: document.getElementById("toastStack"),

  pageTabs: Array.from(document.querySelectorAll(".page-tab")),
  pages: Array.from(document.querySelectorAll(".page")),
};

const TIME_TYPE_MAP = {
  0: "Фикс.",
  1: "Рассвет",
  2: "Закат",
};

const THEME_STORAGE_KEY = "plc-them";
const LEGACY_THEME_STORAGE_KEY = "plc-theme";
const scheduleState = {
  entries: [],
};

const portState = {
  items: [],
};

const brightState = {
  mode: "level",
};

const scheduleUiState = {
  actionMode: "brightness",
};

// === Состояние повтора сценариев ===
// Центральное состояние для функции повтора сценариев. Содержит идентификаторы таймеров,
// временную метку следующего запуска и токен-защиту от гонок при перезапуске повтора.
const scenarioRepeatState = {
  timerId: null,
  countdownId: null,
  intervalMs: 0,
  nextRunAt: 0,
  scene: null,
  ai: null,
  ag: null,
  token: 0,
  busy: false,
};

// === Тайминги команд / сериализация ===
// Таймауты в мс для стабилизации контроллера между последовательными командами.
// Для команд спектра в режиме записи сцены паузы минимальны (как в PLT_1 Unit7).
const COMMAND_PACING_MS = {
  generic: 420,
  spectrum: 200,
  spectrumAdjust: 2500,
  spectrumBatch: 200,
  spectrumSaveChannelSettle: 900,
  spectrumSaveBeforeCommit: 1500,
  sceneActivate: 820,
  sceneSave: 980,
  repeatOffToPlay: 850,
};

// === Очередь команд светильника ===
// Сериализованная цепочка для предотвращения перекрытия API-вызовов управления светильниками.
const luminaireCommandState = {
  chain: Promise.resolve(),
};

// === Метки каналов спектра ===
// Человекочитаемые метки для полей спектра.
const SPECTRUM_CHANNEL_LABELS = {
  red: "Красный",
  blue: "Синий",
  farred: "Дальний красный",
  white: "Белый",
};

const SPECTRUM_INPUT_NODES = {
  red: () => ui.specRed,
  blue: () => ui.specBlue,
  farred: () => ui.specFarRed,
  white: () => ui.specWhite,
};

// === Состояние спектра ===
// Отслеживает, какие каналы спектра были изменены и требуют отправки на устройство.
const spectrumState = {
  dirty: {
    red: false,
    blue: false,
    farred: false,
    white: false,
  },
  lastEdited: null,
};

// Требует явной фиксации спектра (ОК) перед записью сцены.
const spectrumCommitState = {
  okReady: false,
};

// === Отладочный след фронтенда ===
// Хранит последнюю команду, запланированную UI, чтобы консоль показывала и текущую,
// и предыдущую команду перед отправкой в backend.
const debugCommandState = {
  lastPlanned: "",
  lastPlannedAt: 0,
};

function setCurrentScenarioValue(value) {
  // Обновляет поле текущего сценария с нормализацией диапазона 1..20.
  if (!ui.sceneCurrentSimple) {
    return 1;
  }

  const normalized = clampNumber(value, 1, 20, 1);
  ui.sceneCurrentSimple.value = String(normalized);
  return normalized;
}

function normalizeThemValue(value) {
  // Приводит вход к формату Theme: 1 (светлая) или 0 (темная).
  return Number(value) === 0 ? 0 : 1;
}

function pad2(value) {
  // Дополняет число ведущим нулем до двух символов.
  return String(value).padStart(2, "0");
}

function formatClockStamp(date = new Date()) {
  // Форматирует время в виде ЧЧ:ММ:СС.мс для дебага.
  return `${pad2(date.getHours())}:${pad2(date.getMinutes())}:${pad2(date.getSeconds())}.${String(
    date.getMilliseconds()
  ).padStart(3, "0")}`;
}

function formatDurationMs(valueMs) {
  // Форматирует длительность в виде ЧЧ:ММ:СС.
  const totalSeconds = Math.max(0, Math.floor((Number(valueMs) || 0) / 1000));
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;
  return `${pad2(hours)}:${pad2(minutes)}:${pad2(seconds)}`;
}

function sendDebugTraceLog(message) {
  // Отправляет debug-строку в backend-лог без блокировки UI.
  if (!eel || !eel.api_trace_log) {
    return;
  }

  eel.api_trace_log(message)().catch(() => undefined);
}

function waitMs(delayMs) {
  // Асинхронная пауза для последовательных команд к контроллеру.
  return new Promise((resolve) => {
    window.setTimeout(resolve, Math.max(0, Number(delayMs) || 0));
  });
}

function runLuminaireCommand(task, settleMs = COMMAND_PACING_MS.generic) {
  // Сериализует команды управления светильниками и добавляет паузу стабилизации.
  const scheduled = luminaireCommandState.chain
    .catch(() => undefined)
    .then(async () => {
      const result = await task();
      if (settleMs > 0) {
        await waitMs(settleMs);
      }
      return result;
    });

  luminaireCommandState.chain = scheduled.then(
    () => undefined,
    () => undefined
  );

  return scheduled;
}

function optionalFieldValue(node) {
  // Возвращает значение поля или null, если поле пустое.
  const value = String(node?.value ?? "").trim();
  return value === "" ? null : value;
}

function resolveAddressPreference(aiValue, agValue) {
  // При заполненном AG приоритет всегда у группового адреса.
  const ai = String(aiValue ?? "").trim();
  const ag = String(agValue ?? "").trim();

  if (ag !== "") {
    return { ai: null, ag };
  }
  if (ai !== "") {
    return { ai, ag: null };
  }
  return { ai: null, ag: null };
}

function resolveAddressFields(aiNode, agNode) {
  // Собирает адресные поля AI/AG в единый объект для API.
  return resolveAddressPreference(aiNode?.value, agNode?.value);
}

function clearScheduleActionFields() {
  // Очищает взаимно исключающие поля действия в редакторе расписания.
  ui.schedBrightness.value = "";
  ui.schedScene.value = "";
  ui.schedCommandCode.value = "";
}

function clampNumber(value, min, max, fallback) {
  // Нормализует значение в целое число внутри диапазона.
  const parsed = Number.parseInt(String(value ?? ""), 10);
  if (!Number.isFinite(parsed)) {
    return fallback;
  }
  return Math.min(max, Math.max(min, parsed));
}

function setPairValue(numberNode, rangeNode, valueNode, rawValue, suffix = "") {
  // Синхронизирует number+range и подпись текущего значения.
  if (!numberNode || !rangeNode || !valueNode) {
    return;
  }

  const min = Number(rangeNode.min || numberNode.min || 0);
  const max = Number(rangeNode.max || numberNode.max || 100);
  const fallback = clampNumber(numberNode.value || rangeNode.value || rawValue, min, max, min);
  const normalized = clampNumber(rawValue, min, max, fallback);

  numberNode.value = String(normalized);
  rangeNode.value = String(normalized);
  valueNode.textContent = `${normalized}${suffix}`;
}

function bindNumberRange(numberNode, rangeNode, valueNode, suffix = "") {
  // Подключает двустороннюю синхронизацию между полем и слайдером.
  if (!numberNode || !rangeNode || !valueNode) {
    return;
  }

  numberNode.addEventListener("input", () => {
    setPairValue(numberNode, rangeNode, valueNode, numberNode.value, suffix);
  });
  rangeNode.addEventListener("input", () => {
    setPairValue(numberNode, rangeNode, valueNode, rangeNode.value, suffix);
  });

  setPairValue(numberNode, rangeNode, valueNode, numberNode.value || rangeNode.value, suffix);
}

function getPairNumberValue(numberNode, rangeNode, min, max, fallback) {
  // Надежно читает число из пары number/range и возвращает значение в диапазоне.
  const fromRange = Number.parseInt(String(rangeNode?.value ?? ""), 10);
  const fromNumber = Number.parseInt(String(numberNode?.value ?? ""), 10);

  if (Number.isFinite(fromNumber)) {
    return clampNumber(fromNumber, min, max, fallback);
  }
  if (Number.isFinite(fromRange)) {
    return clampNumber(fromRange, min, max, fallback);
  }
  return clampNumber(fallback, min, max, fallback);
}

function getSpectrumInputValue(node, fallback = 0) {
  // Читает значение спектра из поля ввода в диапазоне 0..100.
  return clampNumber(node?.value, 0, 100, fallback);
}

function setSpectrumInputValue(node, value) {
  // Нормализует и записывает значение спектра обратно в поле ввода.
  if (!node) {
    return 0;
  }
  const normalized = clampNumber(value, 0, 100, 0);
  node.value = String(normalized);
  return normalized;
}

function setBrightnessMode(mode) {
  // Переключает активный режим команды яркости: уровень, сценарий или сервис.
  const allowed = new Set(["level", "scene", "command"]);
  const nextMode = allowed.has(mode) ? mode : "level";
  brightState.mode = nextMode;

  ui.brightModeButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.brightMode === nextMode);
  });

  ui.brightModeLevelBox?.classList.toggle("active", nextMode === "level");
  ui.brightModeSceneBox?.classList.toggle("active", nextMode === "scene");
  ui.brightModeCommandBox?.classList.toggle("active", nextMode === "command");
}

function collectBrightnessAction() {
  // Формирует payload для команды яркости в соответствии с выбранным режимом.
  const adr = resolveAddressPreference(ui.brightAI?.value, ui.brightAG?.value);
  const result = {
    ai: adr.ai,
    ag: adr.ag,
    brightness: null,
    scene: null,
    command_code: null,
  };

  if (brightState.mode === "level") {
    result.brightness = String(clampNumber(ui.brightLevel.value, 0, 10, 5));
  } else if (brightState.mode === "scene") {
    result.scene = String(clampNumber(ui.brightScene.value, 1, 20, 1));
  } else {
    result.command_code = String(clampNumber(ui.brightCommand.value, 230, 250, 230));
  }

  return result;
}

function initComfortControls() {
  // Инициализирует расширенные элементы управления: слайдеры и пресеты.
  bindNumberRange(ui.brightLevel, ui.brightLevelRange, ui.brightLevelValue);
  bindNumberRange(ui.brightScene, ui.brightSceneRange, ui.brightSceneValue);
  bindNumberRange(ui.brightCommand, ui.brightCommandRange, ui.brightCommandValue);
  bindNumberRange(ui.scenePercent, ui.scenePercentRange, ui.scenePercentValue, "%");

  setBrightnessMode("level");

  ui.brightModeButtons.forEach((button) => {
    button.addEventListener("click", () => {
      setBrightnessMode(button.dataset.brightMode || "level");
    });
  });

  ui.brightLevel.addEventListener("input", () => setBrightnessMode("level"));
  ui.brightLevelRange.addEventListener("input", () => setBrightnessMode("level"));
  ui.brightScene.addEventListener("input", () => setBrightnessMode("scene"));
  ui.brightSceneRange.addEventListener("input", () => setBrightnessMode("scene"));
  ui.brightCommand.addEventListener("input", () => setBrightnessMode("command"));
  ui.brightCommandRange.addEventListener("input", () => setBrightnessMode("command"));

  ui.brightLevelPresets.forEach((button) => {
    button.addEventListener("click", () => {
      setBrightnessMode("level");
      setPairValue(
        ui.brightLevel,
        ui.brightLevelRange,
        ui.brightLevelValue,
        button.dataset.brightLevel || "5"
      );
    });
  });

  ui.brightScenePresets.forEach((button) => {
    button.addEventListener("click", () => {
      setBrightnessMode("scene");
      setPairValue(
        ui.brightScene,
        ui.brightSceneRange,
        ui.brightSceneValue,
        button.dataset.brightScene || "1"
      );
    });
  });

  ui.scenePercentPresets.forEach((button) => {
    button.addEventListener("click", () => {
      setPairValue(
        ui.scenePercent,
        ui.scenePercentRange,
        ui.scenePercentValue,
        button.dataset.scenePercent || "50",
        "%"
      );
    });
  });
}

function syncSimpleAddressToLegacy() {
  // Синхронизирует новый адресный блок с legacy-полями API.
  const preferred = resolveAddressPreference(ui.fixtureAI?.value, ui.fixtureAG?.value);
  const ai = preferred.ai || "";
  const ag = preferred.ag || "";

  if (ui.fixtureAI) {
    ui.fixtureAI.value = ai;
  }
  if (ui.fixtureAG) {
    ui.fixtureAG.value = ag;
  }

  if (ui.sceneAI) {
    ui.sceneAI.value = ai;
  }
  if (ui.sceneAG) {
    ui.sceneAG.value = ag;
  }
  if (ui.brightAI) {
    ui.brightAI.value = ai;
  }
  if (ui.brightAG) {
    ui.brightAG.value = ag;
  }
}

function initLuminairePanel() {
  // Инициализирует упрощенную панель управления светильниками.
  // Гарантирует нулевые значения спектров при инициализации панели.
  setSpectrumInputValue(ui.specRed, 0);
  setSpectrumInputValue(ui.specBlue, 0);
  setSpectrumInputValue(ui.specFarRed, 0);
  setSpectrumInputValue(ui.specWhite, 0);

  if (!optionalFieldValue(ui.fixtureAI) && !optionalFieldValue(ui.fixtureAG)) {
    // По умолчанию работаем от AG=0, а AI оставляем пустым.
    ui.fixtureAI.value = "";
    if (ui.fixtureAG) {
      ui.fixtureAG.value = "0";
    }
  }

  if (optionalFieldValue(ui.fixtureAG) !== null && ui.fixtureAI) {
    ui.fixtureAI.value = "";
  }

  const markSpectrumDirty = (channel) => {
    spectrumState.dirty[channel] = true;
    spectrumState.lastEdited = channel;
    spectrumCommitState.okReady = false;
  };

  ui.specRed?.addEventListener("input", () => markSpectrumDirty("red"));
  ui.specBlue?.addEventListener("input", () => markSpectrumDirty("blue"));
  ui.specFarRed?.addEventListener("input", () => markSpectrumDirty("farred"));
  ui.specWhite?.addEventListener("input", () => markSpectrumDirty("white"));

  ui.fixtureAI?.addEventListener("input", () => {
    if (optionalFieldValue(ui.fixtureAI) !== null && ui.fixtureAG) {
      ui.fixtureAG.value = "";
    }
    spectrumCommitState.okReady = false;
    syncSimpleAddressToLegacy();
  });

  ui.fixtureAG?.addEventListener("input", () => {
    const agValue = optionalFieldValue(ui.fixtureAG);
    if (agValue !== null && ui.fixtureAI) {
      ui.fixtureAI.value = "";
    }
    spectrumCommitState.okReady = false;
    syncSimpleAddressToLegacy();
  });

  ui.sceneCurrentSimple?.addEventListener("change", () => {
    setCurrentScenarioValue(ui.sceneCurrentSimple.value);
  });

  ui.sceneSaveSimple?.addEventListener("change", () => {
    const saveRaw = optionalFieldValue(ui.sceneSaveSimple);
    if (saveRaw === null) {
      return;
    }

    const currentScene = setCurrentScenarioValue(ui.sceneCurrentSimple?.value);
    const saveScene = clampNumber(saveRaw, 1, 20, currentScene);
    ui.sceneSaveSimple.value = String(saveScene);
    setCurrentScenarioValue(saveScene);
  });

  ui.scenePlaySimple?.addEventListener("change", () => {
    const playRaw = optionalFieldValue(ui.scenePlaySimple);
    if (playRaw === null) {
      return;
    }

    const currentScene = setCurrentScenarioValue(ui.sceneCurrentSimple?.value);
    const playScene = clampNumber(playRaw, 1, 20, currentScene);
    ui.scenePlaySimple.value = String(playScene);
    setCurrentScenarioValue(playScene);
  });

  [ui.scenarioRepeatHours, ui.scenarioRepeatMinutes, ui.scenarioRepeatSeconds].forEach((node) => {
    node?.addEventListener("input", () => {
      normalizeScenarioRepeatFields();
      if (ui.scenarioRepeatEnabled?.checked && scenarioRepeatState.timerId === null) {
        const { hours, minutes, seconds } = normalizeScenarioRepeatFields();
        setScenarioRepeatStatus(
          `Повтор будет запущен каждые ${formatRepeatInterval(hours, minutes, seconds)} после применения`
        );
      }
    });
  });

  ui.scenarioRepeatEnabled?.addEventListener("change", () => {
    if (!ui.scenarioRepeatEnabled.checked) {
      stopScenarioRepeat("Повтор выключен");
      return;
    }

    const { hours, minutes, seconds } = normalizeScenarioRepeatFields();
    setScenarioRepeatStatus(
      `Повтор будет запущен каждые ${formatRepeatInterval(hours, minutes, seconds)} после применения`
    );
  });

  normalizeScenarioRepeatFields();
  setCurrentScenarioValue(ui.sceneCurrentSimple?.value);
  setScenarioRepeatStatus("Повтор выключен");
  syncSimpleAddressToLegacy();
}

function setScheduleActionMode(mode) {
  // Переключает действие для режима AI: яркость, сценарий или код команды.
  const allowed = new Set(["brightness", "scene", "command"]);
  const nextMode = allowed.has(mode) ? mode : "brightness";
  scheduleUiState.actionMode = nextMode;

  ui.schedActionButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.schedAction === nextMode);
  });

  ui.schedActionBrightnessBox?.classList.toggle("active", nextMode === "brightness");
  ui.schedActionSceneBox?.classList.toggle("active", nextMode === "scene");
  ui.schedActionCommandBox?.classList.toggle("active", nextMode === "command");
}

function updateScheduleTargetModeUI() {
  // Переключает видимость секций AI и KEYS/DIAG по выбранному режиму цели.
  const isAiMode = ui.schedTargetMode.value === "ai";
  ui.schedAiActionSection?.classList.toggle("hidden-control", !isAiMode);
  ui.schedKeysSection?.classList.toggle("hidden-control", isAiMode);
  ui.schedAI.disabled = !isAiMode;
  ui.schedAG.disabled = !isAiMode;
}

function updateScheduleTimeModeUI() {
  // Показывает нужный блок времени: фиксированное или смещение.
  const isFixed = ui.schedTimeType.value === "0";
  ui.schedTimeFixedWrap?.classList.toggle("hidden-control", !isFixed);
  ui.schedTimeOffsetWrap?.classList.toggle("hidden-control", isFixed);

  if (isFixed) {
    ui.schedSign.value = "+";
  }
}

function syncScheduleLegacyTimeFieldsFromUI() {
  // Переносит удобные поля времени в legacy-поля, которые ожидает backend.
  if (ui.schedTimeType.value === "0") {
    const [hoursRaw, minutesRaw] = String(ui.schedClockInput.value || "00:00").split(":");
    ui.schedSign.value = "+";
    ui.schedHour.value = String(clampNumber(hoursRaw, 0, 23, 0));
    ui.schedMin.value = String(clampNumber(minutesRaw, 0, 59, 0));
    return;
  }

  const offset = clampNumber(ui.schedOffsetInput.value, -180, 180, 0);
  const absolute = Math.abs(offset);
  ui.schedSign.value = offset < 0 ? "-" : "+";
  ui.schedHour.value = String(Math.floor(absolute / 60));
  ui.schedMin.value = String(absolute % 60);
}

function syncScheduleTimeUIFromLegacyFields() {
  // Заполняет удобные контролы времени значениями из legacy-полей.
  const hours = clampNumber(ui.schedHour.value, 0, 23, 0);
  const minutes = clampNumber(ui.schedMin.value, 0, 59, 0);

  if (ui.schedTimeType.value === "0") {
    ui.schedClockInput.value = `${pad2(hours)}:${pad2(minutes)}`;
  } else {
    const sign = ui.schedSign.value === "-" ? -1 : 1;
    const offset = sign * (hours * 60 + minutes);
    setPairValue(ui.schedOffsetInput, ui.schedOffsetRange, ui.schedOffsetValue, offset, " мин");
  }

  updateScheduleTimeModeUI();
}

function syncScheduleActionFieldsFromUI() {
  // Гарантирует корректный выбор только одного действия для режима AI.
  if (ui.schedTargetMode.value !== "ai") {
    clearScheduleActionFields();
    return;
  }

  if (scheduleUiState.actionMode === "brightness") {
    ui.schedBrightness.value = String(clampNumber(ui.schedBrightness.value, 0, 10, 5));
    ui.schedScene.value = "";
    ui.schedCommandCode.value = "";
    return;
  }

  if (scheduleUiState.actionMode === "scene") {
    ui.schedScene.value = String(clampNumber(ui.schedScene.value, 1, 20, 1));
    ui.schedBrightness.value = "";
    ui.schedCommandCode.value = "";
    return;
  }

  ui.schedCommandCode.value = String(clampNumber(ui.schedCommandCode.value, 0, 255, 230));
  ui.schedBrightness.value = "";
  ui.schedScene.value = "";
}

function syncScheduleActionModeFromLegacyFields() {
  // Подбирает активный режим действия по уже заполненным legacy-полям.
  if (ui.schedTargetMode.value !== "ai") {
    return;
  }

  if (optionalFieldValue(ui.schedBrightness) !== null) {
    setScheduleActionMode("brightness");
    setPairValue(
      ui.schedBrightness,
      ui.schedBrightnessRange,
      ui.schedBrightnessValue,
      ui.schedBrightness.value
    );
    return;
  }

  if (optionalFieldValue(ui.schedScene) !== null) {
    setScheduleActionMode("scene");
    setPairValue(ui.schedScene, ui.schedSceneRange, ui.schedSceneValue, ui.schedScene.value);
    return;
  }

  if (optionalFieldValue(ui.schedCommandCode) !== null) {
    setScheduleActionMode("command");
    return;
  }

  setScheduleActionMode("brightness");
}

function applyScheduleDaysPreset(mode) {
  // Быстрые пресеты выбора дней: будни, выходные, все.
  const dayNodes = [ui.schedD1, ui.schedD2, ui.schedD3, ui.schedD4, ui.schedD5, ui.schedD6, ui.schedD7];

  if (mode === "work") {
    dayNodes.forEach((node, index) => {
      node.checked = index < 5;
    });
    return;
  }

  if (mode === "weekend") {
    dayNodes.forEach((node, index) => {
      node.checked = index >= 5;
    });
    return;
  }

  dayNodes.forEach((node) => {
    node.checked = true;
  });
}

function initScheduleComfortControls() {
  // Инициализирует удобные контролы расписания: время, дни и тип действия.
  bindNumberRange(ui.schedOffsetInput, ui.schedOffsetRange, ui.schedOffsetValue, " мин");
  bindNumberRange(ui.schedBrightness, ui.schedBrightnessRange, ui.schedBrightnessValue);
  bindNumberRange(ui.schedScene, ui.schedSceneRange, ui.schedSceneValue);

  ui.schedClockInput?.addEventListener("input", syncScheduleLegacyTimeFieldsFromUI);
  ui.schedOffsetInput?.addEventListener("input", syncScheduleLegacyTimeFieldsFromUI);
  ui.schedOffsetRange?.addEventListener("input", syncScheduleLegacyTimeFieldsFromUI);

  ui.schedActionButtons.forEach((button) => {
    button.addEventListener("click", () => {
      setScheduleActionMode(button.dataset.schedAction || "brightness");
      syncScheduleActionFieldsFromUI();
    });
  });

  ui.schedBrightness?.addEventListener("input", () => setScheduleActionMode("brightness"));
  ui.schedBrightnessRange?.addEventListener("input", () => setScheduleActionMode("brightness"));
  ui.schedScene?.addEventListener("input", () => setScheduleActionMode("scene"));
  ui.schedSceneRange?.addEventListener("input", () => setScheduleActionMode("scene"));
  ui.schedCommandCode?.addEventListener("input", () => setScheduleActionMode("command"));

  ui.schedCommandPresets.forEach((button) => {
    button.addEventListener("click", () => {
      setScheduleActionMode("command");
      ui.schedCommandCode.value = String(clampNumber(button.dataset.schedCommand, 0, 255, 230));
    });
  });

  ui.schedDaysWork?.addEventListener("click", () => applyScheduleDaysPreset("work"));
  ui.schedDaysWeekend?.addEventListener("click", () => applyScheduleDaysPreset("weekend"));
  ui.schedDaysAll?.addEventListener("click", () => applyScheduleDaysPreset("all"));

  setScheduleActionMode("brightness");
  updateScheduleTargetModeUI();
  syncScheduleTimeUIFromLegacyFields();
}

function normalizeScenarioRepeatFields() {
  // Нормализует поля интервала повторения сценария (часы/минуты/секунды).
  const hours = clampNumber(ui.scenarioRepeatHours?.value, 0, 23, 0);
  const minutes = clampNumber(ui.scenarioRepeatMinutes?.value, 0, 59, 5);
  const seconds = clampNumber(ui.scenarioRepeatSeconds?.value, 0, 59, 0);

  if (ui.scenarioRepeatHours) {
    ui.scenarioRepeatHours.value = String(hours);
  }
  if (ui.scenarioRepeatMinutes) {
    ui.scenarioRepeatMinutes.value = String(minutes);
  }
  if (ui.scenarioRepeatSeconds) {
    ui.scenarioRepeatSeconds.value = String(seconds);
  }

  return { hours, minutes, seconds };
}

function formatRepeatInterval(hours, minutes, seconds) {
  // Форматирует интервал повторения в строку HH:MM:SS.
  return `${pad2(hours)}:${pad2(minutes)}:${pad2(seconds)}`;
}

function setScenarioRepeatStatus(message) {
  // Обновляет строку статуса повторяющихся сценариев.
  if (ui.scenarioRepeatStatus) {
    ui.scenarioRepeatStatus.textContent = message;
  }
}

function formatCountdownFromMs(valueMs) {
  // Переводит миллисекунды в формат обратного отсчета HH:MM:SS.
  const totalSeconds = Math.max(0, Math.ceil((Number(valueMs) || 0) / 1000));
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;
  return formatRepeatInterval(hours, minutes, seconds);
}

function updateScenarioRepeatCountdown() {
  // Обновляет статус повтора с обратным отсчетом до следующего цикла.
  if (scenarioRepeatState.intervalMs <= 0 || scenarioRepeatState.scene === null) {
    return;
  }

  const remaining = scenarioRepeatState.nextRunAt > 0
    ? Math.max(0, scenarioRepeatState.nextRunAt - Date.now())
    : scenarioRepeatState.intervalMs;

  const intervalLabel = formatCountdownFromMs(scenarioRepeatState.intervalMs);
  const remainingLabel = formatCountdownFromMs(remaining);
  const sceneLabel = scenarioRepeatState.scene ?? "-";
  const busySuffix = scenarioRepeatState.busy ? " Выполнение цикла..." : "";

  setScenarioRepeatStatus(
    `Повтор активен: каждые ${intervalLabel}. До следующего запуска ${remainingLabel} (сцена ${sceneLabel}).${busySuffix}`
  );
}

function stopScenarioRepeat(statusMessage = "Повтор выключен") {
  // Останавливает активный повтор сценария, если он запущен.
  scenarioRepeatState.token += 1;

  if (scenarioRepeatState.timerId !== null) {
    window.clearTimeout(scenarioRepeatState.timerId);
    scenarioRepeatState.timerId = null;
  }
  if (scenarioRepeatState.countdownId !== null) {
    window.clearInterval(scenarioRepeatState.countdownId);
    scenarioRepeatState.countdownId = null;
  }
  scenarioRepeatState.intervalMs = 0;
  scenarioRepeatState.nextRunAt = 0;
  scenarioRepeatState.scene = null;
  scenarioRepeatState.ai = null;
  scenarioRepeatState.ag = null;
  scenarioRepeatState.busy = false;
  setScenarioRepeatStatus(statusMessage);
}

function getLuminaireAddress() {
  // Возвращает адрес AI/AG для действий управления светильниками.
  const { ai, ag } = resolveAddressPreference(ui.fixtureAI?.value, ui.fixtureAG?.value);
  if (!ai && !ag) {
    throw new Error("Укажите номер светильника AI или номер группы AG");
  }

  syncSimpleAddressToLegacy();
  return { ai, ag };
}

function getLuminaireProgrammingAddress() {
  // Для программирования сцен используем тот же приоритет AG>AI.
  const { ai, ag } = resolveAddressPreference(ui.fixtureAI?.value, ui.fixtureAG?.value);

  if (!ai && !ag) {
    throw new Error("Укажите AI (1..220) или AG (0..29) для программирования сцены");
  }

  syncSimpleAddressToLegacy();
  return { ai, ag };
}

function resolveProtocolAddressForTrace(ai, ag) {
  // Повторяет legacy-логику адресации: AI=1..220, AG=0..29 -> 000/221..249.
  const aiText = String(ai ?? "").trim();
  const agText = String(ag ?? "").trim();

  if (aiText !== "") {
    const aiValue = Number.parseInt(aiText, 10);
    if (Number.isFinite(aiValue) && aiValue >= 1 && aiValue <= 220) {
      return aiValue;
    }
  }

  const agValue = Number.parseInt(agText || "0", 10);
  if (!Number.isFinite(agValue) || agValue < 0 || agValue > 29) {
    return 0;
  }
  return agValue === 0 ? 0 : 220 + agValue;
}

function buildLegacySpectrumComaCommand(address, channel, percent) {
  // Воспроизводит логику маппинга каналов legacy Unit7 с транспортом COMA.
  // Базовые коды каналов: Красный=140, Синий=160, Дальний красный=180, Белый=200.
  // Масштабирование: 0%=0, 1-10%=1, 11-100%=(percent//5)-1.
  const normalizedChannel = String(channel).trim().toLowerCase();
  const baseCodes = {
    red: 140,
    blue: 160,
    farred: 180,
    white: 200,
  };
  const scaled = percent === 0 ? 0 : percent <= 10 ? 1 : Math.floor(percent / 5) - 1;
  const code = baseCodes[normalizedChannel];
  if (typeof code !== "number") {
    throw new Error(`Неизвестный канал спектра: ${channel}`);
  }
  const adr = String(Number.parseInt(String(address || "0"), 10) || 0).padStart(3, "0");
  return `COMA${adr},${String(code + scaled).padStart(3, "0")}`;
}

function buildPlannedComaCommand(address, code) {
  // Формирует человекочитаемую строку COMA без отправки на устройство.
  const adr = String(Number.parseInt(String(address || "0"), 10) || 0).padStart(3, "0");
  return `COMA${adr},${String(Number(code) || 0).padStart(3, "0")}`;
}

function tracePlannedCommand(source, command, details = "") {
  // Печатает в консоль текущую и предыдущую команды для отладки последовательности.
  const now = Date.now();
  const previous = debugCommandState.lastPlanned || "-";
  const previousAt = debugCommandState.lastPlannedAt || 0;
  const deltaText = previousAt > 0 ? formatDurationMs(now - previousAt) : "00:00:00";
  debugCommandState.lastPlanned = command;
  debugCommandState.lastPlannedAt = now;
  const suffix = details ? ` | ${details}` : "";
  const message = `[${formatClockStamp()}] [${source}] ${command} | previous: ${previous} | +${deltaText}${suffix}`;
  console.log(message);
  sendDebugTraceLog(message);
}

function traceTimingReport(source, message) {
  // Пишет в консоль и backend-лог отдельную строку про время/планирование.
  const text = `[${formatClockStamp()}] [${source}] ${message}`;
  console.log(text);
  sendDebugTraceLog(text);
}

async function applySpectrumCommand(
  forceAllChannels = false,
  settleMs = COMMAND_PACING_MS.spectrumAdjust,
  showApplyToast = true
) {
  // Применяет значения спектральных каналов к выбранному AI/AG.
  // Вызывает backend API: api_scene_set_channel(ai, ag, channel, percent)
  // Для каждого канала отправляется отдельная команда COMA с паузой settleMs.
  const { ai, ag } = forceAllChannels
    ? getLuminaireProgrammingAddress()
    : getLuminaireAddress();

  const values = {
    red: getSpectrumInputValue(ui.specRed, 0),
    blue: getSpectrumInputValue(ui.specBlue, 0),
    farred: getSpectrumInputValue(ui.specFarRed, 0),
    white: getSpectrumInputValue(ui.specWhite, 0),
  };

  // Порядок как в PLT_1 (Unit7): Красный -> Синий -> Дальний красный -> Белый.
  const allChannels = ["red", "blue", "farred", "white"];

  // По запросу: при применении спектра всегда отправляем все 4 канала,
  // а не только последний измененный.
  const channelQueue = allChannels;

  const red = values.red;
  const blue = values.blue;
  const farRed = values.farred;
  const white = values.white;

  setSpectrumInputValue(ui.specRed, red);
  setSpectrumInputValue(ui.specBlue, blue);
  setSpectrumInputValue(ui.specFarRed, farRed);
  setSpectrumInputValue(ui.specWhite, white);

  const summaryLines = [];
  const traceAddress = resolveProtocolAddressForTrace(ai, ag);
  for (const channel of channelQueue) {
    const percent = values[channel];
    const plannedCommand = buildLegacySpectrumComaCommand(
      traceAddress,
      channel,
      Number(percent)
    );
    tracePlannedCommand(
      "SPECTRUM",
      plannedCommand,
      `${SPECTRUM_CHANNEL_LABELS[channel]}=${percent}%`
    );
    // Вызов backend: api_scene_set_channel отправляет команду COMA на контроллер.
    // Возвращает { ok: true, data: { command: "COMA...", lines: [...] } }
    const result = await runLuminaireCommand(
      () => callApi("api_scene_set_channel", ai, ag, channel, Number(percent)),
      settleMs
    );
    const commandText = String(result.command || "").trim();
    summaryLines.push(`Команда светильника: ${commandText}`);
    summaryLines.push(`Интерпретация: ${SPECTRUM_CHANNEL_LABELS[channel]} ${percent}%`);
    summaryLines.push("");
    spectrumState.dirty[channel] = false;
    if (spectrumState.lastEdited === channel) {
      spectrumState.lastEdited = null;
    }
  }

  setRawResponse(summaryLines);
  if (showApplyToast) {
    showToast(`Спектр применен: R${red}% B${blue}% FR${farRed}% W${white}%`, "success");
  }
  await refreshLogs(true);
}

async function applySpectrumSingleChannelCommand(channel, settleMs = COMMAND_PACING_MS.generic) {
  // Применяет один выбранный канал спектра по кнопке OK рядом с полем.
  const { ai, ag } = getLuminaireAddress();
  const channelNodeGetter = SPECTRUM_INPUT_NODES[channel];
  const channelNode = channelNodeGetter ? channelNodeGetter() : null;

  if (!channelNode) {
    throw new Error("Поле спектра не найдено");
  }

  const percent = getSpectrumInputValue(channelNode, 0);
  setSpectrumInputValue(channelNode, percent);

  const traceAddress = resolveProtocolAddressForTrace(ai, ag);
  const plannedCommand = buildLegacySpectrumComaCommand(traceAddress, channel, Number(percent));
  tracePlannedCommand(
    "SPECTRUM",
    plannedCommand,
    `${SPECTRUM_CHANNEL_LABELS[channel]}=${percent}%`
  );

  const result = await runLuminaireCommand(
    () => callApi("api_scene_set_channel", ai, ag, channel, Number(percent)),
    settleMs
  );

  spectrumState.dirty[channel] = false;
  if (spectrumState.lastEdited === channel) {
    spectrumState.lastEdited = null;
  }

  setRawResponse([
    `Команда светильника: ${String(result.command || "").trim()}`,
    `Интерпретация: ${SPECTRUM_CHANNEL_LABELS[channel]} ${percent}%`,
  ]);
  showToast(`${SPECTRUM_CHANNEL_LABELS[channel]} применен: ${percent}%`, "success");
  await refreshLogs(true);
}

async function confirmSpectrumStateCommand(showReadyToast = true) {
  // Применяет все 4 канала спектра и отмечает состояние как готовое для записи сцены.
  // Вызывается кнопкой "ОК спектр" (устаревшая логика, теперь используется "Применить спектр").
  await applySpectrumCommand(true, COMMAND_PACING_MS.spectrumBatch, false);
  spectrumCommitState.okReady = true;
  if (showReadyToast) {
    showToast("Спектр зафиксирован. Теперь можно нажать Запись.", "success");
  }
}

function scheduleScenarioRepeatCycle(repeatToken, delayMs) {
  // Планирует следующий запуск повтора без наложения таймеров.
  if (repeatToken !== scenarioRepeatState.token || scenarioRepeatState.intervalMs <= 0) {
    return;
  }

  scenarioRepeatState.nextRunAt = Date.now() + delayMs;
  traceTimingReport(
    "REPEAT",
    `Следующий запуск через ${formatDurationMs(delayMs)} (сцена ${scenarioRepeatState.scene ?? "-"})`
  );
  scenarioRepeatState.timerId = window.setTimeout(() => {
    runScenarioRepeatCycle(repeatToken);
  }, Math.max(0, delayMs));
  updateScenarioRepeatCountdown();
}

async function runScenarioRepeatCycle(repeatToken) {
  // Выполняет цикл повтора: выключение, пауза, запуск сценария.
  if (repeatToken !== scenarioRepeatState.token || scenarioRepeatState.intervalMs <= 0) {
    return;
  }

  scenarioRepeatState.timerId = null;
  if (scenarioRepeatState.busy) {
    scheduleScenarioRepeatCycle(repeatToken, scenarioRepeatState.intervalMs);
    return;
  }

  scenarioRepeatState.busy = true;
  traceTimingReport(
    "REPEAT",
    `Цикл запускается: пауза ${formatDurationMs(COMMAND_PACING_MS.repeatOffToPlay)} после выключения`
  );
  updateScenarioRepeatCountdown();

  try {
    await runLuminaireCommand(
      () => callApi("api_send_brightness", scenarioRepeatState.ai, scenarioRepeatState.ag, 0, null, null),
      COMMAND_PACING_MS.generic
    );

    if (repeatToken !== scenarioRepeatState.token) {
      return;
    }

    await waitMs(COMMAND_PACING_MS.repeatOffToPlay);

    if (repeatToken !== scenarioRepeatState.token) {
      return;
    }

    const result = await runLuminaireCommand(
      () => callApi("api_scene_activate", scenarioRepeatState.ai, scenarioRepeatState.ag, Number(scenarioRepeatState.scene)),
      COMMAND_PACING_MS.sceneActivate
    );

    if (result.lines) {
      setRawResponse(result.lines);
    }
    await refreshLogs(true);
  } catch (error) {
    if (repeatToken === scenarioRepeatState.token) {
      stopScenarioRepeat("Повтор остановлен из-за ошибки");
      showToast(`Ошибка повтора сценария: ${error.message}`, "error");
    }
    return;
  } finally {
    if (repeatToken === scenarioRepeatState.token) {
      scenarioRepeatState.busy = false;
      updateScenarioRepeatCountdown();
    }
  }

  if (repeatToken !== scenarioRepeatState.token || scenarioRepeatState.intervalMs <= 0) {
    return;
  }

  scheduleScenarioRepeatCycle(repeatToken, scenarioRepeatState.intervalMs);
}

function startScenarioRepeat(ai, ag, playScene, intervalMs) {
  // Запускает периодический цикл без гонок между запусками.
  stopScenarioRepeat("Повтор запускается...");

  const repeatToken = scenarioRepeatState.token;
  scenarioRepeatState.intervalMs = intervalMs;
  scenarioRepeatState.scene = Number(playScene);
  scenarioRepeatState.ai = ai;
  scenarioRepeatState.ag = ag;
  scenarioRepeatState.busy = false;

  traceTimingReport(
    "REPEAT",
    `Повтор включен: каждые ${formatDurationMs(intervalMs)} для сцены ${scenarioRepeatState.scene}`
  );

  scenarioRepeatState.countdownId = window.setInterval(() => {
    updateScenarioRepeatCountdown();
  }, 250);

  scheduleScenarioRepeatCycle(repeatToken, intervalMs);
}

function resolveScenarioSelection() {
  // Нормализует номера текущего/записи/воспроизведения сценария.
  const currentScene = setCurrentScenarioValue(ui.sceneCurrentSimple?.value);
  const saveSceneRaw = optionalFieldValue(ui.sceneSaveSimple);
  const playSceneRaw = optionalFieldValue(ui.scenePlaySimple);

  const saveScene = saveSceneRaw ? clampNumber(saveSceneRaw, 1, 20, currentScene) : currentScene;
  const playScene = playSceneRaw ? clampNumber(playSceneRaw, 1, 20, currentScene) : currentScene;

  if (ui.sceneSaveSimple && saveSceneRaw !== null) {
    ui.sceneSaveSimple.value = String(saveScene);
  }
  if (ui.scenePlaySimple && playSceneRaw !== null) {
    ui.scenePlaySimple.value = String(playScene);
  }

  return {
    currentScene,
    saveScene,
    playScene,
  };
}

async function saveScenarioCommand() {
  // Сохраняет текущие каналы в выбранный номер сценария.
  // Последовательность PLT_1 (Unit7):
  // 1. COMA AAA,14x - Красный канал (api_scene_set_channel)
  // 2. COMA AAA,16x - Синий канал (api_scene_set_channel)
  // 3. COMA AAA,18x - Дальний красный канал (api_scene_set_channel)
  // 4. COMA AAA,20x - Белый канал (api_scene_set_channel)
  // 5. Пауза перед записью
  // 6. COMA AAA,03N - запись сцены N (api_scene_save)
  const { ai, ag } = getLuminaireProgrammingAddress();
  const { saveScene } = resolveScenarioSelection();

  if (scenarioRepeatState.timerId !== null || scenarioRepeatState.busy) {
    stopScenarioRepeat("Повтор остановлен: запись сценария");
  }

  // PLT_1 последовательность: SetChannel 1-4 → WriteScene (03N).
  // Отправляем все 4 канала с текущими значениями из UI по порядку PLT_1.
  const saveStartTime = Date.now();
  traceTimingReport("SAVE", `Запись сцены ${saveScene}: отправка 4 каналов перед COMA 03N`);

  // Отправляем все 4 канала по порядку PLT_1: Красный → Синий → Дальний красный → Белый
  const values = {
    red: getSpectrumInputValue(ui.specRed, 0),
    blue: getSpectrumInputValue(ui.specBlue, 0),
    farred: getSpectrumInputValue(ui.specFarRed, 0),
    white: getSpectrumInputValue(ui.specWhite, 0),
  };
  const allChannels = ["red", "blue", "farred", "white"];
  const traceAddress = resolveProtocolAddressForTrace(ai, ag);

  traceTimingReport("SAVE", `Отправка 4 каналов: R=${values.red}% B=${values.blue}% FR=${values.farred}% W=${values.white}%`);

  let channelIndex = 0;
  for (const channel of allChannels) {
    const channelStart = Date.now();
    const percent = values[channel];
    const plannedCommand = buildLegacySpectrumComaCommand(traceAddress, channel, Number(percent));
    tracePlannedCommand(
      "SAVE",
      plannedCommand,
      `${SPECTRUM_CHANNEL_LABELS[channel]}=${percent}% (канал ${channelIndex + 1}/4)`
    );
    // Вызов backend: api_scene_set_channel - отправляет COMA AAA,CCC для канала.
    // backend преобразует percent в legacy масштаб (0, 1-10→1, 15→2, ...)
    await runLuminaireCommand(
      () => callApi("api_scene_set_channel", ai, ag, channel, Number(percent), true),
      COMMAND_PACING_MS.spectrum
    );
    // Увеличенная пауза для гарантированной фиксации канала перед следующим.
    await waitMs(COMMAND_PACING_MS.spectrumSaveChannelSettle);
    const channelTime = Date.now() - channelStart;
    traceTimingReport("SAVE", `Канал ${channelIndex + 1}/4 (${channel}) отправлен за ${channelTime}мс`);
    channelIndex++;
  }

  const totalChannelsTime = Date.now() - saveStartTime;
  traceTimingReport("SAVE", `Все 4 канала отправлены за ${totalChannelsTime}мс, пауза перед записью сцены...`);

  // Увеличенная пауза перед COMA 03N, чтобы контроллер успел применить спектр.
  await waitMs(COMMAND_PACING_MS.spectrumSaveBeforeCommit);

  traceTimingReport("SAVE", `Запись сцены ${saveScene} начинается`);
  tracePlannedCommand(
    "SAVE",
    buildPlannedComaCommand(resolveProtocolAddressForTrace(ai, ag), 30 + Number(saveScene)),
    `сцена=${saveScene}`
  );

  // Вызов backend: api_scene_save - отправляет COMA AAA,03N (запись сцены N)
  // backend формирует команду 30+saveScene и отправляет fire-and-forget
  const result = await runLuminaireCommand(
    () => callApi("api_scene_save", ai, ag, Number(saveScene)),
    COMMAND_PACING_MS.sceneSave
  );
  setRawResponse(result.lines || []);
  setCurrentScenarioValue(saveScene);
  await refreshLogs(true);
  showToast(`Сценарий ${saveScene} записан: R${values.red}% B${values.blue}% FR${values.farred}% W${values.white}%`, "success");
}

async function playScenarioCommand() {
  // Воспроизводит выбранный сценарий и при необходимости запускает повтор.
  // Вызов backend: api_scene_activate - отправляет COMA AAA,01N (активация сцены N)
  // backend формирует команду 10+playScene и отправляет fire-and-forget
  const { ai, ag } = getLuminaireAddress();
  const { playScene } = resolveScenarioSelection();

  traceTimingReport("PLAY", `Воспроизведение сцены ${playScene} начинается`);
  tracePlannedCommand(
    "PLAY",
    buildPlannedComaCommand(resolveProtocolAddressForTrace(ai, ag), 10 + Number(playScene)),
    `сцена=${playScene}`
  );

  // Вызов backend: api_scene_activate - активация сцены в контроллере
  const playResult = await runLuminaireCommand(
    () => callApi("api_scene_activate", ai, ag, Number(playScene)),
    COMMAND_PACING_MS.sceneActivate
  );
  setRawResponse(playResult.lines || []);
  setCurrentScenarioValue(playScene);
  if (ui.sceneSaveSimple) {
    ui.sceneSaveSimple.value = "";
  }
  await refreshLogs(true);

  const repeatEnabled = Boolean(ui.scenarioRepeatEnabled?.checked);
  if (!repeatEnabled) {
    stopScenarioRepeat("Повтор выключен");
    showToast(`Сценарий ${playScene} воспроизведен`, "success");
    return;
  }

  const { hours, minutes, seconds } = normalizeScenarioRepeatFields();
  const totalSeconds = hours * 3600 + minutes * 60 + seconds;
  if (totalSeconds < 1) {
    throw new Error("Интервал повтора должен быть не меньше 1 секунды");
  }

  const intervalLabel = formatRepeatInterval(hours, minutes, seconds);
  startScenarioRepeat(ai, ag, playScene, totalSeconds * 1000);
  showToast(`Сценарий ${playScene} запущен, повтор каждые ${intervalLabel}`, "success");
}

function showToast(message, tone = "info") {
  // Показывает всплывающее уведомление выбранного типа.
  const toast = document.createElement("div");
  toast.className = `toast ${tone}`;
  toast.textContent = message;
  ui.toastStack.appendChild(toast);
  setTimeout(() => {
    toast.remove();
  }, 3800);
}

function setButtonBusy(button, busy, pendingText = "Выполняется...") {
  // Блокирует кнопку и меняет подпись на время выполнения действия.
  if (!button) {
    return;
  }
  if (!button.dataset.defaultLabel) {
    button.dataset.defaultLabel = button.textContent;
  }
  button.disabled = busy;
  button.textContent = busy ? pendingText : button.dataset.defaultLabel;
}

async function withBusy(button, pendingText, action) {
  // Выполняет асинхронное действие, гарантируя включение/выключение busy-состояния.
  setButtonBusy(button, true, pendingText);
  try {
    return await action();
  } finally {
    setButtonBusy(button, false);
  }
}

async function callApi(method, ...args) {
  // Унифицированный вызов Eel API с обработкой типового формата ответа.
  // Все вызовы backend (Python) идут через эту функцию.
  // Формат ответа: { ok: true, data: {...} } или { ok: false, error: "..." }
  if (!eel || !eel[method]) {
    throw new Error(`Метод Eel не найден: ${method}`);
  }
  const response = await eel[method](...args)();
  if (!response || !response.ok) {
    throw new Error((response && response.error) || "Неизвестная ошибка backend");
  }
  return response.data;
}

function trayCloseWindow() {
  // Закрывает окно по запросу backend при выходе из трея.
  try {
    window.open("", "_self");
    window.close();
  } catch (_error) {
    // Пусто: в некоторых браузерных оболочках close может быть ограничен.
  }
  if (!window.closed) {
    window.location.href = "about:blank";
  }
}

if (typeof eel !== "undefined" && typeof eel.expose === "function") {
  eel.expose(trayCloseWindow, "tray_close_window");
}

function populateDatalist(node, values) {
  // Заполняет datalist списком значений-подсказок.
  node.innerHTML = "";
  for (const value of values || []) {
    const option = document.createElement("option");
    option.value = value;
    node.appendChild(option);
  }
}

function normalizePortList(values) {
  // Нормализует список портов к уникальному формату COMx с сортировкой по номеру.
  const unique = new Set();
  for (const raw of values || []) {
    const value = String(raw ?? "").trim().toUpperCase();
    if (/^COM\d+$/.test(value)) {
      unique.add(value);
    }
  }

  return Array.from(unique).sort((left, right) => Number(left.slice(3)) - Number(right.slice(3)));
}

function renderPortQuickList(ports) {
  // Рендерит кликабельные кнопки COM-портов как fallback для datalist.
  if (!ui.portQuickList) {
    return;
  }

  const normalized = normalizePortList(ports);
  ui.portQuickList.innerHTML = "";
  ui.portQuickList.classList.toggle("empty", normalized.length === 0);

  if (!normalized.length) {
    ui.portQuickList.textContent = "Порты не обнаружены";
    return;
  }

  const current = String(ui.portInput?.value || "").trim().toUpperCase();
  for (const port of normalized) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "port-chip";
    if (port === current) {
      button.classList.add("active");
    }
    button.textContent = port;
    button.addEventListener("click", () => {
      ui.portInput.value = port;
      renderPortQuickList(portState.items);
    });
    ui.portQuickList.appendChild(button);
  }
}

function updateConnectionBadges(connection) {
  // Обновляет индикаторы статуса подключения.
  const isConnected = Boolean(connection.connected);
  ui.statusBadge.textContent = isConnected ? "Подключено" : "Отключено";
  ui.statusBadge.classList.toggle("online", isConnected);
  ui.statusBadge.classList.toggle("offline", !isConnected);

  ui.modeBadge.textContent = "Реальное устройство";
  ui.modeBadge.classList.remove("mode-sim");
  ui.modeBadge.classList.add("mode-real");

  if (connection.port) {
    ui.portInput.value = connection.port;
  }
  if (connection.baudrate) {
    ui.baudInput.value = connection.baudrate;
  }
}

function fillLocalTimeFields() {
  // Подставляет в поля текущее локальное время и дату компьютера.
  const now = new Date();
  const day = ((now.getDay() + 6) % 7) + 1;
  ui.timeValue.value = `${pad2(now.getHours())}:${pad2(now.getMinutes())}:${pad2(now.getSeconds())}`;
  ui.dayValue.value = day;
  ui.dateValue.value = `${pad2(now.getDate())}.${pad2(now.getMonth() + 1)}.${String(now.getFullYear()).slice(-2)}`;
}

function formatScheduleTimeLabel(timeValue, signValue = "+") {
  // Формирует подпись времени в двух форматах: 24h и AM/PM.
  const raw = String(timeValue || "00:00").trim();
  const match = raw.match(/^(\d{1,2}):(\d{2})$/);
  const sign = signValue === "-" ? "-" : "+";

  if (!match) {
    return `${sign}${raw}`;
  }

  const hours24 = clampNumber(match[1], 0, 23, 0);
  const minutes = clampNumber(match[2], 0, 59, 0);
  const suffix = hours24 >= 12 ? "PM" : "AM";
  const hours12base = hours24 % 12;
  const hours12 = hours12base === 0 ? 12 : hours12base;

  return `${sign}${pad2(hours24)}:${pad2(minutes)} (${hours12}:${pad2(minutes)} ${suffix})`;
}

function renderSchedule(entries) {
  // Рендерит таблицу расписания из массива записей SHED.
  ui.scheduleBody.innerHTML = "";
  const data = entries || [];
  const filterMode = ui.scheduleFilter?.value || "all";
  const filtered =
    filterMode === "active"
      ? data.filter((item) => Boolean(item.active))
      : filterMode === "inactive"
        ? data.filter((item) => !Boolean(item.active))
        : data;

  if (!filtered.length) {
    const row = document.createElement("tr");
    const cell = document.createElement("td");
    cell.colSpan = 8;
    cell.textContent = data.length ? "Нет записей для выбранного фильтра" : "Записей нет";
    row.appendChild(cell);
    ui.scheduleBody.appendChild(row);
    ui.scheduleCount.textContent = data.length ? `0 из ${data.length} записей` : "0 записей";
    return;
  }

  for (const item of filtered) {
    const row = document.createElement("tr");
    const days = (item.days || [])
      .map((flag, index) => (flag ? String(index + 1) : "-"))
      .join("");

    const cells = [
      item.index,
      item.active ? "Да" : "Нет",
      days,
      TIME_TYPE_MAP[item.time_type] || "Неизвестно",
      formatScheduleTimeLabel(item.time || "00:00", item.sign || "+"),
      item.address,
      item.command,
      item.level,
    ];

    for (const value of cells) {
      const cell = document.createElement("td");
      cell.textContent = String(value);
      row.appendChild(cell);
    }

    row.addEventListener("click", () => fillScheduleEditor(item));
    ui.scheduleBody.appendChild(row);
  }

  ui.scheduleCount.textContent =
    filtered.length === data.length
      ? `${data.length} записей`
      : `${filtered.length} из ${data.length} записей`;
}

function setScheduleEntries(entries) {
  // Обновляет кеш расписания и перерисовывает таблицу с текущим фильтром.
  scheduleState.entries = Array.isArray(entries) ? entries : [];
  renderSchedule(scheduleState.entries);
}

function fillScheduleEditor(item) {
  // Заполняет форму редактирования на основе выбранной строки расписания.
  if (!item) {
    return;
  }

  ui.schedIndex.value = item.index ?? 0;
  ui.schedActive.checked = Boolean(item.active);
  ui.schedTimeType.value = String(item.time_type ?? 0);
  ui.schedSign.value = item.sign === "-" ? "-" : "+";

  const [hours, minutes] = String(item.time || "00:00").split(":");
  ui.schedHour.value = Number(hours || 0);
  ui.schedMin.value = Number(minutes || 0);
  ui.schedLevel.value = Number(item.level ?? 0);

  const days = item.days || [];
  [ui.schedD1, ui.schedD2, ui.schedD3, ui.schedD4, ui.schedD5, ui.schedD6, ui.schedD7].forEach(
    (node, index) => {
      node.checked = Boolean(days[index]);
    }
  );

  ui.schedAI.value = "";
  ui.schedAG.value = "";
  ui.schedTargetMode.value = "ai";
  ui.schedKeyA.checked = false;
  ui.schedKeyB.checked = false;
  ui.schedKeyC.checked = false;
  clearScheduleActionFields();

  const address = Number(item.address ?? 0);
  const command = Number(item.command ?? 0);

  if (address === 250) {
    ui.schedTargetMode.value = "keys";
    ui.schedKeyA.checked = (command & 1) !== 0;
    ui.schedKeyB.checked = (command & 2) !== 0;
    ui.schedKeyC.checked = (command & 4) !== 0;
  } else if (address === 251) {
    ui.schedTargetMode.value = "diag";
    // Совместимость с PLT_1: DIAG хранит биты в level (100/010/001).
    // Для старых записей оставляем fallback на битовую маску в command.
    const diagLevel = Number(item.level ?? 0);
    if (diagLevel > 0) {
      ui.schedKeyA.checked = Math.trunc(diagLevel / 100) > 0;
      ui.schedKeyB.checked = Math.trunc((diagLevel % 100) / 10) > 0;
      ui.schedKeyC.checked = (diagLevel % 10) > 0;
    } else {
      ui.schedKeyA.checked = (command & 1) !== 0;
      ui.schedKeyB.checked = (command & 2) !== 0;
      ui.schedKeyC.checked = (command & 4) !== 0;
    }
  } else {
    if (address === 0) {
      ui.schedAG.value = "0";
    } else if (address >= 221 && address <= 249) {
      ui.schedAG.value = String(address - 220);
    } else {
      ui.schedAI.value = String(address);
    }

    if (command >= 0 && command <= 10) {
      ui.schedBrightness.value = String(command);
    } else if (command >= 11 && command <= 30) {
      ui.schedScene.value = String(command - 10);
    } else {
      ui.schedCommandCode.value = String(command);
    }
  }

  syncScheduleTimeUIFromLegacyFields();
  syncScheduleActionModeFromLegacyFields();
  updateScheduleTargetModeUI();
}

function renderLogs(items) {
  // Выводит журнал обмена в текстовый блок с автопрокруткой вниз.
  const data = (items || []).filter((item) => {
    const text = String(item?.text || "");
    return !/^Таймаут: нет ответа на 'COMA/i.test(text);
  });
  if (!data.length) {
    ui.logView.textContent = "Трафик пока отсутствует.";
    return;
  }
  ui.logView.textContent = data
    .map((item) => `${item.ts}  ${String(item.dir).toUpperCase().padEnd(3, " ")}  ${item.text}`)
    .join("\n");
  ui.logView.scrollTop = ui.logView.scrollHeight;
}

function setRawResponse(lines) {
  // Показывает сырой ответ устройства в блоке консоли.
  const output = (lines || []).join("\n").trim();
  ui.rawResponse.textContent = output || "<нет ответа>";
}

function setLogMeta(logFilePath) {
  // Показывает расположение файла постоянного лога для диагностики ошибок.
  if (!ui.logMeta) {
    return;
  }

  const path = String(logFilePath || "").trim();
  ui.logMeta.textContent = path ? `Файл лога: ${path}` : "Файл лога: не определен";
}

async function refreshLogs(silent = true) {
  // Обновляет лог из backend и при необходимости показывает ошибку.
  // Вызов backend: api_get_logs(limit) - чтение последних строк журнала обмена
  try {
    const payload = await callApi("api_get_logs", 320);
    renderLogs(payload.items || []);
  } catch (error) {
    if (!silent) {
      showToast(error.message, "error");
    }
  }
}

function applyTheme(them) {
  // Применяет тему по коду Theme: 1 (светлая), 0 (темная).
  const themValue = normalizeThemValue(them);
  const nextTheme = themValue === 1 ? "light" : "dark";
  document.body.dataset.theme = nextTheme;
  ui.themeToggleBtn.textContent = themValue === 1 ? "Тема: светлая (Theme=1)" : "Тема: темная (Theme=0)";
  return themValue;
}

function toggleTheme() {
  // Переключает тему и синхронизирует значение Them в backend и localStorage.
  const currentThem = document.body.dataset.theme === "dark" ? 0 : 1;
  const nextThem = currentThem === 1 ? 0 : 1;
  const appliedThem = applyTheme(nextThem);
  localStorage.setItem(THEME_STORAGE_KEY, String(appliedThem));
  // Вызов backend: api_set_theme(them) - сохранение темы в config.ini
  callApi("api_set_theme", appliedThem).catch((error) => {
    showToast(error.message, "error");
  });
}

function initTheme(them = null) {
  // Инициализирует тему из аргумента, localStorage или системных настроек.
  if (them !== null && them !== undefined && them !== "") {
    const appliedThem = applyTheme(them);
    localStorage.setItem(THEME_STORAGE_KEY, String(appliedThem));
    return;
  }

  const saved = localStorage.getItem(THEME_STORAGE_KEY);
  if (saved === "0" || saved === "1") {
    applyTheme(Number(saved));
    return;
  }

  const legacySaved = localStorage.getItem(LEGACY_THEME_STORAGE_KEY);
  if (legacySaved === "dark" || legacySaved === "light") {
    const themFromLegacy = legacySaved === "dark" ? 0 : 1;
    const appliedThem = applyTheme(themFromLegacy);
    localStorage.setItem(THEME_STORAGE_KEY, String(appliedThem));
    return;
  }

  const prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  const appliedThem = applyTheme(prefersDark ? 0 : 1);
  localStorage.setItem(THEME_STORAGE_KEY, String(appliedThem));
}

function switchPage(pageId) {
  // Переключает отображаемую страницу и активную кнопку вкладки.
  ui.pages.forEach((page) => {
    page.classList.toggle("active", page.id === pageId);
  });
  ui.pageTabs.forEach((tab) => {
    tab.classList.toggle("active", tab.dataset.page === pageId);
  });
}

function initPages() {
  // Подключает обработчики вкладок для разбиения интерфейса на страницы.
  ui.pageTabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      switchPage(tab.dataset.page);
    });
  });
}

function collectSchedulePayload() {
  // Собирает payload редактора расписания для API записи SHED.
  syncScheduleLegacyTimeFieldsFromUI();
  syncScheduleActionFieldsFromUI();

  const targetMode = ui.schedTargetMode.value;
  const isAiMode = targetMode === "ai";

  return {
    index: Number(ui.schedIndex.value),
    active: ui.schedActive.checked,
    days: [
      ui.schedD1.checked,
      ui.schedD2.checked,
      ui.schedD3.checked,
      ui.schedD4.checked,
      ui.schedD5.checked,
      ui.schedD6.checked,
      ui.schedD7.checked,
    ],
    time_type: Number(ui.schedTimeType.value),
    sign: ui.schedSign.value,
    hours: Number(ui.schedHour.value),
    minutes: Number(ui.schedMin.value),
    target_mode: targetMode,
    ai: isAiMode ? optionalFieldValue(ui.schedAI) : null,
    ag: isAiMode ? optionalFieldValue(ui.schedAG) : null,
    brightness: isAiMode ? optionalFieldValue(ui.schedBrightness) : null,
    scene: isAiMode ? optionalFieldValue(ui.schedScene) : null,
    command_code: isAiMode ? optionalFieldValue(ui.schedCommandCode) : null,
    key_a: ui.schedKeyA.checked,
    key_b: ui.schedKeyB.checked,
    key_c: ui.schedKeyC.checked,
    level: Number(ui.schedLevel.value),
  };
}

async function bootstrap() {
  // Выполняет первичную инициализацию интерфейса и исходных данных.
  // Вызов backend: api_bootstrap - возвращает конфигурацию, порты, логи, шаблоны команд
  try {
    ui.astroYear.value = String(new Date().getFullYear());

    // Получение начальных данных из backend: подключение, порты, конфиг, логи
    const data = await callApi("api_bootstrap");
    const cfg = data.config || {};
    ui.portInput.value = cfg.port_name || "COM4";
    ui.baudInput.value = cfg.baudrate || 9600;
    initTheme(cfg.them);

    updateConnectionBadges(data.connection || {});
    const ports = normalizePortList(data.ports || []);
    portState.items = ports;
    populateDatalist(ui.portHints, ports);
    renderPortQuickList(ports);
    setLogMeta(data.log_file);

    const currentPort = String(ui.portInput.value || "").trim().toUpperCase();
    if (ports.length && (!currentPort || !ports.includes(currentPort))) {
      ui.portInput.value = ports[0];
      renderPortQuickList(ports);
    }

    populateDatalist(ui.commandHints, data.command_templates || []);

    if (!ui.rawCommand.value && data.command_templates && data.command_templates.length) {
      ui.rawCommand.value = data.command_templates[0];
    }

    fillLocalTimeFields();
    await refreshLogs(false);
  } catch (error) {
    showToast(error.message, "error");
  }
}

function wireEvents() {
  // Подключает обработчики всех кнопок, полей и переключателей интерфейса.
  ui.themeToggleBtn.addEventListener("click", () => {
    toggleTheme();
  });

  const singleSpectrumButtons = [
    { node: ui.specRedApplyBtn, channel: "red" },
    { node: ui.specBlueApplyBtn, channel: "blue" },
    { node: ui.specFarRedApplyBtn, channel: "farred" },
    { node: ui.specWhiteApplyBtn, channel: "white" },
  ];

  singleSpectrumButtons.forEach(({ node, channel }) => {
    node?.addEventListener("click", () =>
      withBusy(node, "Отправка...", async () => {
        if (scenarioRepeatState.timerId !== null || scenarioRepeatState.busy) {
          stopScenarioRepeat("Повтор остановлен: ручное управление спектром");
        }
        await applySpectrumSingleChannelCommand(channel);
      }).catch((error) => showToast(error.message, "error"))
    );
  });

  // Кнопка "Применить спектр" - применяет все 4 канала к светильнику без записи в сцену.
  ui.applySpectrumBtn?.addEventListener("click", () =>
    withBusy(ui.applySpectrumBtn, "Применение...", async () => {
      if (scenarioRepeatState.timerId !== null || scenarioRepeatState.busy) {
        stopScenarioRepeat("Повтор остановлен: ручное управление спектром");
      }
      // По кнопке применяем полный спектр с межкомандным интервалом 2.5 сек.
      await applySpectrumCommand(false);
    }).catch((error) => showToast(error.message, "error"))
  );

  ui.saveScenarioBtn?.addEventListener("click", () =>
    withBusy(ui.saveScenarioBtn, "Запись...", async () => {
      await saveScenarioCommand();
    }).catch((error) => showToast(error.message, "error"))
  );

  ui.playScenarioBtn?.addEventListener("click", () =>
    withBusy(ui.playScenarioBtn, "Воспроизведение...", async () => {
      await playScenarioCommand();
    }).catch((error) => showToast(error.message, "error"))
  );

  ui.stopScenarioRepeatBtn?.addEventListener("click", () => {
    stopScenarioRepeat("Повтор остановлен вручную");
    showToast("Повтор сценария остановлен", "info");
  });

  ui.connectBtn.addEventListener("click", () =>
    withBusy(ui.connectBtn, "Подключение...", async () => {
      // Вызов backend: api_connect(port, baudrate) - подключение к COM-порту
      // Возвращает статус подключения и предупреждения об ошибках
      const payload = await callApi(
        "api_connect",
        ui.portInput.value.trim(),
        Number(ui.baudInput.value)
      );
      updateConnectionBadges(payload);
      if (payload.warning) {
        showToast(payload.warning, "error");
      } else {
        showToast("Подключение обновлено", "success");
      }
      await refreshLogs(true);
    }).catch((error) => showToast(error.message, "error"))
  );

  ui.disconnectBtn.addEventListener("click", () =>
    withBusy(ui.disconnectBtn, "Отключение...", async () => {
      // Вызов backend: api_disconnect() - закрытие COM-порта
      const payload = await callApi("api_disconnect");
      updateConnectionBadges(payload);
      stopScenarioRepeat("Повтор выключен");
      showToast("Соединение закрыто", "info");
      await refreshLogs(true);
    }).catch((error) => showToast(error.message, "error"))
  );

  ui.refreshPortsBtn.addEventListener("click", () =>
    withBusy(ui.refreshPortsBtn, "Сканирование...", async () => {
      // Вызов backend: api_refresh_ports() - сканирование доступных COM-портов
      // Возвращает список портов в формате ["COM1", "COM3", "COM4", ...]
      const ports = normalizePortList(await callApi("api_refresh_ports"));
      portState.items = ports;
      populateDatalist(ui.portHints, ports);
      renderPortQuickList(ports);

      if (ports.length) {
        const currentPort = String(ui.portInput.value || "").trim().toUpperCase();
        if (!currentPort || !ports.includes(currentPort)) {
          ui.portInput.value = ports[0];
          renderPortQuickList(ports);
        }
        showToast(`Найдено портов: ${ports.length}`, "info");
      } else {
        showToast("COM-порты не обнаружены", "info");
      }
    }).catch((error) => showToast(error.message, "error"))
  );

  ui.portInput.addEventListener("input", () => {
    renderPortQuickList(portState.items);
  });

  ui.saveConnBtn.addEventListener("click", () =>
    withBusy(ui.saveConnBtn, "Сохранение...", async () => {
      // Вызов backend: api_save_connection(port, baudrate) - сохранение параметров в config.ini
      await callApi("api_save_connection", ui.portInput.value.trim(), Number(ui.baudInput.value));
      showToast("Параметры соединения сохранены", "success");
    }).catch((error) => showToast(error.message, "error"))
  );

  ui.sendComBtn.addEventListener("click", () =>
    withBusy(ui.sendComBtn, "Отправка...", async () => {
      // Вызов backend: api_send_com(address, code) - отправка команды COM AAA,CCC
      const payload = await callApi(
        "api_send_com",
        Number(ui.comAddress.value),
        Number(ui.comCode.value)
      );
      setRawResponse(payload.lines);
      showToast(`Отправлено: ${payload.command}`, "success");
      await refreshLogs(true);
    }).catch((error) => showToast(error.message, "error"))
  );

  ui.readTimeBtn.addEventListener("click", () =>
    withBusy(ui.readTimeBtn, "Чтение...", async () => {
      // Вызов backend: api_read_time() - чтение TIME из контроллера
      const payload = await callApi("api_read_time");
      ui.timeValue.value = payload.time;
      ui.dayValue.value = payload.day;
      ui.dateValue.value = payload.date;
      setRawResponse(payload.lines);
      showToast("Время считано", "success");
      await refreshLogs(true);
    }).catch((error) => showToast(error.message, "error"))
  );

  ui.localTimeBtn.addEventListener("click", () => {
    fillLocalTimeFields();
    showToast("Локальное время подставлено", "info");
  });

  ui.writeTimeBtn.addEventListener("click", () =>
    withBusy(ui.writeTimeBtn, "Запись...", async () => {
      // Вызов backend: api_set_time(time, day, date) - запись TIME в контроллер
      const payload = await callApi(
        "api_set_time",
        ui.timeValue.value.trim(),
        Number(ui.dayValue.value),
        ui.dateValue.value.trim()
      );
      setRawResponse(payload.lines);
      showToast(`Отправлено: ${payload.command}`, "success");
      await refreshLogs(true);
    }).catch((error) => showToast(error.message, "error"))
  );

  ui.readGeoBtn.addEventListener("click", () =>
    withBusy(ui.readGeoBtn, "Чтение...", async () => {
      // Вызов backend: api_read_geo() - чтение GEONEZ (широта, долгота, пояс)
      const payload = await callApi("api_read_geo");
      ui.latValue.value = payload.lat;
      ui.lonValue.value = payload.lon;
      ui.zoneValue.value = payload.zone;
      setRawResponse(payload.lines);
      showToast("Координаты считаны", "success");
      await refreshLogs(true);
    }).catch((error) => showToast(error.message, "error"))
  );

  ui.writeGeoBtn.addEventListener("click", () =>
    withBusy(ui.writeGeoBtn, "Запись...", async () => {
      // Вызов backend: api_set_geo(lat, lon, zone) - запись GEONEZ в контроллер
      const payload = await callApi(
        "api_set_geo",
        Number(ui.latValue.value),
        Number(ui.lonValue.value),
        Number(ui.zoneValue.value)
      );
      setRawResponse(payload.lines);
      showToast(`Отправлено: ${payload.command}`, "success");
      await refreshLogs(true);
    }).catch((error) => showToast(error.message, "error"))
  );

  ui.sendBrightnessBtn.addEventListener("click", () =>
    withBusy(ui.sendBrightnessBtn, "Отправка...", async () => {
      // Вызов backend: api_send_brightness(ai, ag, brightness, scene, command_code)
      // Отправляет команду яркости/сцены/сервисного кода на светильник
      const action = collectBrightnessAction();
      const payload = await callApi(
        "api_send_brightness",
        action.ai,
        action.ag,
        action.brightness,
        action.scene,
        action.command_code
      );
      setRawResponse(payload.lines);
      showToast(`Отправлено: ${payload.command}`, "success");
      await refreshLogs(true);
    }).catch((error) => showToast(error.message, "error"))
  );

  ui.generateAstronomyBtn.addEventListener("click", () =>
    withBusy(ui.generateAstronomyBtn, "Расчет...", async () => {
      // Вызов backend: api_generate_astronomy(lat, lon, zone, year, morning_corr, evening_corr)
      // Генерирует файлы астрономического расписания на указанный год
      const payload = await callApi(
        "api_generate_astronomy",
        Number(ui.latValue.value),
        Number(ui.lonValue.value),
        Number(ui.zoneValue.value),
        Number(ui.astroYear.value),
        Number(ui.astroMorningCorr.value),
        Number(ui.astroEveningCorr.value)
      );

      ui.astronomyResult.textContent = [
        `Год: ${payload.year}`,
        `Файлы: ${payload.text_file}, ${payload.csv_file}`,
        `Коррекция: утро ${payload.morning_correction} мин, вечер ${payload.evening_correction} мин`,
        `Суммарная наработка света: ${payload.total_hours} ч (${payload.total_minutes} мин)`,
      ].join("\n");
      showToast("Астрономические файлы сформированы", "success");
    }).catch((error) => showToast(error.message, "error"))
  );

  ui.readKeysBtn.addEventListener("click", () =>
    withBusy(ui.readKeysBtn, "Чтение...", async () => {
      // Вызов backend: api_read_keys() - чтение состояния KEYS (биты A/B/C)
      const payload = await callApi("api_read_keys");
      ui.keysA.checked = payload.a;
      ui.keysB.checked = payload.b;
      ui.keysC.checked = payload.c;
      setRawResponse(payload.lines);
      showToast("KEYS считаны", "success");
      await refreshLogs(true);
    }).catch((error) => showToast(error.message, "error"))
  );

  ui.writeKeysBtn.addEventListener("click", () =>
    withBusy(ui.writeKeysBtn, "Запись...", async () => {
      // Вызов backend: api_set_keys(a, b, c) - запись состояния KEYS (битовая маска)
      const payload = await callApi("api_set_keys", ui.keysA.checked, ui.keysB.checked, ui.keysC.checked);
      setRawResponse(payload.lines);
      showToast(`Отправлено: ${payload.command}`, "success");
      await refreshLogs(true);
    }).catch((error) => showToast(error.message, "error"))
  );

  ui.readMaskBtn.addEventListener("click", () =>
    withBusy(ui.readMaskBtn, "Чтение...", async () => {
      // Вызов backend: api_read_mask() - чтение состояния MASK (биты A/B/C)
      const payload = await callApi("api_read_mask");
      ui.maskA.checked = payload.a;
      ui.maskB.checked = payload.b;
      ui.maskC.checked = payload.c;
      setRawResponse(payload.lines);
      showToast("MASK считана", "success");
      await refreshLogs(true);
    }).catch((error) => showToast(error.message, "error"))
  );

  ui.writeMaskBtn.addEventListener("click", () =>
    withBusy(ui.writeMaskBtn, "Запись...", async () => {
      // Вызов backend: api_set_mask(a, b, c) - запись состояния MASK (битовая маска)
      const payload = await callApi("api_set_mask", ui.maskA.checked, ui.maskB.checked, ui.maskC.checked);
      setRawResponse(payload.lines);
      showToast(`Отправлено: ${payload.command}`, "success");
      await refreshLogs(true);
    }).catch((error) => showToast(error.message, "error"))
  );

  ui.adrPrgBtn.addEventListener("click", () =>
    withBusy(ui.adrPrgBtn, "Отправка...", async () => {
      // Вызов backend: api_enable_address_programming() - установка ADRPRG=1
      // Разрешает запись нового AI-адреса через COM 255
      const payload = await callApi("api_enable_address_programming");
      setRawResponse(payload.lines);
      showToast(`Отправлено: ${payload.command}`, "success");
      await refreshLogs(true);
    }).catch((error) => showToast(error.message, "error"))
  );

  ui.setAiBtn.addEventListener("click", () =>
    withBusy(ui.setAiBtn, "Запись...", async () => {
      // Вызов backend: api_set_ai_address(new_ai) - запись нового AI-адреса (COM 255,AI)
      const payload = await callApi("api_set_ai_address", Number(ui.aiProgramValue.value));
      setRawResponse(payload.lines);
      showToast(`Новый AI записан: ${payload.ai}`, "success");
      await refreshLogs(true);
    }).catch((error) => showToast(error.message, "error"))
  );

  ui.grpApplyBtn.addEventListener("click", () =>
    withBusy(ui.grpApplyBtn, "Отправка...", async () => {
      // Вызов backend: api_assign_group_slot(ai, ag, slot, number, clear)
      // Назначение группы AG в слот (Unit3) или очистка назначений
      const adr = resolveAddressFields(ui.grpAI, ui.grpAG);
      const payload = await callApi(
        "api_assign_group_slot",
        adr.ai,
        adr.ag,
        Number(ui.grpSlot.value),
        Number(ui.grpNumber.value),
        ui.grpClear.checked
      );
      setRawResponse(payload.lines);
      showToast(payload.cleared ? "Группы очищены" : `Отправлено: ${payload.command}`, "success");
      await refreshLogs(true);
    }).catch((error) => showToast(error.message, "error"))
  );

  ui.sceneActivateBtn.addEventListener("click", () =>
    withBusy(ui.sceneActivateBtn, "Отправка...", async () => {
      // Вызов backend: api_scene_activate(ai, ag, scene_no) - выполнение сценария (COMA AAA,01N)
      const adr = resolveAddressFields(ui.sceneAI, ui.sceneAG);
      const payload = await callApi("api_scene_activate", adr.ai, adr.ag, Number(ui.sceneReadNo.value));
      setRawResponse(payload.lines);
      showToast(`Отправлено: ${payload.command}`, "success");
      await refreshLogs(true);
    }).catch((error) => showToast(error.message, "error"))
  );

  ui.sceneSaveBtn.addEventListener("click", () =>
    withBusy(ui.sceneSaveBtn, "Отправка...", async () => {
      // Вызов backend: api_scene_save(ai, ag, scene_no) - запись сценария (COMA AAA,03N)
      // Внимание: не отправляет каналы, только финальную команду записи!
      const adr = resolveAddressFields(ui.sceneAI, ui.sceneAG);
      const payload = await callApi("api_scene_save", adr.ai, adr.ag, Number(ui.sceneWriteNo.value));
      setRawResponse(payload.lines);
      showToast(`Отправлено: ${payload.command}`, "success");
      await refreshLogs(true);
    }).catch((error) => showToast(error.message, "error"))
  );

  ui.sceneStartBtn.addEventListener("click", () =>
    withBusy(ui.sceneStartBtn, "Отправка...", async () => {
      // Вызов backend: api_scene_set_start(ai, ag) - установка стартового сценария (COMA AAA,220)
      const adr = resolveAddressFields(ui.sceneAI, ui.sceneAG);
      const payload = await callApi("api_scene_set_start", adr.ai, adr.ag);
      setRawResponse(payload.lines);
      showToast(`Отправлено: ${payload.command}`, "success");
      await refreshLogs(true);
    }).catch((error) => showToast(error.message, "error"))
  );

  ui.sceneChannelBtn.addEventListener("click", () =>
    withBusy(ui.sceneChannelBtn, "Отправка...", async () => {
      // Вызов backend: api_scene_set_channel(ai, ag, channel, percent)
      // Отправка команды спектрального канала (COMA AAA,14x/16x/18x/20x)
      const adr = resolveAddressFields(ui.sceneAI, ui.sceneAG);
      const payload = await callApi(
        "api_scene_set_channel",
        adr.ai,
        adr.ag,
        ui.sceneChannel.value,
        Number(ui.scenePercent.value)
      );
      setRawResponse(payload.lines);
      showToast(`Отправлено: ${payload.command}`, "success");
      await refreshLogs(true);
    }).catch((error) => showToast(error.message, "error"))
  );

  ui.sceneGroupBtn.addEventListener("click", () =>
    withBusy(ui.sceneGroupBtn, "Отправка...", async () => {
      // Вызов backend: api_scene_assign_group(ai, ag, slot, number)
      // Назначение группы AG0/AG1/AG2 для сценариев (Unit8)
      const adr = resolveAddressFields(ui.sceneAI, ui.sceneAG);
      const payload = await callApi(
        "api_scene_assign_group",
        adr.ai,
        adr.ag,
        Number(ui.sceneGroupSlot.value),
        Number(ui.sceneGroupNumber.value)
      );
      setRawResponse(payload.lines);
      showToast(`Отправлено: ${payload.command}`, "success");
      await refreshLogs(true);
    }).catch((error) => showToast(error.message, "error"))
  );

  ui.sendRawBtn.addEventListener("click", () =>
    withBusy(ui.sendRawBtn, "Отправка...", async () => {
      // Вызов backend: api_send_raw(command) - отправка произвольной команды
      // Поддерживает: TIME, GEONEZ, KEYS, MASK, COM, COMA, SHED
      const payload = await callApi("api_send_raw", ui.rawCommand.value.trim());
      setRawResponse(payload.lines);
      if (payload.schedule && payload.schedule.length) {
        setScheduleEntries(payload.schedule);
      }
      showToast(`Отправлено: ${payload.command}`, "success");
      await refreshLogs(true);
    }).catch((error) => showToast(error.message, "error"))
  );

  ui.readScheduleBtn.addEventListener("click", () =>
    withBusy(ui.readScheduleBtn, "Чтение...", async () => {
      // Вызов backend: api_read_schedule() - чтение всего расписания SHED из контроллера
      // Возвращает массив записей расписания и сырой ответ
      const payload = await callApi("api_read_schedule");
      setScheduleEntries(payload.entries || []);
      setRawResponse(payload.lines);
      showToast(`Строк расписания: ${payload.count}`, "success");
      await refreshLogs(true);
    }).catch((error) => showToast(error.message, "error"))
  );

  ui.scheduleWriteBtn.addEventListener("click", () =>
    withBusy(ui.scheduleWriteBtn, "Запись...", async () => {
      // Вызов backend: api_write_schedule_entry(payload) - запись одной строки SHED
      // payload содержит: index, active, days, time_type, sign, hours, minutes, target_mode, ai, ag, и т.д.
      const payload = await callApi("api_write_schedule_entry", collectSchedulePayload());
      setRawResponse(payload.lines);
      showToast(`Сохранено: ${payload.command}`, "success");

      // Обновление расписания после записи
      const refreshed = await callApi("api_read_schedule");
      setScheduleEntries(refreshed.entries || []);
      await refreshLogs(true);
    }).catch((error) => showToast(error.message, "error"))
  );

  ui.schedTimeType.addEventListener("change", () => {
    updateScheduleTimeModeUI();
    syncScheduleLegacyTimeFieldsFromUI();
  });

  ui.schedTargetMode.addEventListener("change", () => {
    updateScheduleTargetModeUI();
    syncScheduleActionFieldsFromUI();
  });

  [ui.schedBrightness, ui.schedScene, ui.schedCommandCode].forEach((node) => {
    node.addEventListener("input", () => {
      if (ui.schedTargetMode.value !== "ai") {
        return;
      }

      if (node === ui.schedBrightness) {
        setScheduleActionMode("brightness");
      } else if (node === ui.schedScene) {
        setScheduleActionMode("scene");
      } else {
        setScheduleActionMode("command");
      }
      syncScheduleActionFieldsFromUI();
    });
  });

  ui.refreshLogsBtn.addEventListener("click", () => {
    refreshLogs(false);
  });

  ui.scheduleFilter.addEventListener("change", () => {
    renderSchedule(scheduleState.entries);
  });
}

window.addEventListener("DOMContentLoaded", async () => {
  initTheme();
  initPages();
  initComfortControls();
  initLuminairePanel();
  initScheduleComfortControls();
  wireEvents();
  await bootstrap();

  setInterval(() => {
    refreshLogs(true);
  }, 1800);
});

window.addEventListener("beforeunload", () => {
  stopScenarioRepeat("Повтор выключен");
});
