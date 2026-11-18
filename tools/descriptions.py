"""Uppdaterar beskrivningarna på spelkorten (matchas på kortnumret 'NN.').
Användning: python descriptions.py <sökväg till secrets.json>"""
import json, sys, urllib.request, urllib.parse

D = {}

# ---------------------------------------------------------------- SETUP
D[1] = r'''
**Mål:** Ett gemensamt repo på GitHub där all kod för spelet bor.

**Steg**
1. Gå till github.com → **New repository**
2. Namn: `MazeGame`
3. Kryssa i **Add a README file**
4. Lämna .gitignore tom (den fixar vi i kort 03)

Eller från terminalen med GitHub CLI:
```powershell
gh repo create MazeGame --public --add-readme
```

Lägg sedan till alla i gruppen: **Settings → Collaborators → Add people**.

**Klart när**
- Repot syns på GitHub
- Alla i gruppen har skrivrättighet
'''

D[2] = r'''
**Mål:** Ha repot lokalt på din dator så att du kan börja koda.

```powershell
cd C:\git
git clone https://github.com/<användarnamn>/MazeGame.git
cd MazeGame
git status
```

`git status` ska säga ungefär:
```
On branch main
nothing to commit, working tree clean
```

**Klart när**
- Mappen finns lokalt och `git status` fungerar
'''

D[3] = r'''
**Mål:** Se till att byggfiler (`bin/`, `obj/`) och inställningar från Visual Studio aldrig hamnar i repot.

```powershell
dotnet new gitignore
git add .gitignore
git commit -m "Lägg till .gitignore för .NET"
git push
```

**Varför?** `bin/` och `obj/` skapas på nytt varje gång du bygger. Om de committas blir det merge-konflikter hela tiden.

**Klart när**
- Efter `dotnet build` visar `git status` inga `bin/` eller `obj/`-mappar
'''

D[4] = r'''
**Mål:** Ett körbart konsolprojekt.

```powershell
dotnet new console -n MazeGame -o src/MazeGame
dotnet run --project src/MazeGame
```

Det ska skriva ut `Hello, World!`.

Mappstruktur efteråt:
```
MazeGame/
├── .gitignore
├── README.md
└── src/
    └── MazeGame/
        ├── MazeGame.csproj
        └── Program.cs
```

**Klart när**
- `dotnet run` fungerar
- Committat och pushat
'''

D[5] = r'''
**Mål:** Ett testprojekt så att vi kan testa logiken (labyrint, rörelse, monster) utan att starta spelet.

```powershell
dotnet new sln -n MazeGame
dotnet new xunit -n MazeGame.Tests -o tests/MazeGame.Tests
dotnet sln add src/MazeGame tests/MazeGame.Tests
dotnet add tests/MazeGame.Tests reference src/MazeGame
dotnet test
```

`dotnet test` ska visa `Passed!` (mallen har ett tomt test som går igenom).

**Tips:** Ta bort `UnitTest1.cs` när du har skrivit ditt första riktiga test (kort 10).

**Klart när**
- `dotnet test` är grönt
- Solution-filen öppnas i Visual Studio med båda projekten
'''

D[6] = r'''
**Mål:** En plats för det som är kvar, så att nya idéer inte stör det vi håller på med.

Skapa `BACKLOG.md` i repots rot:
```markdown
# Backlog

## Klart
- [x] Repo och projekt

## Pågår
- [ ] Labyrinten

## Att göra
- [ ] Spelare
- [ ] Monster

## Idéer (senare)
- Power-ups som gör monstren rädda
```

**Regel:** Får du en ny idé mitt i ett kort? Skriv in den sist under *Idéer* och fortsätt med det du höll på med.

**Klart när**
- Filen finns, är committad och alla i gruppen vet om den
'''

# ---------------------------------------------------------------- GRUND
D[7] = r'''
**Mål:** Ett sätt att beskriva åt vilket håll något rör sig.

Skapa filen `Direction.cs`:
```csharp
namespace MazeGame;

public enum Direction
{
    None,
    Up,
    Down,
    Left,
    Right
}
```

**Varför `None`?** När ingen tangent är nedtryckt ska spelaren stå still. Med `None` slipper vi `null`.

**Klart när**
- Projektet bygger
'''

D[8] = r'''
**Mål:** En typ som håller en plats i labyrinten.

Skapa filen `Position.cs`:
```csharp
namespace MazeGame;

public readonly record struct Position(int X, int Y);
```

- `X` = kolumn (vänster → höger)
- `Y` = rad (uppifrån och **ned**, Y växer nedåt i konsolen!)

**Varför `record struct`?** Du får jämförelse på värden på köpet:
```csharp
var a = new Position(2, 3);
var b = new Position(2, 3);
Console.WriteLine(a == b); // True
```
Det kommer vi att använda för att se om ett monster har tagit spelaren.

**Klart när**
- Projektet bygger
'''

