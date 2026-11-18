// Testar CLO26-prompterna utan webbläsare. Kör: node tests-web/test_kursprompter.js
const fs = require("fs"), path = require("path"), vm = require("vm");
const ctx = { module: { exports: {} } };
vm.createContext(ctx);
for (const f of ["generator.js", "kursprompter.js"]) {
  vm.runInContext(fs.readFileSync(path.join(__dirname, "../docs/assets", f), "utf8"), ctx);
}
const K = ctx.module.exports;
let fail = 0;
const check = (ok, msg) => { if (!ok) { fail++; console.log("  FEL: " + msg); } };
const tidy = (s) => s.replace(/\n{3,}/g, "\n\n").trim();

const ids = K.COURSE_PROMPTS.map((p) => p.id);
check(new Set(ids).size === ids.length, "id:n är inte unika");

for (const p of K.COURSE_PROMPTS) {
  const defaults = Object.fromEntries(p.fields.map((f) => [f.id, f.default ?? (f.type === "checkbox" ? false : "")]));
  const full = tidy(p.build({ ...defaults, ...p.example }));
  const minimal = { ...defaults };
  p.fields.filter((f) => f.required).forEach((f) => (minimal[f.id] = "X"));
  const small = tidy(p.build(minimal));
  for (const [name, out] of [["exempel", full], ["minimal", small]]) {
    for (const bad of ["undefined", "null", "[object"]) check(!out.includes(bad), `${p.id}/${name}: innehåller "${bad}"`);
    check(out.length > 60, `${p.id}/${name}: misstänkt kort`);
  }
  for (const f of p.fields.filter((f) => f.required)) check(p.example[f.id], `${p.id}: exemplet saknar ${f.id}`);
  for (const key of Object.keys(p.example)) check(p.fields.some((f) => f.id === key), `${p.id}: okänt exempelfält ${key}`);
  check(p.source?.path && p.tips?.length, `${p.id}: saknar källa eller tips`);
  check(K.COURSE_GROUPS.some((g) => g.id === p.group), `${p.id}: okänd grupp ${p.group}`);
}

// Kursens linje: ledtrådar som standard
const fastnat = K.findCoursePrompt("fastnat");
check(fastnat.fields.find((f) => f.id === "mode").default === "ledtradar", "fastnat: standard ska vara ledtrådar");
check(fastnat.build(fastnat.example).includes("Ge mig ledtrådar, inte lösningen"), "fastnat: ledtrådstexten saknas");
check(K.findCoursePrompt("granska-uppdelning").build(K.findCoursePrompt("granska-uppdelning").example).includes("inte en färdig uppdelning"), "granska: ska be om frågor, inte uppdelning");
const kort = K.findCoursePrompt("kanban-kort");
check(kort.build({ ...kort.example, target: "github", repo: "a/b" }).includes("gh issue create"), "kort/github: saknar gh issue create");
check(kort.build(kort.example).includes("Backlog, Working, Test och Done"), "kort/trello: kolumnerna saknas");
const uml = K.findCoursePrompt("uml");
const umlAll = uml.build(uml.example);
check(umlAll.includes("aldrig `\\n`") && umlAll.includes("`\\\\` för backslash"), "uml: escape-raderna stämmer inte med originalet");
check((umlAll.match(/^\d\. \*\*/gm) || []).length === 6, "uml: alla sex sektioner ska finnas");
check((uml.build({ ...uml.example, sequence: false, contracts: false }).match(/^\d\. \*\*/gm) || []).length === 4, "uml: avbockade sektioner ska försvinna");

console.log(`Prompter: ${K.COURSE_PROMPTS.length}`);
console.log(fail ? `${fail} FEL` : "ALLA TESTER OK");
process.exit(fail ? 1 : 0);
