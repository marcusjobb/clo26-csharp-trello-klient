namespace TrelloKlient;

/// <summary>
/// Slår ihop kort, listor och medlemmar till läsbara rader.
/// </summary>
/// <remarks>
/// Klassen gör INGA nätverksanrop och skriver INGET till konsolen.
/// Den tar in data och returnerar data – därför är den lätt att testa
/// (se TaskReportTests.cs).
/// </remarks>
public static class TaskReport
{
    /// <summary>Visas när ingen är ansvarig för ett kort.</summary>
    public const string Unassigned = "(ingen)";

    /// <summary>Visas när ett id inte går att slå upp.</summary>
    public const string Unknown = "?";

    public static List<TaskRow> Build(
        IEnumerable<TrelloCard> cards,
        IEnumerable<TrelloList> lists,
        IEnumerable<TrelloMember> members)
    {
        // Bygg två "uppslagsböcker": id -> namn.
        // Ett Dictionary hittar ett värde direkt, i stället för att leta
        // igenom hela listan för varje kort.
        var listNames = lists.ToDictionary(list => list.Id, list => list.Name);
        var memberNames = members.ToDictionary(member => member.Id, member => member.FullName);

        // Select gör om varje kort till en TaskRow.
        return cards
            .Select(card => new TaskRow(
                Task: card.Name,
                Responsible: ResponsibleFor(card, memberNames),
                Status: listNames.GetValueOrDefault(card.IdList, Unknown)))
            .ToList();
    }

    /// <summary>Namnen på kortets medlemmar, kommaseparerade.</summary>
    private static string ResponsibleFor(TrelloCard card, Dictionary<string, string> memberNames)
    {
        if (card.IdMembers.Count == 0)
            return Unassigned;

        // GetValueOrDefault: ge namnet om id:t finns, annars "?".
        var names = card.IdMembers.Select(id => memberNames.GetValueOrDefault(id, Unknown));
        return string.Join(", ", names);
    }
}