D[9] = r'''
**Mål:** Räkna ut nästa ruta åt ett visst håll.

Lägg till en kropp i `Position`:
```csharp
public readonly record struct Position(int X, int Y)
{
    public Position Move(Direction direction) => direction switch
    {
        Direction.Up    => this with { Y = Y - 1 },
        Direction.Down  => this with { Y = Y + 1 },
        Direction.Left  => this with { X = X - 1 },
        Direction.Right => this with { X = X + 1 },
        _               => this
    };
}
```

**Obs:** `Move` ändrar **inte** den gamla positionen, den returnerar en ny. Då kan vi först kolla om nästa ruta är en vägg innan vi flyttar.

```csharp
var p = new Position(5, 5);
var next = p.Move(Direction.Up); // (5, 4)
// p är fortfarande (5, 5)
```

**Klart när**
- Projektet bygger
'''

D[10] = r'''
**Mål:** Bevisa att `Move` fungerar åt alla håll.

Skapa `PositionTests.cs` i testprojektet:
```csharp
using MazeGame;

namespace MazeGame.Tests;

public class PositionTests
{
    [Theory]
    [InlineData(Direction.Up,    5, 4)]
    [InlineData(Direction.Down,  5, 6)]
    [InlineData(Direction.Left,  4, 5)]
    [InlineData(Direction.Right, 6, 5)]
    [InlineData(Direction.None,  5, 5)]
    public void Move_ReturnsNeighbour(Direction direction, int expectedX, int expectedY)
    {
        var start = new Position(5, 5);

        var result = start.Move(direction);

        Assert.Equal(new Position(expectedX, expectedY), result);
    }
}
```

`[Theory]` + `[InlineData]` = samma test med olika indata. Fem tester för priset av ett.

**Klart när**
- `dotnet test` visar 5 gröna tester
'''

# ---------------------------------------------------------------- LABYRINT
D[11] = r'''
**Mål:** En klass som håller koll på var väggarna är.

Skapa `Maze.cs`:
```csharp
namespace MazeGame;

public class Maze
{
    private readonly bool[,] _walls; // [x, y] – true = vägg

    private Maze(bool[,] walls)
    {
        _walls = walls;
    }
}
```

**Varför privat konstruktor?** En `Maze` ska alltid skapas från en bana via `Maze.Load(...)` (kort 13). Då kan ingen skapa en halvfärdig labyrint.

**Klart när**
- Projektet bygger
'''

D[12] = r'''
**Mål:** Den första banan, ritad som text.

Skapa `Levels.cs`:
```csharp
namespace MazeGame;

public static class Levels
{
    public static readonly string[] Level1 =
    [
        "####################",
        "#P       ##       M#",
        "# ## ### ## ### ## #",
        "#                  #",
        "# ## # ###### # ## #",
        "#    #   ##   #    #",
        "#### ### ## ### ####",
        "#                  #",
        "# ## ### ## ### ## #",
        "#M       ##       M#",
        "####################",
    ];
}
```

| Tecken | Betyder |
|---|---|
| `#` | Vägg |
| ` ` | Gång |
| `P` | Spelarens start |
| `M` | Ett monsters start |

Rita gärna en egen bana, men tänk på reglerna nedan.

**Klart när**
- Alla rader är **exakt lika långa**
- Kanten runt om är vägg
- Alla gångar hänger ihop (inga instängda rum)
'''

D[13] = r'''
**Mål:** Göra om textbanan till en `Maze`.

Lägg till i `Maze`:
```csharp
public Position PlayerStart { get; private set; }
public List<Position> MonsterStarts { get; } = [];

public static Maze Load(string[] rows)
{
    int height = rows.Length;
    int width = rows[0].Length;
    var walls = new bool[width, height];
    var maze = new Maze(walls);

    for (int y = 0; y < height; y++)
    {
        if (rows[y].Length != width)
            throw new ArgumentException($"Rad {y} har fel längd.");

        for (int x = 0; x < width; x++)
        {
            switch (rows[y][x])
            {
                case '#': walls[x, y] = true; break;
                case 'P': maze.PlayerStart = new Position(x, y); break;
                case 'M': maze.MonsterStarts.Add(new Position(x, y)); break;
            }
        }
    }
    return maze;
}
```

**Se upp:** En sträng läses `rows[y][x]` (rad först), men vår array är `walls[x, y]` (kolumn först). Det är lätt att blanda ihop!

**Klart när**
- `Maze.Load(Levels.Level1)` kraschar inte
'''

D[14] = r'''
**Mål:** Kunna fråga hur stor labyrinten är.

```csharp
public int Width  => _walls.GetLength(0);
public int Height => _walls.GetLength(1);
```

`GetLength(0)` = storleken i första dimensionen (x), `GetLength(1)` = andra (y).

Används senare för att:
- rita hela banan (kort 18)
- skriva poängen på raden **under** banan (kort 31)

**Klart när**
- `Maze.Load(Levels.Level1).Width` ger `20` och `Height` ger `11`
'''

