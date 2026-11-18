namespace TrelloKlient;

// ---------------------------------------------------------------------
//  DTO:er (Data Transfer Objects) – enkla "behållare" som JSON från
//  Trello packas upp i. Namnen på egenskaperna MÅSTE matcha fälten i
//  Trellos JSON (stor/liten bokstav spelar ingen roll, se TrelloClient).
//
//  Vi tar bara med de fält vi behöver. Trello skickar mycket mer,
//  men allt som inte finns här ignoreras automatiskt.
// ---------------------------------------------------------------------

/// <summary>En board. <c>Closed</c> = arkiverad.</summary>
public record TrelloBoard(string Id, string Name, bool Closed);

/// <summary>En lista på boarden, t.ex. "To Do", "Doing", "Done".</summary>
public record TrelloList(string Id, string Name);

/// <summary>En person som är medlem på boarden.</summary>
public record TrelloMember(string Id, string FullName, string Username);

/// <summary>
/// Ett kort. Observera att kortet bara har ID:n till sin lista och sina
/// medlemmar – inte namnen. Namnen slås upp i <see cref="TaskReport"/>.
/// </summary>
public record TrelloCard(string Id, string Name, string IdList, List<string> IdMembers);

/// <summary>En färdig rad att skriva ut: uppgift, ansvarig(a) och status.</summary>
public record TaskRow(string Task, string Responsible, string Status);
