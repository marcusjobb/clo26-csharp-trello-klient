using TrelloKlient;

namespace TrelloKlient.Tests;

/// <summary>
/// Testar TaskReport.Build med påhittad data – inget anrop till Trello behövs.
/// Varje test följer mönstret Arrange (förbered) → Act (gör) → Assert (kontrollera).
/// </summary>
public class TaskReportTests
{
    // Gemensam testdata: två listor och två personer.
    private static readonly List<TrelloList> Lists = [new("L1", "Att göra"), new("L2", "Klart")];
    private static readonly List<TrelloMember> Members = [new("M1", "Anna A", "anna"), new("M2", "Bo B", "bo")];

    [Fact]
    public void Build_MapsListIdToStatusName()
    {
        // Arrange: ett kort som ligger i listan L2 ("Klart") och tillhör Anna.
        List<TrelloCard> cards = [new("C1", "Skapa repo", "L2", ["M1"])];

        // Act
        var rows = TaskReport.Build(cards, Lists, Members);

        // Assert: id:n har blivit namn.
        Assert.Equal(new TaskRow("Skapa repo", "Anna A", "Klart"), rows.Single());
    }

    [Fact]
    public void Build_CardWithoutMembers_IsUnassigned()
    {
        List<TrelloCard> cards = [new("C1", "Skapa Player", "L1", [])];

        var rows = TaskReport.Build(cards, Lists, Members);

        Assert.Equal(TaskReport.Unassigned, rows.Single().Responsible);
    }

    [Fact]
    public void Build_SeveralMembers_AreCommaSeparated()
    {
        List<TrelloCard> cards = [new("C1", "Rita karta", "L1", ["M1", "M2"])];

        var rows = TaskReport.Build(cards, Lists, Members);

        Assert.Equal("Anna A, Bo B", rows.Single().Responsible);
    }

    [Fact]
    public void Build_UnknownIds_ShowQuestionMark()
    {
        // Arrange: listan L9 och personen M9 finns inte – programmet får inte krascha.
        List<TrelloCard> cards = [new("C1", "X", "L9", ["M9"])];

        var rows = TaskReport.Build(cards, Lists, Members);

        Assert.Equal(new TaskRow("X", TaskReport.Unknown, TaskReport.Unknown), rows.Single());
    }
}