D[15] = r'''
**Mål:** Svara på frågan "får man gå hit?".

```csharp
public bool IsInside(Position p) =>
    p.X >= 0 && p.X < Width && p.Y >= 0 && p.Y < Height;

public bool IsWall(Position p) =>
    !IsInside(p) || _walls[p.X, p.Y];
```

**Varför räknas "utanför kartan" som vägg?** Då kan varken spelare eller monster springa ut ur banan, och vi får aldrig `IndexOutOfRangeException`.

**Klart när**
- Projektet bygger
'''

D[16] = r'''
**Mål:** Testa labyrinten med en pytteliten bana.

`MazeTests.cs`:
```csharp
using MazeGame;

namespace MazeGame.Tests;

public class MazeTests
{
    private static Maze Tiny() => Maze.Load(
    [
        "###",
        "#P#",
        "###",
    ]);

    [Fact]
    public void IsWall_Corner_IsTrue() =>
        Assert.True(Tiny().IsWall(new Position(0, 0)));

    [Fact]
    public void IsWall_Floor_IsFalse() =>
        Assert.False(Tiny().IsWall(new Position(1, 1)));

    [Fact]
    public void IsWall_OutsideMap_IsTrue() =>
        Assert.True(Tiny().IsWall(new Position(-1, 5)));

    [Fact]
    public void Load_FindsPlayerStart() =>
        Assert.Equal(new Position(1, 1), Tiny().PlayerStart);

    [Fact]
    public void Load_RowsWithDifferentLength_Throws() =>
        Assert.Throws<ArgumentException>(() => Maze.Load(["###", "#"]));
}
```

**Klart när**
- Alla tester är gröna
'''

# ---------------------------------------------------------------- RITA
D[17] = r'''
**Mål:** En klass som är den **enda** som pratar med konsolen.

`Renderer.cs`:
```csharp
namespace MazeGame;

/// <summary>All utskrift till konsolen sker här – ingen annanstans.</summary>
public class Renderer
{
}
```

**Varför?** Om `Maze`, `Player` och `Monster` aldrig skriver till `Console` kan vi testa dem i xUnit. Utskrift i testerna går inte att kontrollera.

**Regel för gruppen:** Hittar du `Console.Write` i någon annan klass än `Renderer` (och `InputHandler` för tangenter), flytta den hit.

**Klart när**
- Klassen finns och projektet bygger
'''

D[18] = r'''
**Mål:** Se labyrinten på skärmen för första gången.

```csharp
using System.Text;

public void DrawMaze(Maze maze)
{
    Console.Clear();
    for (int y = 0; y < maze.Height; y++)
    {
        var line = new StringBuilder();
        for (int x = 0; x < maze.Width; x++)
            line.Append(maze.IsWall(new Position(x, y)) ? '#' : ' ');

        Console.WriteLine(line);
    }
}
```

Testa i `Program.cs`:
```csharp
using MazeGame;

var maze = Maze.Load(Levels.Level1);
new Renderer().DrawMaze(maze);
```

**Tips:** `StringBuilder` + en `WriteLine` per rad går mycket snabbare än en `Write` per tecken.

**Klart när**
- `dotnet run` visar banan
'''

D[19] = r'''
**Mål:** Rita ett enda tecken på en viss plats, utan att rita om hela skärmen.

```csharp
public void DrawAt(Position p, char symbol)
{
    Console.SetCursorPosition(p.X, p.Y);
    Console.Write(symbol);
}
```

Så här flyttar man något:
```csharp
renderer.DrawAt(oldPosition, ' ');  // sudda där den var
renderer.DrawAt(newPosition, '@');  // rita där den är nu
```

**Varför inte `Console.Clear()` varje gång?** Hela skärmen blinkar då. Om vi bara ritar om det som har ändrats flimrar det inte alls.

**Klart när**
- Du kan rita ett `@` mitt i banan från `Program.cs`
'''

D[20] = r'''
**Mål:** Ta bort den blinkande markören och återställa konsolen när spelet slutar.

```csharp
public void Init()
{
    Console.CursorVisible = false;
    Console.OutputEncoding = System.Text.Encoding.UTF8; // å, ä, ö
}

public void Restore(Maze maze)
{
    Console.CursorVisible = true;
    Console.SetCursorPosition(0, maze.Height + 3); // under banan och poängen
}
```

`Restore` anropas i en `finally` i spelloopen (kort 27), så att markören kommer tillbaka även om spelet kraschar.

**Klart när**
- Ingen markör blinkar i banan
- Efter avslut hamnar prompten **under** banan, inte mitt i den
'''

# ---------------------------------------------------------------- SPELARE
D[21] = r'''
**Mål:** Spelaren som objekt.

`Player.cs`:
```csharp
namespace MazeGame;

public class Player
{
    public const char Symbol = '@';

    public Position Position { get; private set; }

    public Player(Position start)
    {
        Position = start;
    }
}
```

**Varför `private set`?** Bara `Player` själv får flytta spelaren, via `TryMove` (kort 24). Då kan ingen annan kod råka flytta in den i en vägg.

**Klart när**
- `new Player(maze.PlayerStart)` fungerar och kan ritas med `DrawAt`
'''

