/*
 * CLO26 – prompter som kursen föreslår.
 *
 * Varje prompt är data: fält, en mall (build), ett exempel, tips och var i
 * kursen den kommer ifrån. Sidan kurs.html?id=... ritar formuläret.
 * Testas med: node tests/test_kursprompter.js
 *
 * Grundhållning i alla prompter: AI är en juniorkollega, inte facit.
 * Standardvalet är därför ledtrådar och förklaringar – inte färdiga lösningar.
 */

const COURSE_REPO = "https://github.com/marcusjobb/YRGO-CLO26-HT26Kursmaterial/blob/main/";

const LEVEL_DEFAULT = "nybörjare i C# (termin 1)";

/** Lägger kod i ett kodblock med rätt språk. */
function codeBlock(code, lang = "") {
  return "```" + lang + "\n" + code.trim() + "\n```";
}

const HINT_MODES = [
  { value: "ledtradar", label: "Ledtrådar – inte lösningen (rekommenderas)" },
  { value: "forklaring", label: "Förklaring av problemet – men skriv inte om min kod" },
  { value: "losning", label: "En lösning – med varje ändring förklarad" }
];

const COURSE_PROMPTS = [
  // ---------------------------------------------------------------- PLANERA
  {
    id: "forklara-uppgift", group: "planera",
    title: "Förklara en uppgift",
    tagline: "Förstår du inte en uppgift i AI:ns lista? Be om en förklaring innan den blir ett kort.",
    source: { name: "Kurs 3 · AI-planering och Trello, steg 3: Granska", path: "kurs-03-fordjupad-oop/03_refactoring_clean_code_kanban/exercises/ai_planering_trello.md" },
    tips: [
      "Varje kort måste du kunna förklara med egna ord. Den här prompten hjälper dig dit – den ersätter inte din egen förklaring.",
      "Läs svaret och försök sedan förklara uppgiften för en klasskamrat. Går det inte: fråga igen eller ta bort uppgiften."
    ],
    fields: [
      { id: "project", type: "textarea", rows: 3, label: "Projektet i tre rader (valfritt)", hint: "Vad appen gör, vad som är klart när, vilka delar som finns." },
      { id: "task", type: "textarea", rows: 2, required: true, label: "Uppgiften du inte förstår", placeholder: "t.ex. Implementera BookingRepository med LoadToday()" },
      { id: "level", type: "text", label: "Din nivå", default: LEVEL_DEFAULT },
      { id: "maxTime", type: "select", label: "Hur stor får en uppgift vara?", default: "30 minuter",
        options: [{ value: "15 minuter", label: "15 minuter" }, { value: "30 minuter", label: "30 minuter" }, { value: "1 timme", label: "1 timme" }] }
    ],
    build: (v) => lines(
      "Jag planerar ett projekt och har fått uppgiften nedan i en lista från en AI. Jag måste kunna förklara den med egna ord innan jag lägger in den på vår Kanban-tavla.",
      "",
      v.project ? `Projektet:\n${v.project}\n` : null,
      `Uppgiften: ${v.task}`,
      "",
      `Förklara för någon som är ${v.level || LEVEL_DEFAULT}:`,
      "1. Vad ska göras, konkret?",
      "2. Varför behövs uppgiften i projektet?",
      "3. Vad måste vara klart innan, och vad bygger på den här uppgiften?",
      "4. Hur vet jag att den är klar?",
      "",
      `Om uppgiften är större än ${v.maxTime}, föreslå hur den kan delas upp. Skriv inte koden åt mig.`
    ),
    example: {
      project: "En konsolapp där Hjulets kunder bokar tid för däckbyte.\nKlart när man kan boka, se dagens bokningar och skriva ut en faktura.\nDelar: Booking, PriceCalculator, BookingRepository, InvoicePrinter, ConsoleMenu.",
      task: "Implementera BookingRepository med Save() och LoadToday()",
      level: LEVEL_DEFAULT, maxTime: "30 minuter"
    }
  },
  {
    id: "kanban-kort", group: "planera",
    title: "Gör kort av listan",
    tagline: "Gör om din granskade uppgiftslista till kort för Trello eller GitHub Issues.",
    source: { name: "Kurs 3 · AI-planering och Trello, steg 4–5: Skapa kort", path: "kurs-03-fordjupad-oop/03_refactoring_clean_code_kanban/exercises/ai_planering_trello.md" },
    tips: [
      "Klistra bara in en lista du redan har granskat. AI:n ska formatera, inte hitta på nya uppgifter.",
      "Trello: klistrar du in flera rader i ”Lägg till ett kort” frågar Trello om den ska skapa ett kort per rad.",
      "GitHub: kör skriptet först när du har läst det. Kontrollera att `gh auth status` säger att du är inloggad.",
      "Alla kort börjar i Backlog. Begränsa Working till två eller tre kort åt gången."
    ],
    fields: [
      { id: "tasks", type: "textarea", rows: 8, required: true, label: "Din granskade uppgiftslista", hint: "En uppgift per rad, gärna med tid." },
      { id: "target", type: "select", label: "Var ska korten hamna?", default: "trello",
        options: [
          { value: "trello", label: "Trello – rader att klistra in" },
          { value: "github", label: "GitHub Issues – PowerShell-skript med gh" }
        ] },
      { id: "repo", type: "text", label: "GitHub-repo (bara för GitHub)", placeholder: "t.ex. mittkonto/hjulet-bokning" },
      { id: "project", type: "text", label: "GitHub-projekt/tavla (valfritt)", placeholder: "t.ex. Hjulet – planering" },
      { id: "details", type: "checkbox", default: true, label: "Lägg till en kort beskrivning och ”Klart när” per kort" }
    ],
    build: (v) => {
      const keep = "Behåll min ordning och mina formuleringar. Lägg inte till eller ta bort uppgifter – rätta bara stavfel. Om en uppgift verkar för stor, säg det efter listan i stället för att ändra den.";
      const details = v.details ? "Varje kort ska ha en beskrivning på en eller två meningar och en rad ”Klart när: …” som går att kontrollera." : null;
      if (v.target === "github") {
        return lines(
          `Gör om uppgiftslistan nedan till GitHub Issues i repot ${v.repo || "ägare/repo"}.`,
          "",
          "Uppgifter:",
          v.tasks,
          "",
          "Skriv ett PowerShell-skript som:",
          "1. Skapar etiketten backlog om den inte finns: gh label create backlog --force",
          `2. Skapar en issue per uppgift med gh issue create, titeln ”NN. Titel” och etiketten backlog${v.project ? `, och lägger den i projektet ”${v.project}” med --project` : ""}.`,
          "Använd enkla citattecken runt texter i PowerShell.",
          "",
          details,
          keep,
          "Förklara kort vad skriptet gör innan själva koden, så att jag kan läsa det innan jag kör det."
        );
      }
      return lines(
        "Gör om uppgiftslistan nedan till kort för vår Kanban-tavla i Trello. Tavlan har kolumnerna Backlog, Working, Test och Done, och alla kort börjar i Backlog.",
        "",
        "Uppgifter:",
        v.tasks,
        "",
        "Skriv först korttitlarna i ett kodblock: en rad per kort, utan punkter och utan tomma rader, i formatet ”NN. Titel (ca X min)”. Då kan jag klistra in alla rader på en gång i Trello.",
        details ? "\nSkriv sedan, under listan, beskrivningen och ”Klart när” för varje kort, så att jag kan klistra in dem i korten." : null,
        details,
        keep
      );
    },
    example: {
      tasks: "Skapa repo och konsolprojekt – 15 min\nSkapa klassen Booking – 20 min\nSkapa PriceCalculator med moms – 30 min\nTest: PriceCalculator räknar moms rätt – 20 min\nSpara bokningar i fil med BookingRepository – 30 min\nVisa dagens bokningar sorterade på tid – 30 min",
      target: "trello", repo: "", project: "", details: true
    }
  },
  {
    id: "dela-upp-kort", group: "planera",
    title: "Dela upp ett för stort kort",
    tagline: "Kortet har legat i Working för länge? Dela upp det i steg du kan börja på direkt.",
    source: { name: "Kurs 3 · AI-planering och Trello, steg 6: Reflektera", path: "kurs-03-fordjupad-oop/03_refactoring_clean_code_kanban/exercises/ai_planering_trello.md" },
    tips: [
      "Ett tecken på för stort kort: det innehåller ordet ”och”, eller du vet inte var du ska börja.",
      "Flytta kort, skriv inte om dem: ersätt det stora kortet med de nya, små korten i stället för att ändra det."
    ],
    fields: [
      { id: "card", type: "textarea", rows: 2, required: true, label: "Kortet som är för stort" },
      { id: "why", type: "textarea", rows: 2, label: "Varför känns det för stort? (valfritt)", placeholder: "t.ex. Jag vet inte var jag ska börja." },
      { id: "maxTime", type: "select", label: "Hur stort får ett nytt kort vara?", default: "30 minuter",
        options: [{ value: "15 minuter", label: "15 minuter" }, { value: "30 minuter", label: "30 minuter" }, { value: "1 timme", label: "1 timme" }] },
      { id: "level", type: "text", label: "Din nivå", default: LEVEL_DEFAULT }
    ],
    build: (v) => lines(
      `Det här kortet på vår Kanban-tavla är för stort: ”${v.card}”`,
      v.why ? `Varför: ${v.why}` : null,
      "",
      `Dela upp det i mindre kort som tar högst ${v.maxTime} vardera. Varje nytt kort ska:`,
      "- vara ett konkret steg jag kan börja på direkt",
      "- gå att testa eller visa när det är klart",
      "- ha en rad ”Klart när: …”",
      "",
      "Lista korten i den ordning de ska göras.",
      `Jag är ${v.level || LEVEL_DEFAULT}. Om ett steg kräver något jag troligen inte kan än, säg det. Skriv inte koden åt mig.`
    ),
    example: {
      card: "Spara och läsa bokningar i fil",
      why: "Jag vet inte var jag ska börja, och det har legat i Working i två dagar.",
      maxTime: "30 minuter", level: LEVEL_DEFAULT
    }
  },

  // ---------------------------------------------------------------- KODA
  {
    id: "fastnat", group: "koda",
    title: "Jag har fastnat",
    tagline: "15-minutersregeln: fråga klassen, sedan AI, sedan läraren. Den här prompten är steg två.",
    source: { name: "Kurs 1–3 · 15-minutersregeln", path: "kurs-01-grundlaggande-oop/01_git_och_verktyg/notes/github_actions.md" },
    tips: [
      "Fastnar du i mer än 15 minuter: fråga klassen, sedan AI, sedan läraren. I den ordningen.",
      "Ledtrådar lär dig mer än en färdig lösning – och du ska kunna förklara koden du lämnar in.",
      "Klistra aldrig in lösenord, API-nycklar eller personuppgifter i en AI-chatt.",
      "Ta med felmeddelandet exakt som det står. Det är ofta den viktigaste ledtråden."
    ],
    fields: [
      { id: "goal", type: "textarea", rows: 2, required: true, label: "Vad försöker du göra?" },
      { id: "tried", type: "textarea", rows: 2, label: "Vad har du provat?" },
      { id: "error", type: "textarea", rows: 3, label: "Felmeddelande (valfritt)", hint: "Klistra in exakt som det står." },
      { id: "code", type: "textarea", rows: 8, label: "Koden (valfritt)", hint: "Bara den del som har med problemet att göra." },
      { id: "level", type: "text", label: "Din nivå", default: LEVEL_DEFAULT },
      { id: "mode", type: "select", label: "Vilken hjälp vill du ha?", default: "ledtradar", options: HINT_MODES }
    ],
    build: (v) => {
      const help = {
        ledtradar: "Ge mig ledtrådar, inte lösningen. Börja med den minsta ledtråden – jag frågar om jag behöver fler. Säg var i koden jag ska titta och vad jag ska kontrollera.",
        forklaring: "Förklara vad felet betyder och varför det uppstår. Skriv inte om min kod – jag vill rätta den själv.",
        losning: "Visa en lösning och förklara varje ändring rad för rad, så att jag kan förklara den själv efteråt."
      }[v.mode];
      return lines(
        `Jag har fastnat och vill förstå problemet. Jag är ${v.level || LEVEL_DEFAULT}.`,
        "",
        `Det här försöker jag göra: ${v.goal}`,
        v.tried ? `Det här har jag provat: ${v.tried}` : null,
        v.error ? "\nFelmeddelande:\n" + codeBlock(v.error) : null,
        v.code ? "\nKoden:\n" + codeBlock(v.code, "csharp") : null,
        "",
        help,
        "Om du behöver se mer av koden för att svara, fråga efter den i stället för att gissa."
      );
    },
    example: {
      goal: "Läsa in bokningar från en fil när programmet startar.",
      tried: "Jag har kontrollerat att filen finns i projektmappen.",
      error: "System.IO.FileNotFoundException: Could not find file 'C:\\kod\\Hjulet\\bin\\Debug\\net10.0\\bokningar.txt'.",
      code: "var lines = File.ReadAllLines(\"bokningar.txt\");",
      level: LEVEL_DEFAULT, mode: "ledtradar"
    }
  },
  {
    id: "forklara-kod", group: "koda",
    title: "Förklara kod",
    tagline: "Förstå kod du inte skrivit själv – eller kod en AI skrivit åt dig.",
    source: { name: "Kurs 3 · OpenCode-installationen", path: "kurs-03-fordjupad-oop/00_kursintro/notes/opencode_installation.md" },
    tips: [
      "Kontrollera alltid att förklaringen stämmer med koden. AI:n kan ha fel.",
      "I OpenCode eller Claude Code kan du skriva filnamnet i stället för att klistra in koden: ”Vad gör filen Program.cs?”"
    ],
    fields: [
      { id: "file", type: "text", label: "Filnamn (valfritt)", placeholder: "t.ex. Program.cs" },
      { id: "code", type: "textarea", rows: 10, label: "Koden", hint: "Lämna tom om AI:n kan läsa filen själv (OpenCode, Claude Code)." },
      { id: "question", type: "textarea", rows: 2, label: "Vad vill du särskilt förstå? (valfritt)" },
      { id: "level", type: "text", label: "Din nivå", default: LEVEL_DEFAULT },
      { id: "smells", type: "checkbox", default: true, label: "Peka ut code smells – men rätta dem inte" }
    ],
    build: (v) => {
      const what = v.file ? `filen ${v.file}` : "den här koden";
      return lines(
        `Förklara vad ${what} gör, för någon som är ${v.level || LEVEL_DEFAULT}.`,
        v.code ? "\n" + codeBlock(v.code, "csharp") + "\n" : null,
        v.question ? `Jag vill särskilt förstå: ${v.question}\n` : null,
        "Gå igenom koden uppifrån och ner: vad gör varje del, och varför finns den?",
        `Avsluta med en mening om vad ${what} ansvarar för.`,
        v.smells ? "Om något ser ut som ett fel eller en code smell, nämn det kort och förklara varför – men skriv inte om koden." : null
      );
    },
    example: {
      file: "Program.cs",
      code: "var menu = new ConsoleMenu(new BookingRepository(\"bokningar.txt\"));\nmenu.Show();",
      question: "Varför skickas BookingRepository in i ConsoleMenu?",
      level: LEVEL_DEFAULT, smells: true
    }
  },
  {
    id: "granska-uppdelning", group: "koda",
    title: "Granska min uppdelning",
    tagline: "Har dina klasser ett ansvar var? Låt AI:n ställa frågorna – svaren ger du själv.",
    source: { name: "Kurs 3 · Projekt: dela upp bokningsappen", path: "kurs-03-fordjupad-oop/03_refactoring_clean_code_kanban/exercises/projekt_uppdelning.md" },
    tips: [
      "Gör din egen uppdelning först. Granskning av något du inte gjort lär dig ingenting.",
      "Står det ”och” i en ansvarsmening har du troligen två klasser.",
      "Du ska kunna motivera din uppdelning – AI:ns frågor är till för att du ska hitta svagheterna själv."
    ],
    fields: [
      { id: "project", type: "textarea", rows: 3, label: "Projektbeskrivning", hint: "Vad appen ska kunna." },
      { id: "design", type: "textarea", rows: 10, required: true, label: "Din uppdelning", hint: "Klasser, ansvar och metoder – gärna enligt mallen i övningen." },
      { id: "changes", type: "textarea", rows: 3, label: "Förändringar att testa uppdelningen mot", hint: "En per rad.",
        default: "Momsen ändras\nVi byter från fil till databas\nVi byter från konsol till webb" },
      { id: "mode", type: "select", label: "Vilken hjälp vill du ha?", default: "ledtradar",
        options: [
          { value: "ledtradar", label: "Frågor och ledtrådar – inte en ny uppdelning (rekommenderas)" },
          { value: "forslag", label: "Konkreta förslag på förbättringar, med motivering" }
        ] }
    ],
    build: (v) => lines(
      "Jag har delat upp ett projekt i klasser och metoder, och vill granska uppdelningen mot SRP (Single Responsibility Principle) och SoC (Separation of Concerns).",
      v.project ? `\nProjektet:\n${v.project}` : null,
      "",
      "Min uppdelning:",
      v.design,
      "",
      "Granska så här:",
      "1. Har varje klass ett enda ansvar? Peka ut klasser vars ansvar egentligen är två saker.",
      "2. Vilka klasser känner till konsolen, filer eller databasen? Är det bara en klass för varje sak?",
      v.changes ? "3. Gå igenom förändringarna nedan. Vilka klasser behöver ändras för var och en, och vilka slipper?\n" + bullets(v.changes) : null,
      "",
      v.mode === "forslag"
        ? "Ge konkreta förslag på förbättringar och motivera varje förslag med SRP eller SoC."
        : "Ge mig frågor och ledtrådar, inte en färdig uppdelning. Jag ska kunna motivera min lösning själv."
    ),
    example: {
      project: "Hjulets bokningsapp i konsolen: ta emot bokningar, lista dagens bokningar sorterat på tid, räkna ut pris med moms, spara i fil och skriva ut faktura.",
      design: "### Booking\n**Ansvar:** Håller uppgifterna om en bokning och räknar ut priset.\n\n### BookingManager\n**Ansvar:** Sparar bokningar i fil och visar menyn.\n\n### InvoicePrinter\n**Ansvar:** Skriver ut en faktura.",
      changes: "Momsen ändras\nVi byter från fil till databas\nVi byter från konsol till webb",
      mode: "ledtradar"
    }
  },
  {
    id: "uml", group: "koda",
    title: "UML-dokumentation",
    tagline: "Kursens UML-prompt: låt AI:n läsa ditt projekt och skriva UML.md med Mermaid-diagram.",
    source: { name: "Kurs 3 · UML-prompten", path: "kurs-03-fordjupad-oop/02_ef_mongodb_designmonster/notes/uml_prompt.md" },
    tips: [
      "Ge AI:n tillgång till koden, till exempel genom att bifoga projektmappen, och klistra in prompten.",
      "Kontrollera resultatet mot checklistan i kursens anteckningar. Du ska kunna förklara varje diagram.",
      "Rendera filen (t.ex. i GitHub eller VS Code) och kontrollera att alla diagram visas utan fel."
    ],
    fields: [
      { id: "about", type: "text", label: "Vad är projektet? (valfritt)", placeholder: "t.ex. Hjulets bokningsapp i C# med SQLite" },
      { id: "classDiagram", type: "checkbox", default: true, label: "Klassdiagram" },
      { id: "deps", type: "checkbox", default: true, label: "Beroenden & paket" },
      { id: "flow", type: "checkbox", default: true, label: "Programflöde" },
      { id: "sequence", type: "checkbox", default: true, label: "Sekvensdiagram" },
      { id: "contracts", type: "checkbox", default: true, label: "Implementationer av kontrakt (bara om det finns interface/basklasser)" },
      { id: "notes", type: "checkbox", default: true, label: "Not-ruta med iakttagelser" }
    ],
    build: (v) => {
      const sections = [
        v.classDiagram && "**Klassdiagram** (`classDiagram`): alla typer fullt ut — medlemmar med synlighet, `«abstract»`/`«interface»`-stereotyper, arvspilar med etiketten `ärver`, aggregation (`o--` med multiplicitet), beroenden (`..>`) inklusive entry point-klassen som använder resten.",
        v.deps && "**Beroenden & paket** (`flowchart LR`): entry point → klasser → lagring/paket. Streckade pilar (`-.->`) för utkommenterade/valfria beroenden. Databas-form `[( )]` för databaser, filform för filer.",
        v.flow && "**Programflöde** (`flowchart TD`): huvudflödet från start till slut med beslutsnoder, menyval och terminaler `([Start])`/`([Slut])`.",
        v.sequence && "**Sekvensdiagram** (`sequenceDiagram`): ett centralt use case end-to-end — deltagare, meddelanden och svar, inklusive lagring.",
        v.contracts && "**Implementationer av kontrakt** (`flowchart TB`) — ENDAST om det finns basklasser/interface med flera implementationer: visa kontraktet överst och varje implementation med sina operationer.",
        v.notes && "**Not-ruta** (blockquote): iakttagelser om arkitekturen — t.ex. metoder som finns i en implementation men saknas i kontraktet, oavslutad kod, platshållare som kastar `NotImplementedException`."
      ].filter(Boolean);

      return lines(
        "# Prompt: Generera UML-dokumentation för ditt projekt",
        "",
        "Analysera det projekt jag har klistrat in / bifogat / gett dig tillgång till, och skapa en fil `UML.md` med fullständig UML-dokumentation i Mermaid.",
        v.about ? `\nProjektet: ${v.about}` : null,
        "",
        "## Steg 1 — Kartlägg koden",
        "",
        "- Läs ALLA källkodsfiler (hoppa över `bin/`, `obj/`, `node_modules/` och annan build-output)",
        "- Identifiera alla typer (klasser, interface, record, struct) med:",
        "  - fält/properties och metoder, med synlighetsprefix: `+` publik, `#` skyddad, `-` privat",
        "  - konstruktorer och om de gör något intressant (t.ex. skapar tabell, öppnar anslutning)",
        "- Notera relationer:",
        "  - arv och interface-implementeringar",
        "  - komposition/aggregation (t.ex. `List<Katt>`-fält → `o--` med multiplicitet)",
        "  - beroenden mellan klasser (vem skapar/använder vem)",
        "  - startpunkt/entry point och vad den använder",
        "  - externa paket (NuGet, npm, ...) och var data lagras (filer, databas)",
        "- Följ kodflödet från entry point för att förstå körningsordningen",
        "",
        "## Steg 2 — Skriv UML.md med dessa sektioner",
        "",
        sections.map((s, i) => `${i + 1}. ${s}`).join("\n"),
        "",
        "Mellan diagrammen: kort förklarande text på svenska (2–5 punkter per diagram).",
        v.classDiagram ? "Under klassdiagrammet en **Läsning:**-lista med en rad per klass." : null,
        "",
        "## Stilregler för Mermaid",
        "",
        "- Körbar syntax ovan allt:",
        "  - citattecken runt etiketter som innehåller specialtecken eller radbrytningar",
        "  - `<br/>` för radbrytning i noder (aldrig `\\n`)",
        "  - `\\\\` för backslash i etiketter",
        "  - undvik `(`, `)`, `[`, `]`, `{`, `}` i ociterad text",
        "- Generiska typer i `classDiagram` skrivs med tilde: `List~Katt~`",
        "- Abstrakta medlemmar markeras med `*` efter signaturen",
        "- Granska varje diagram mot Mermaid-syntaxen innan resultatet lämnas — alla diagram ska rendera felfritt",
        "",
        "## Ton och språk",
        "",
        "- Svenska, korta pedagogiska förklaringar — läsaren ska förstå systemet utan att öppna koden",
        "- Börja dokumentet med en kort intro (typ av app, mål-framework/SDK, syfte)",
        v.notes ? "- Avsluta med Not-observationer som en kollega skulle göra vid genomgång" : null,
        "",
        "## Leverans",
        "",
        "- Spara resultatet som `UML.md` i projektets rot — kan du inte skriva filer, visa hela innehållet i ett enda kodblock som går att kopiera"
      );
    },
    example: { about: "Hjulets bokningsapp i C# med en textfil som lagring", classDiagram: true, deps: true, flow: true, sequence: true, contracts: true, notes: true }
  }
];

// Gruppernas rubriker och ordning på startsidan.
const COURSE_GROUPS = [
  { id: "planera", title: "Planera ett projekt", text: "Dagens Kanban-lektion: beskriv, dela upp, granska och gör kort." },
  { id: "koda", title: "När du kodar", text: "Fastnat, ny kod eller dags att granska? AI som juniorkollega – inte facit." }
];

function findCoursePrompt(id) {
  return COURSE_PROMPTS.find((p) => p.id === id) ?? null;
}

if (typeof module !== "undefined") {
  module.exports = { COURSE_PROMPTS, COURSE_GROUPS, COURSE_REPO, findCoursePrompt };
}
