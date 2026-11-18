# TrelloKlient

Konsolprogram som listar alla kort på en Trello-board: **uppgift**, **ansvarig** och **status** (= listan kortet ligger i).

## Kom igång

1. Kopiera `TrelloKlient/secrets.example.json` till `TrelloKlient/secrets.json`
2. Fyll i:
   - `ApiKey` – från https://trello.com/power-ups/admin (din Power-Up → API key)
   - `Token` – generera via länken *"Token"* bredvid API-nyckeln (OBS: inte "Secret", den används bara för OAuth)
   - `BoardName` – namnet på boarden, t.ex. `planering av spel`
3. Kör:

```powershell
dotnet run --project TrelloKlient
```

Exempelutskrift:

```
Board: planering av spel

Uppgift                     | Ansvarig | Status
------------------------------------------------
[Setup] Skapa GitHub-repo   | Anna A   | Klart
[Maze] Skapa klassen Maze   | (ingen)  | Att göra
```

`secrets.json` är gitignorerad – committa den aldrig.

## Tester

```powershell
dotnet test
```

## Mer i repot

| Fil | Vad |
|---|---|
| `docs/planeringsprompt.md` | Mall-prompt för att låta en AI planera ett projekt i små tasks med bra beskrivningar, inklusive hur man kopplar AI:n till Trello/GitHub |
| `docs/miniprompt.md` | Kort, generisk prompt: beskriv projektet i tre rader, få uppgifter med ordning och tid, granska förslaget |
| `docs/miniprompt-labyrintspel.md` | Samma miniprompt, ifylld för labyrintspelet |
| `tools/seed_board.py` | Skapar spel-tasks som kort på boarden (`python tools/seed_board.py TrelloKlient/secrets.json`) |
| `tools/descriptions.py` | Fyller korten med utförliga beskrivningar och kodexempel |

## Säkerhet

- `secrets.json` är gitignorerad. Kolla med `git check-ignore -v TrelloKlient/secrets.json`.
- Klistra aldrig in nycklar i en chatt, ett issue eller en commit. Har det hänt: generera nya.
- Nycklarna skickas i en `Authorization`-header, inte i URL:en, så de hamnar inte i loggar.