D[22] = r'''
**Mål:** Översätta en tangent till en `Direction`.

`InputHandler.cs`:
```csharp
namespace MazeGame;

public static class InputHandler
{
    public static Direction ToDirection(ConsoleKey key) => key switch
    {
        ConsoleKey.UpArrow    or ConsoleKey.W => Direction.Up,
        ConsoleKey.DownArrow  or ConsoleKey.S => Direction.Down,
        ConsoleKey.LeftArrow  or ConsoleKey.A => Direction.Left,
        ConsoleKey.RightArrow or ConsoleKey.D => Direction.Right,
        _                                     => Direction.None
    };
}
```

Funktionen läser inte själv från tangentbordet, så den går att testa:
```csharp
[Fact]
public void ToDirection_W_IsUp() =>
    Assert.Equal(Direction.Up, InputHandler.ToDirection(ConsoleKey.W));
```

**Klart när**
- Både piltangenter och WASD fungerar
- Minst ett test finns
'''

D[23] = r'''
**Mål:** Läsa tangenter **utan att spelet stannar** och väntar.

Lägg till i `InputHandler`:
```csharp
/// <summary>Returnerar senast tryckta tangent, eller null om ingen tryckts.</summary>
public static ConsoleKey? ReadKey()
{
    ConsoleKey? last = null;

    while (Console.KeyAvailable)
        last = Console.ReadKey(intercept: true).Key;

    return last;
}
```

**Varför inte bara `Console.ReadKey()`?** Den **väntar** tills någon trycker. Då står monstren också still. Med `KeyAvailable` frågar vi först om det finns en tangent att läsa.

- `intercept: true` = tecknet skrivs inte ut på skärmen
- `while`-loopen tömmer bufferten. Om du håller in en tangent byggs det annars upp en kö och spelaren fortsätter gå efter att du släppt.

**Klart när**
- Spelet läser tangenter utan att frysa
'''

D[24] = r'''
**Mål:** Flytta spelaren, men aldrig in i en vägg.

Lägg till i `Player`:
```csharp
public bool TryMove(Direction direction, Maze maze)
{
    Position next = Position.Move(direction);

    if (maze.IsWall(next))
        return false;

    Position = next;
    return true;
}
```

**Varför `bool`?** Spelloopen vill veta om spelaren faktiskt flyttade, så att den bara ritar om när något har ändrats.

`Try`-prefixet är en C#-konvention (jämför `int.TryParse`): "försök, och berätta om det gick".

**Klart när**
- Projektet bygger
'''

D[25] = r'''
**Mål:** Bevisa att väggar stoppar spelaren.

`PlayerTests.cs`:
```csharp
using MazeGame;

namespace MazeGame.Tests;

public class PlayerTests
{
    private static Maze Corridor() => Maze.Load(
    [
        "#####",
        "#P  #",
        "#####",
    ]);

    [Fact]
    public void TryMove_IntoWall_StaysPut()
    {
        var maze = Corridor();
        var player = new Player(maze.PlayerStart);

        bool moved = player.TryMove(Direction.Up, maze);

        Assert.False(moved);
        Assert.Equal(new Position(1, 1), player.Position);
    }

    [Fact]
    public void TryMove_IntoFloor_Moves()
    {
        var maze = Corridor();
        var player = new Player(maze.PlayerStart);

        bool moved = player.TryMove(Direction.Right, maze);

        Assert.True(moved);
        Assert.Equal(new Position(2, 1), player.Position);
    }
}
```

**Klart när**
- Båda testerna är gröna
'''

# ---------------------------------------------------------------- SPELLOOP
D[26] = r'''
**Mål:** En klass som håller ihop allt: bana, spelare, ritning.

`Game.cs`:
```csharp
namespace MazeGame;

public class Game
{
    private readonly Maze _maze;
    private readonly Player _player;
    private readonly Renderer _renderer = new();
    private bool _running = true;

    public Game(string[] level)
    {
        _maze = Maze.Load(level);
        _player = new Player(_maze.PlayerStart);
    }
}
```

`Program.cs` blir nu bara:
```csharp
using MazeGame;

new Game(Levels.Level1).Run();
```
(`Run` skriver du i nästa kort.)

**Klart när**
- Klassen finns
'''

