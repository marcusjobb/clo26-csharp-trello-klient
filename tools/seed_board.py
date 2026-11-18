"""Engångsskript: skapar spel-tasks som kort på Trello-boarden.
Användning: python seed_board.py <sökväg till secrets.json>
Idempotent: kort som redan finns (samma namn) hoppas över."""
import json, sys, urllib.request, urllib.parse

TASKS = [
    # (kategori, titel, beskrivning)
    ("Setup", "Skapa GitHub-repo för spelet", "Tomt repo med README."),
    ("Setup", "Klona repot lokalt", "git clone till din dator."),
    ("Setup", "Lägg till .gitignore för .NET", "dotnet new gitignore"),
    ("Setup", "Skapa konsolprojektet", "dotnet new console -n MazeGame"),
    ("Setup", "Skapa testprojekt och solution", "dotnet new xunit + dotnet new sln, koppla ihop."),
    ("Setup", "Skapa BACKLOG.md", "Lista över vad som är kvar att göra."),
    ("Grund", "Skapa enum Direction", "Up, Down, Left, Right, None."),
    ("Grund", "Skapa record struct Position (X, Y)", "Enkel koordinat i labyrinten."),
    ("Grund", "Metod Position.Move(Direction)", "Returnerar en ny Position ett steg åt rätt håll."),
    ("Grund", "Test: Position.Move", "Ett test per riktning."),
    ("Labyrint", "Skapa klassen Maze", "Håller kartan."),
    ("Labyrint", "Rita första banan som string-array", "'#' = vägg, ' ' = gång. Ca 20x10 tecken."),
    ("Labyrint", "Maze.Load(string[] rader)", "Tolka texten till väggar och gångar."),
    ("Labyrint", "Egenskaperna Maze.Width och Maze.Height", ""),
    ("Labyrint", "Metod Maze.IsWall(Position)", "true om vägg eller utanför kartan."),
    ("Labyrint", "Test: Maze.IsWall", "Vägg, gång och utanför kartan."),
    ("Rita", "Skapa klassen Renderer", "All Console-utskrift samlas här."),
    ("Rita", "Renderer.DrawMaze(Maze)", "Skriv ut hela banan en gång."),
    ("Rita", "Renderer.DrawAt(Position, char)", "Console.SetCursorPosition + Write – rita bara det som ändras."),
    ("Rita", "Dölj markören", "Console.CursorVisible = false."),
    ("Spelare", "Skapa klassen Player", "Har en Position och en symbol, t.ex. '@'."),
    ("Spelare", "Skapa klassen InputHandler", "Översätter piltangenter/WASD till Direction."),
    ("Spelare", "Läs tangenter utan att blockera", "Använd Console.KeyAvailable så spelet inte stannar."),
    ("Spelare", "Metod Player.TryMove(Direction, Maze)", "Flytta bara om nästa ruta inte är vägg."),
    ("Spelare", "Test: spelaren går inte in i väggar", ""),
    ("Spelloop", "Skapa klassen Game", "Äger Maze, Player, Renderer."),
    ("Spelloop", "Metod Game.Run() med spelloop", "input → uppdatera → rita → Thread.Sleep(100)."),
    ("Spelloop", "Avsluta spelet med Esc", ""),
    ("Prickar", "Lägg prickar i alla gångar", "'.' i varje tom ruta vid start."),
    ("Prickar", "Spelaren äter prickar", "Prick försvinner, poäng +10."),
    ("Prickar", "Visa poäng under banan", ""),
    ("Prickar", "Vinst när alla prickar är uppätna", ""),
    ("Prickar", "Test: äta prick ger poäng", ""),
    ("Monster", "Skapa klassen Monster", "Har en Position och symbol, t.ex. 'M'."),
    ("Monster", "Monster rör sig slumpmässigt", "Välj en slumpad riktning som inte är vägg."),
    ("Monster", "Monster rör sig långsammare än spelaren", "Flytta bara var 2:a eller 3:e varv i loopen."),
    ("Monster", "Monster jagar spelaren", "Välj det steg som minskar avståndet till spelaren."),
    ("Monster", "Test: jagande monster går närmare", ""),
    ("Monster", "Krock spelare–monster = Game Over", ""),
    ("Monster", "Flera monster med olika startplatser", ""),
    ("Finputs", "Startskärm med instruktioner", ""),
    ("Finputs", "Game Over- och vinstskärm", "Fråga 'Spela igen? (j/n)'."),
    ("Finputs", "Tre liv och omstart på startplatsen", ""),
    ("Finputs", "Färger", "Spelare gul, monster röda, väggar blå."),
    ("Finputs", "Fler banor", "Nästa bana när alla prickar är uppätna."),
]

def api(method, path, auth, params=None):
    url = "https://api.trello.com/1/" + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, method=method, headers={"Authorization": auth})
    with urllib.request.urlopen(req) as r:
        return json.load(r)

def main():
    s = json.load(open(sys.argv[1], encoding="utf-8-sig"))
    auth = f'OAuth oauth_consumer_key="{s["ApiKey"]}", oauth_token="{s["Token"]}"'
    boards = api("GET", "members/me/boards", auth, {"fields": "name,closed"})
    board = next((b for b in boards if not b["closed"]
                  and b["name"].strip().lower() == s["BoardName"].strip().lower()), None)
    if not board:
        sys.exit(f'Hittar ingen board "{s["BoardName"]}". Finns: {[b["name"] for b in boards]}')

    lists = api("GET", f"boards/{board['id']}/lists", auth, {"fields": "name"})
    todo = next((l for l in lists if l["name"].lower() in ("att göra", "to do", "todo")), None)
    if not todo:
        todo = api("POST", "lists", auth, {"name": "Att göra", "idBoard": board["id"], "pos": "top"})
        print("Skapade listan 'Att göra'")

    existing = {c["name"] for c in api("GET", f"boards/{board['id']}/cards", auth, {"fields": "name"})}
    created = 0
    for i, (cat, title, desc) in enumerate(TASKS, 1):
        name = f"{i:02d}. [{cat}] {title}"
        if name in existing:
            continue
        api("POST", "cards", auth, {"idList": todo["id"], "name": name, "desc": desc, "pos": "bottom"})
        created += 1
    print(f"Klart: {created} nya kort i '{todo['name']}' ({len(TASKS) - created} fanns redan).")

if __name__ == "__main__":
    main()

