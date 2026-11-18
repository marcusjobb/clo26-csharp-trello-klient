// =====================================================================
//  TrelloKlient – listar alla kort på en Trello-board:
//  uppgift, ansvarig och status (= listan kortet ligger i).
//
//  Flödet i programmet:
//    1. Läs nycklar från secrets.json      (Secrets.cs)
//    2. Hämta data från Trellos API        (TrelloClient.cs)
//    3. Slå ihop datan till rader          (TaskReport.cs)   <- ren logik, testad
//    4. Skriv ut raderna som en tabell     (TaskTable.cs)    <- bara utskrift
// =====================================================================

using System.Text;
using TrelloKlient;

// Utan den här raden blir å, ä och ö fel i Windows-konsolen.
Console.OutputEncoding = Encoding.UTF8;

try
{
    // AppContext.BaseDirectory = mappen där programmet körs (bin/Debug/...).
    // secrets.json kopieras dit när man bygger (se TrelloKlient.csproj).
    var secrets = Secrets.Load(Path.Combine(AppContext.BaseDirectory, "secrets.json"));
    var trello = new TrelloClient(secrets.ApiKey, secrets.Token);

    var board = await trello.FindBoardAsync(secrets.BoardName);
    if (board is null)
    {
        Console.WriteLine($"Hittade ingen öppen board som heter \"{secrets.BoardName}\".");
        return 1; // Exitkod 1 = något gick fel. 0 = allt gick bra.
    }

    Console.WriteLine($"Board: {board.Name}\n");

    // Trello ger oss tre separata listor som pekar på varandra med id:n.
    // Kort har idList och idMembers – vi behöver listornas och medlemmarnas
    // NAMN för att kunna skriva ut något läsbart.
    var cards = await trello.GetCardsAsync(board.Id);
    var lists = await trello.GetListsAsync(board.Id);
    var members = await trello.GetMembersAsync(board.Id);

    var rows = TaskReport.Build(cards, lists, members);
    TaskTable.Print(rows);
    return 0;
}
catch (Exception ex)
{
    // Ett enda ställe som fångar alla fel och skriver dem i rött,
    // i stället för att programmet kraschar med en lång stacktrace.
    Console.ForegroundColor = ConsoleColor.Red;
    Console.WriteLine(ex.Message);
    Console.ResetColor();
    return 1;
}