D[27] = r'''
**Mål:** Själva hjärtat i spelet, loopen som kör ungefär 10 gånger per sekund.

```csharp
public void Run()
{
    _renderer.Init();
    _renderer.DrawMaze(_maze);
    _renderer.DrawAt(_player.Position, Player.Symbol);

    try
    {
        while (_running)
        {
            HandleInput();          // 1. läs tangent
            Update();               // 2. flytta monster, kolla krockar
            Thread.Sleep(100);      // 3. vänta lite
        }
    }
    finally
    {
        _renderer.Restore(_maze);
    }
}

private void HandleInput()
{
    ConsoleKey? key = InputHandler.ReadKey();
    if (key is null)
        return;

    Position old = _player.Position;
    if (_player.TryMove(InputHandler.ToDirection(key.Value), _maze))
    {
        _renderer.DrawAt(old, ' ');
        _renderer.DrawAt(_player.Position, Player.Symbol);
    }
}

private void Update()
{
    // Monstren kommer hit senare
}
```

**Pac-Man-känsla (frivilligt):** Spara senaste riktningen i ett fält `_direction` och försök flytta åt det hållet **varje varv**, inte bara när en tangent trycks. Då fortsätter spelaren springa tills den slår i en vägg.

**Klart när**
- Du kan springa runt i banan med pilarna
'''

D[28] = r'''
**Mål:** Kunna avsluta spelet snyggt.

Först i `HandleInput`, direkt efter `null`-kollen:
```csharp
if (key == ConsoleKey.Escape)
{
    _running = false;
    return;
}
```

Loopen tar slut, `finally` kör `Restore`, och programmet avslutas.

**Klart när**
- Esc avslutar spelet
- Markören syns igen och prompten hamnar under banan
'''

# ---------------------------------------------------------------- PRICKAR
D[29] = r'''
**Mål:** Prickar i alla gångar, som i Pac-Man.

I `Maze`:
```csharp
public const char PelletSymbol = '.';

private readonly HashSet<Position> _pellets = [];

public bool HasPellet(Position p) => _pellets.Contains(p);
public int PelletsLeft => _pellets.Count;
```

I `Load`, lägg till i `switch`:
```csharp
case ' ':
case 'M':
    maze._pellets.Add(new Position(x, y));
    break;
```
(Ingen prick där spelaren startar.)

I `Renderer.DrawMaze`, byt raden som väljer tecken:
```csharp
var p = new Position(x, y);
line.Append(maze.IsWall(p) ? '#' : maze.HasPellet(p) ? Maze.PelletSymbol : ' ');
```

Lägg också till en metod som ritar det som **ligger** på en ruta. Den behövs när ett monster lämnar en ruta med en prick:
```csharp
public void DrawCell(Maze maze, Position p) =>
    DrawAt(p, maze.HasPellet(p) ? Maze.PelletSymbol : ' ');
```

**Varför `HashSet`?** `Contains` och `Remove` går blixtsnabbt, oavsett hur många prickar som finns.

**Klart när**
- Banan visas full av prickar
'''

D[30] = r'''
**Mål:** Spelaren äter prickar och får poäng.

I `Maze`:
```csharp
/// <summary>Tar bort pricken. Returnerar true om det fanns en.</summary>
public bool EatPellet(Position p) => _pellets.Remove(p);
```

I `Game`:
```csharp
private int _score;
public int Score => _score;
```

I `HandleInput`, efter att spelaren har flyttat:
```csharp
if (_maze.EatPellet(_player.Position))
    _score += 10;
```

Pricken försvinner från skärmen automatiskt, eftersom spelaren ritas ovanpå den och `' '` ritas när spelaren går vidare.

**Klart när**
- Prickarna försvinner där du går
'''

D[31] = r'''
**Mål:** Se poängen medan man spelar.

I `Renderer`:
```csharp
public void DrawStatus(Maze maze, int score)
{
    Console.SetCursorPosition(0, maze.Height + 1);
    Console.Write($"Poäng: {score,-6}  Prickar kvar: {maze.PelletsLeft,-4}");
}
```

**Vad gör `,-6`?** Fyller ut till 6 tecken (vänsterjusterat). Annars ligger gamla siffror kvar: går du från `100` till `90` står det `900` på skärmen.

Anropa `DrawStatus` i `Run` (efter `DrawMaze`) och varje gång spelaren äter en prick.

**Klart när**
- Poängen uppdateras direkt när man äter
'''

D[32] = r'''
**Mål:** Man vinner när alla prickar är uppätna.

I `Game`:
```csharp
private bool _won;
```

I `Update`:
```csharp
if (_maze.PelletsLeft == 0)
{
    _won = true;
    _running = false;
}
```

Efter loopen i `Run` (innan `finally`), tillfälligt:
```csharp
if (_won)
{
    Console.SetCursorPosition(0, _maze.Height + 2);
    Console.Write("Du vann!");
    Thread.Sleep(2000);
}
```
(Det blir snyggare i kort 42. Och ja, det är en `Console.Write` utanför `Renderer`. Flytta gärna dit den.)

**Testtips:** Gör en minibana med bara 2 prickar för att testa vinsten snabbt.

**Klart när**
- Spelet slutar med vinst när sista pricken är uppäten
'''

