/*
 * Gemensam motor för alla promptgeneratorer.
 *
 * Varje sida anropar createGenerator({ fields, build, example }):
 *   fields  – lista med fält som ska visas i formuläret
 *   build   – funktion som får alla värden och returnerar den färdiga prompten
 *   example – (valfritt) värden som fylls i av knappen "Fyll i exempel"
 *   storageKey – (valfritt) egen nyckel för sparade värden, när flera generatorer delar samma sida
 *   texts   – (valfritt) egna texter för statusmeddelanden, t.ex. på göteborgska
 *
 * Fälttyper: "text", "textarea", "select" (med options) och "checkbox".
 */
function createGenerator(config) {
  const form = document.getElementById("form");
  const fieldsBox = document.getElementById("fields");
  const result = document.getElementById("result");
  const output = document.getElementById("output");
  const status = document.getElementById("status");

  // Varje sida sparar sina egna värden i webbläsaren, så att inget försvinner vid omladdning.
  const storageKey = "promptplanner:" + (config.storageKey ?? location.pathname);

  const texts = {
    missing: "Fyll i: ",
    copied: "✓ Kopierad! Klistra in den i din AI.",
    copyFailed: "Kunde inte kopiera automatiskt – texten är markerad, tryck Ctrl+C.",
    ...config.texts
  };

  // ---------- Rita formuläret ----------
  const saved = loadSaved();
  for (const field of config.fields) {
    fieldsBox.appendChild(renderField(field, saved[field.id]));
  }

  function renderField(field, savedValue) {
    const wrap = document.createElement("div");
    wrap.className = "field";
    const value = savedValue ?? field.default ?? (field.type === "checkbox" ? false : "");

    if (field.type === "checkbox") {
      wrap.innerHTML = `<label class="check"><input type="checkbox" id="${field.id}"> <span></span></label>`;
      wrap.querySelector("span").textContent = field.label;
      wrap.querySelector("input").checked = Boolean(value);
      return wrap;
    }

    const label = document.createElement("label");
    label.htmlFor = field.id;
    label.textContent = field.label;
    if (field.required) label.insertAdjacentHTML("beforeend", ' <span class="req" aria-hidden="true">*</span>');
    wrap.appendChild(label);

    if (field.hint) {
      const hint = document.createElement("span");
      hint.className = "hint";
      hint.id = field.id + "-hint";
      hint.textContent = field.hint;
      wrap.appendChild(hint);
    }

    let input;
    if (field.type === "select") {
      input = document.createElement("select");
      for (const option of field.options) {
        input.add(new Option(option.label, option.value));
      }
    } else if (field.type === "textarea") {
      input = document.createElement("textarea");
      input.rows = field.rows ?? 3;
    } else {
      input = document.createElement("input");
      input.type = "text";
    }

    input.id = field.id;
    if (field.placeholder) input.placeholder = field.placeholder;
    if (field.hint) input.setAttribute("aria-describedby", field.id + "-hint");
    if (field.required) input.required = true;
    input.value = value;
    wrap.appendChild(input);
    return wrap;
  }

  // ---------- Läsa värden ----------
  function readValues() {
    const values = {};
    for (const field of config.fields) {
      const el = document.getElementById(field.id);
      values[field.id] = field.type === "checkbox" ? el.checked : el.value.trim();
    }
    return values;
  }

  function fillValues(values) {
    for (const field of config.fields) {
      const el = document.getElementById(field.id);
      const value = values[field.id] ?? field.default ?? (field.type === "checkbox" ? false : "");
      if (field.type === "checkbox") el.checked = Boolean(value);
      else el.value = value;
      el.classList.remove("invalid");
    }
  }

  // ---------- Generera ----------
  form.addEventListener("submit", async (event) => {
    event.preventDefault(); // formuläret ska inte skickas någonstans

    const values = readValues();
    const missing = config.fields.filter((f) => f.required && !values[f.id]);
    for (const field of config.fields) {
      document.getElementById(field.id).classList.toggle("invalid", missing.includes(field));
    }
    if (missing.length > 0) {
      result.hidden = false;
      output.value = "";
      setStatus(texts.missing + missing.map((f) => f.label).join(", "), "error");
      document.getElementById(missing[0].id).focus();
      return;
    }

    save(values);
    output.value = tidy(config.build(values));
    result.hidden = false;
    autoResize();
    result.scrollIntoView({ behavior: "smooth", block: "start" });
    await copyPrompt();
  });

  document.getElementById("copyAgain").addEventListener("click", copyPrompt);

  document.getElementById("reset").addEventListener("click", () => {
    fillValues({});
    save({});
    result.hidden = true;
  });

  const exampleButton = document.getElementById("example");
  if (exampleButton && config.example) {
    exampleButton.addEventListener("click", () => fillValues(config.example));
  } else if (exampleButton) {
    exampleButton.hidden = true;
  }

  // ---------- Hjälpfunktioner ----------
  async function copyPrompt() {
    try {
      await navigator.clipboard.writeText(output.value);
      setStatus(texts.copied, "ok");
    } catch {
      // Reserv om webbläsaren inte tillåter urklipp: markera texten så att man kan trycka Ctrl+C.
      output.focus();
      output.select();
      setStatus(texts.copyFailed, "error");
    }
  }

  function setStatus(text, kind) {
    status.textContent = text;
    status.className = kind;
  }

  function autoResize() {
    output.style.height = "auto";
    output.style.height = output.scrollHeight + 4 + "px";
  }

  /** Tar bort tomma rader i följd och mellanrum i början/slutet. */
  function tidy(text) {
    return text.replace(/\n{3,}/g, "\n\n").trim();
  }

  function loadSaved() {
    try {
      return JSON.parse(localStorage.getItem(storageKey)) ?? {};
    } catch {
      return {};
    }
  }

  function save(values) {
    try {
      localStorage.setItem(storageKey, JSON.stringify(values));
    } catch {
      /* t.ex. privat fönster – då sparar vi helt enkelt inte */
    }
  }
}

/* ---------- Små byggklossar som mallarna kan använda ---------- */

/** Gör om text med en sak per rad till en punktlista. */
function bullets(text) {
  return text
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => (line.startsWith("-") ? line : "- " + line))
    .join("\n");
}

/** "- **Rubrik:** värde" – eller ingenting om värdet är tomt. */
function item(title, value) {
  return value ? `- **${title}:** ${value}` : null;
}

/** Ett block med rubrik och innehåll – eller ingenting om innehållet är tomt. */
function block(title, content) {
  return content ? `${title}\n${content}\n` : null;
}

/** Slår ihop rader och hoppar över de som är null. */
function lines(...parts) {
  return parts.filter((part) => part !== null && part !== undefined && part !== false).join("\n");
}
