# Mall-prompt: planera ett projekt i små tasks

## Innan du börjar: koppla AI:n till Trello eller GitHub

För att AI:n ska kunna **skapa korten åt dig** måste den ha behörighet till din board eller ditt repo. Hur du gör det beror på vilken sorts AI du använder.

### A. AI-agent på din egen dator (Claude Code, Copilot agent, Antigravity m.fl.)
Agenten kör kommandon och anropar API:er direkt, så den behöver nycklar.

**Trello: API-nyckel + token**
1. Gå till https://trello.com/power-ups/admin → **New** och skapa en Power-Up/app (vilket namn som helst).
2. Öppna appen → **API key** och kopiera nyckeln.
3. Klicka på den blå länken **Token** i texten till höger om nyckeln → **Allow** och kopiera token (börjar med `ATTA…`).
   - OBS: **Secret** behövs inte. Den används bara för OAuth.
4. Lägg nyckel och token i en `secrets.json` som är **gitignorerad**:
   ```json
   { "ApiKey": "...", "Token": "...", "BoardName": "namnet på boarden" }
   ```
5. Berätta för agenten var filen ligger. Klistra helst **inte** in nycklarna i chatten.

**GitHub (Issues/Projects): GitHub CLI**
```powershell
winget install GitHub.cli
gh auth login
gh auth status    # kontrollera att du är inloggad
```
Agenten kan sedan skapa issues med `gh issue create`, så du behöver ingen token i någon fil.

### B. Webb-AI (claude.ai, ChatGPT m.fl.)
En webb-AI kan inte köra kommandon på din dator. Den måste i stället **kopplas** till tjänsten:
- Leta under inställningarna efter **Connectors / Integrationer / Appar** (namnet skiljer sig mellan verktyg) och koppla Trello eller GitHub. Du loggar in hos tjänsten och godkänner åtkomsten.
- Saknas en koppling till din tjänst: be AI:n leverera korten som text (markdown, CSV eller JSON). Sedan klistrar du in dem själv eller importerar dem med ett skript, t.ex. `tools/seed_board.py` i det här repot.

### Efteråt
- Ta bort token eller koppla bort integrationen när planeringen är klar, om den inte ska användas mer.
- Har en token synts i en chatt eller hamnat i git: **generera en ny**.

---

## Själva prompten

Kopiera allt under linjen, fyll i `[HAKPARENTESERNA]` och klistra in till Claude/ChatGPT/annan AI.

---

Jag vill planera ett programmeringsprojekt som ska delas upp i små tasks (t.ex. Trello-kort).

## Projektet
- **Vad ska byggas:** [t.ex. ett enkelt konsolspel i C# där man springer i en labyrint och jagas av monster, Pac-Man-känsla, ingen grafik, inga vapen]
- **Språk/teknik:** [t.ex. C#, .NET, xUnit, Git/GitHub]
- **Vilka som ska göra det:** [t.ex. studenter termin 1 som kan variabler, loopar, metoder och enkla klasser]
- **Ungefärlig tid:** [t.ex. 2 veckor, grupper om 3]
- **Måste finnas / får inte finnas:** [t.ex. tester ska finnas, inga externa paket]
- **Git flow:** main, dev, feature branches och pull requests (ska uppmuntras)
- **Var korten ska hamna:** [Trello-boarden "NAMN" via token i `secrets.json` / GitHub Issues i repot "ägare/repo" via `gh` / kopplad connector / ingen koppling: ge mig bara text]
- **databas:** [Ja/Nej - om Ja säg vilken]
- **Designpatterns:** [factory? Observer? Inget?] 

## Hur tasks ska delas upp
- Varje task ska vara **ett litet, överkomligt steg** på 15–60 minuter: skapa repo, skapa en klass, skriva en metod, skriva ett test.
- Börja med setup (repo, .gitignore, projekt, testprojekt, backlog).
- Bygg sedan i **vertikala slices**, så att spelet/programmet kan köras och visa något nytt efter varje grupp av tasks.
- Lägg ett **test-kort** direkt efter den logik det testar, inte samlat i slutet.
- Lägg det som är "kul men inte nödvändigt" sist i en egen grupp (finputs).
- Numrera korten i den ordning de bör göras: `01. [Grupp] Titel`.
- Sortera tasken i svårighet och tidskrav

## Varje task ska ha en beskrivning med
1. **Mål:** en mening om varför tasken finns.
2. **Kodexempel** (inte facit) som faktiskt kompilerar och bygger vidare på de tidigare korten (samma klassnamn, metodnamn och designval genom hela kedjan).
3. **Förklaring av det svåra:** ett "Varför?" eller "Se upp:" när något är nytt eller lätt att göra fel (t.ex. `rows[y][x]` vs `walls[x, y]`).
4. **Klart när:** 1–3 konkreta, kontrollerbara punkter ("`dotnet test` är grönt", "Esc avslutar spelet").

## Designregler att hålla genom hela planen
- [t.ex. Bara klassen `Renderer` får skriva till konsolen, så att logiken går att testa.]
- [t.ex. Logik som ska testas tar in sina beroenden som parametrar, t.ex. `Random`.]
- [Lägg till egna regler här.]

## Leverans
Ge mig först **bara listan med kortnamn**, grupperad, så att jag kan godkänna upplägget. När jag har sagt OK, skriv beskrivningarna.

Formatet ska vara markdown som fungerar i [Trello / GitHub Issues / Azure DevOps].