D[33] = r'''
**Mål:** Testa prick-logiken.

Poängräkningen ligger i `Game`, som pratar med konsolen och är svår att testa. Men **regeln** ligger i `Maze`, och den kan vi testa:

```csharp
public class PelletTests
{
    private static Maze Corridor() => Maze.Load(
    [
        "#####",
        "#P  #",
        "#####",
    ]);

    [Fact]
    public void Load_PutsPelletsOnFloorButNotOnStart()
    {
        var maze = Corridor();

        Assert.Equal(2, maze.PelletsLeft);
        Assert.False(maze.HasPellet(maze.PlayerStart));
    }

    [Fact]
    public void EatPellet_RemovesIt()
    {
        var maze = Corridor();
        var pos = new Position(2, 1);

        Assert.True(maze.EatPellet(pos));
        Assert.False(maze.HasPellet(pos));
        Assert.Equal(1, maze.PelletsLeft);
    }

    [Fact]
    public void EatPellet_SameSpotTwice_SecondTimeFalse()
    {
        var maze = Corridor();
        var pos = new Position(2, 1);
        maze.EatPellet(pos);

        Assert.False(maze.EatPellet(pos)); // ingen dubbelpoäng
    }
}
```

**Klart när**
- Testerna är gröna
'''

# ---------------------------------------------------------------- MONSTER
D[34] = r'''
**Mål:** Monstret som objekt.

`Monster.cs`:
```csharp
namespace MazeGame;

public class Monster
{
    public const char Symbol = 'M';

    public Position Position { get; private set; }

    public Monster(Position start)
    {
        Position = start;
    }
}
```

I `Game`:
```csharp
private readonly List<Monster> _monsters;

// i konstruktorn:
_monsters = _maze.MonsterStarts.Select(p => new Monster(p)).ToList();
```

I `Run`, rita dem efter spelaren:
```csharp
foreach (var monster in _monsters)
    _renderer.DrawAt(monster.Position, Monster.Symbol);
```

**Klart när**
- Monstren syns på sina startplatser (de står still än så länge)
'''

D[35] = r'''
**Mål:** Monstren vandrar runt slumpmässigt.

I `Monster`:
```csharp
private static readonly Direction[] AllDirections =
    [Direction.Up, Direction.Down, Direction.Left, Direction.Right];

public void MoveRandomly(Maze maze, Random random)
{
    var possible = AllDirections
        .Where(d => !maze.IsWall(Position.Move(d)))
        .ToList();

    if (possible.Count > 0)
        Position = Position.Move(possible[random.Next(possible.Count)]);
}
```

I `Game`:
```csharp
private readonly Random _random = new();

private void MoveMonsters()
{
    foreach (var monster in _monsters)
    {
        Position old = monster.Position;
        monster.MoveRandomly(_maze, _random);
        _renderer.DrawCell(_maze, old);   // rita tillbaka pricken!
        _renderer.DrawAt(monster.Position, Monster.Symbol);
    }
}
```
Anropa `MoveMonsters()` från `Update()`.

**Varför skicka in `Random` som parameter?** I tester kan man då använda `new Random(42)`, som ger samma "slump" varje gång.

**Klart när**
- Monstren vandrar runt utan att gå genom väggar
- Prickarna ligger kvar där monstren har gått
'''

D[36] = r'''
**Mål:** Ge spelaren en chans: monstren rör sig inte varje varv.

I `Game`:
```csharp
private const int MonsterSpeed = 3; // flytta var 3:e varv
private int _tick;

private void Update()
{
    _tick++;
    if (_tick % MonsterSpeed == 0)
        MoveMonsters();

    // ...vinstkollen från kort 32
}
```

**Hur funkar `%`?** Det är resten vid division. `_tick % 3` blir 1, 2, 0, 1, 2, 0 … så det blir `0` var tredje gång.

| MonsterSpeed | Känsla |
|---|---|
| 1 | Omöjligt |
| 2 | Svårt |
| 3 | Lagom |
| 4 | Lätt |

**Klart när**
- Spelaren är märkbart snabbare än monstren
'''

D[37] = r'''
**Mål:** Monstren jagar spelaren.

**Idén:** Titta på de 4 grannrutorna och välj den som ligger närmast spelaren.

I `Monster`:
```csharp
public void Chase(Position target, Maze maze)
{
    var options = AllDirections
        .Select(d => Position.Move(d))
        .Where(p => !maze.IsWall(p))
        .ToList();

    if (options.Count == 0)
        return;

    Position = options.MinBy(p => Distance(p, target));
}

private static int Distance(Position a, Position b) =>
    Math.Abs(a.X - b.X) + Math.Abs(a.Y - b.Y);
```

**Lite matte:** `Distance` kallas *Manhattan-avstånd*: hur många steg man måste gå om man bara får gå rakt (som gatorna på Manhattan). Från (1,1) till (4,3) är det |4−1| + |3−1| = 3 + 2 = **5 steg**.

**Problem:** Ett monster som bara jagar fastnar ofta bakom väggar. Blanda därför in lite slump i `MoveMonsters`:
```csharp
if (_random.Next(100) < 75)          // 75 % av gångerna
    monster.Chase(_player.Position, _maze);
else
    monster.MoveRandomly(_maze, _random);
```

**Klart när**
- Monstren rör sig tydligt mot spelaren, men fastnar inte för alltid
'''

