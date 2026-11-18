namespace TrelloKlient;

/// <summary>
/// Skriver ut rader som en tabell i konsolen. Det här är den ENDA klassen
/// (förutom Program.cs) som skriver till konsolen.
/// </summary>
public static class TaskTable
{
    private const string Separator = " | ";
    private const string TaskHeader = "Uppgift";
    private const string ResponsibleHeader = "Ansvarig";
    private const string StatusHeader = "Status";

    public static void Print(IReadOnlyList<TaskRow> rows)
    {
        if (rows.Count == 0)
        {
            Console.WriteLine("Inga kort på boarden.");
            return;
        }

        // Varje kolumn ska vara lika bred som sitt längsta värde
        // (eller rubriken, om den är längre).
        int taskWidth = Math.Max(TaskHeader.Length, rows.Max(r => r.Task.Length));
        int responsibleWidth = Math.Max(ResponsibleHeader.Length, rows.Max(r => r.Responsible.Length));
        int statusWidth = Math.Max(StatusHeader.Length, rows.Max(r => r.Status.Length));

        PrintRow(TaskHeader, ResponsibleHeader, StatusHeader, taskWidth, responsibleWidth);

        // Strecket under rubriken blir exakt lika långt som en rad.
        int lineLength = taskWidth + Separator.Length + responsibleWidth + Separator.Length + statusWidth;
        Console.WriteLine(new string('-', lineLength));

        foreach (var row in rows)
            PrintRow(row.Task, row.Responsible, row.Status, taskWidth, responsibleWidth);
    }

    private static void PrintRow(string task, string responsible, string status, int taskWidth, int responsibleWidth)
    {
        // PadRight fyller ut med mellanslag så att kolumnerna hamnar rakt under varandra.
        Console.WriteLine(task.PadRight(taskWidth) + Separator + responsible.PadRight(responsibleWidth) + Separator + status);
    }
}