D[38] = r'''
**Mål:** Testa monstrens rörelser.

`MonsterTests.cs`:
```csharp
using MazeGame;

namespace MazeGame.Tests;

public class MonsterTests
{
    [Fact]
    public void Chase_MovesCloserToTarget()
    {
        var maze = Maze.Load(
        [
            "#######",
            "#M   P#",
            "#######",
        ]);
        var monster = new Monster(maze.MonsterStarts[0]);

        monster.Chase(maze.PlayerStart, maze);

        Assert.Equal(new Position(2, 1), monster.Position);
    }

    [Fact]
    public void MoveRandomly_NeverEntersWall()
    {
        var maze = Maze.Load(
        [
            "###",
            "#M#",
            "# #",
            "###",
        ]);
        var monster = new Monster(maze.MonsterStarts[0]);

        monster.MoveRandomly(maze, new Random(42));

        Assert.Equal(new Position(1, 2), monster.Position); // enda möjliga steget
    }
}
```

**Klart när**
- Testerna är gröna
'''

D[39] = r'''
**Mål:** Blir man tagen är spelet slut.

I `Game`:
```csharp
private bool PlayerIsCaught() =>
    _monsters.Any(m => m.Position == _player.Position);
```
(Här betalar sig `record struct` från kort 08: `==` jämför X och Y åt oss.)

Kolla på **två** ställen:
1. I `HandleInput`, efter att spelaren har flyttat (spelaren gick in i ett monster)
2. I `MoveMonsters`, efter att monstren har flyttat (ett monster gick in i spelaren)

```csharp
if (PlayerIsCaught())
{
    _running = false; // tre liv kommer i kort 43
}
```

**Varför två ställen?** Kollar du bara på ett ställe kan spelaren och monstret byta plats med varandra och "gå igenom" varandra.

**Klart när**
- Spelet slutar när ett monster når spelaren
'''

D[40] = r'''
**Mål:** Flera monster som beter sig olika.

Fler monster får du redan gratis: rita fler `M` i banan, så skapar `MonsterStarts` dem.

**Gör dem olika:** Lägg till i `Monster`:
```csharp
public bool IsChaser { get; init; }
```

När de skapas i `Game` blir varannan en jägare:
```csharp
_monsters = _maze.MonsterStarts
    .Select((pos, i) => new Monster(pos) { IsChaser = i % 2 == 0 })
    .ToList();
```

I `MoveMonsters`:
```csharp
if (monster.IsChaser && _random.Next(100) < 75)
    monster.Chase(_player.Position, _maze);
else
    monster.MoveRandomly(_maze, _random);
```

**Idé:** Ge jägarna en annan färg i kort 44, så att spelaren ser vilka som är farligast.

**Klart när**
- 3 monster på Level1, minst ett jagar och minst ett vandrar
'''

# ---------------------------------------------------------------- FINPUTS
D[41] = r'''
**Mål:** En välkomstskärm som förklarar spelet.

I `Renderer`:
```csharp
public void DrawStartScreen()
{
    Console.Clear();
    Console.WriteLine("""
        ===  LABYRINTEN  ===

        Ät alla prickar (.) utan att bli tagen av monstren (M).

        Styr:     piltangenter eller WASD
        Avsluta:  Esc

        Tryck på valfri tangent för att börja...
        """);
    Console.ReadKey(intercept: true);
}
```

`"""` är en *raw string literal* (C# 11). Radbrytningar och indrag blir som de står, och indraget fram till sista `"""` tas bort automatiskt.

Anropa den först i `Program.cs`.

**Klart när**
- Startskärmen visas och spelet börjar vid tangenttryck
'''

D[42] = r'''
**Mål:** En tydlig slutskärm och möjlighet att spela igen.

Skapa `GameResult.cs`:
```csharp
namespace MazeGame;

public enum GameResult { Won, Lost, Quit }
```

Låt `Game.Run()` returnera `GameResult` i stället för `void`. Byt ut `_won` mot ett fält `_result`.

I `Renderer`:
```csharp
public bool AskPlayAgain(GameResult result, int score)
{
    Console.Clear();
    Console.WriteLine(result == GameResult.Won ? "*** DU VANN! ***" : "*** GAME OVER ***");
    Console.WriteLine($"Poäng: {score}");
    Console.Write("Spela igen? (j/n) ");
    return Console.ReadKey(intercept: true).Key == ConsoleKey.J;
}
```

`Program.cs`:
```csharp
var renderer = new Renderer();
renderer.DrawStartScreen();

bool playAgain;
do
{
    var game = new Game(Levels.Level1);
    GameResult result = game.Run();

    playAgain = result != GameResult.Quit
             && renderer.AskPlayAgain(result, game.Score);
}
while (playAgain);
```

**Klart när**
- Vinst och förlust ger olika skärmar
- `j` startar ett nytt spel med alla prickar tillbaka
- Esc avslutar direkt utan fråga
'''

D[43] = r'''
**Mål:** Tre liv. Blir man tagen startar man om på startplatsen.

I `Player` och `Monster`:
```csharp
public void MoveTo(Position p) => Position = p;
```

I `Game`:
```csharp
private int _lives = 3;

private void OnCaught()
{
    _lives--;
    if (_lives == 0)
    {
        _result = GameResult.Lost;
        _running = false;
        return;
    }

    _renderer.DrawCell(_maze, _player.Position);
    _player.MoveTo(_maze.PlayerStart);
    _renderer.DrawAt(_player.Position, Player.Symbol);

    for (int i = 0; i < _monsters.Count; i++)
    {
        _renderer.DrawCell(_maze, _monsters[i].Position);
        _monsters[i].MoveTo(_maze.MonsterStarts[i]);
        _renderer.DrawAt(_monsters[i].Position, Monster.Symbol);
    }

    Thread.Sleep(1000); // andrum innan det börjar igen
}
```

Byt ut `_running = false` från kort 39 mot `OnCaught()`.

Visa liven i `DrawStatus`:
```csharp
Console.Write($"Poäng: {score,-6}  Liv: {lives}  Prickar kvar: {maze.PelletsLeft,-4}");
```

**Obs:** Prickarna ska **inte** komma tillbaka när man dör, bara när man startar ett nytt spel.

**Klart när**
- Man överlever två gånger, den tredje blir Game Over
'''

D[44] = r'''
**Mål:** Färg, så att man ser direkt vad som är vad.

I `Renderer`:
```csharp
private static ConsoleColor ColorOf(char symbol) => symbol switch
{
    '@' => ConsoleColor.Yellow,
    'M' => ConsoleColor.Red,
    '#' => ConsoleColor.DarkBlue,
    '.' => ConsoleColor.White,
    _   => ConsoleColor.Gray
};

public void DrawAt(Position p, char symbol)
{
    Console.SetCursorPosition(p.X, p.Y);
    Console.ForegroundColor = ColorOf(symbol);
    Console.Write(symbol);
    Console.ResetColor();
}
```

Snyggt med den här designen: ingen annan klass behöver ändras, eftersom allt redan ritas via `DrawAt`. Utom `DrawMaze`, som skriver hela rader. Byt den till att anropa `DrawAt` för varje ruta (för en bana på 20×11 är det fortfarande snabbt nog).

**Extra:** Jägarmonster (kort 40) kan få `ConsoleColor.Magenta`. Då behöver `DrawAt` en valfri färgparameter.

**Klart när**
- Spelare gul, monster röda, väggar blå
'''

D[45] = r'''
**Mål:** Klarar man en bana kommer nästa, och den är svårare.

I `Levels`:
```csharp
public static readonly string[] Level2 = [ /* rita en ny bana */ ];
public static readonly string[] Level3 = [ /* ... */ ];

public static readonly string[][] All = [Level1, Level2, Level3];
```

Poäng och liv ska följa med mellan banorna. Ge `Game` en konstruktor som tar emot dem:
```csharp
public Game(string[] level, int score, int lives, int monsterSpeed)
```

`Program.cs`:
```csharp
int score = 0, lives = 3;
GameResult result = GameResult.Won;

for (int i = 0; i < Levels.All.Length && result == GameResult.Won; i++)
{
    int speed = Math.Max(1, 3 - i);   // 3, 2, 1: snabbare monster för varje bana
    var game = new Game(Levels.All[i], score, lives, speed);
    result = game.Run();
    score = game.Score;
    lives = game.Lives;
}
```

**Klart när**
- Minst 2 banor
- Poäng och liv följer med
- Monstren blir snabbare för varje bana
'''

# ----------------------------------------------------------------
def api(method, path, auth, params=None, body=None):
    url = "https://api.trello.com/1/" + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = urllib.parse.urlencode(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method, headers={"Authorization": auth})
    with urllib.request.urlopen(req) as r:
        return json.load(r)

def main():
    assert len(D) == 45, len(D)
    s = json.load(open(sys.argv[1], encoding="utf-8-sig"))
    auth = f'OAuth oauth_consumer_key="{s["ApiKey"]}", oauth_token="{s["Token"]}"'
    board = next(b for b in api("GET", "members/me/boards", auth, {"fields": "name,closed"})
                 if not b["closed"] and b["name"].strip().lower() == s["BoardName"].strip().lower())
    updated = 0
    for c in api("GET", f"boards/{board['id']}/cards", auth, {"fields": "name"}):
        num = c["name"][:2]
        if num.isdigit() and int(num) in D:
            api("PUT", f"cards/{c['id']}", auth, body={"desc": D[int(num)].strip()})
            updated += 1
    print(f"Uppdaterade {updated} kort.")

if __name__ == "__main__":
    main()
