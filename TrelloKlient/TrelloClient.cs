using System.Net.Http.Json;
using System.Text.Json;

namespace TrelloKlient;

/// <summary>
/// Pratar med Trellos REST-API. Klassen kan bara LÄSA data.
/// Dokumentation: https://developer.atlassian.com/cloud/trello/rest/
/// </summary>
public class TrelloClient
{
    // static readonly = skapas en gång och delas av alla anrop.
    private static readonly JsonSerializerOptions JsonOptions = new() { PropertyNameCaseInsensitive = true };

    private readonly HttpClient _http;

    /// <param name="apiKey">API-nyckeln från Trellos Power-Up-sida.</param>
    /// <param name="token">Token som ger åtkomst till ditt konto (inte "Secret").</param>
    /// <param name="http">Valfri HttpClient – gör att man kan byta ut den i tester.</param>
    public TrelloClient(string apiKey, string token, HttpClient? http = null)
    {
        _http = http ?? new HttpClient();

        // ??= betyder "sätt bara värdet om det är null just nu".
        // Med BaseAddress satt kan vi skriva "boards/123" i stället för hela URL:en.
        _http.BaseAddress ??= new Uri("https://api.trello.com/1/");

        // Nycklarna skickas i en header i stället för i URL:en.
        // URL:er sparas ofta i loggar – headers gör det oftast inte.
        _http.DefaultRequestHeaders.Add("Authorization",
            $"OAuth oauth_consumer_key=\"{apiKey}\", oauth_token=\"{token}\"");
    }

    /// <summary>
    /// Letar bland dina boards efter en med rätt namn.
    /// Returnerar <c>null</c> om ingen hittas.
    /// </summary>
    public async Task<TrelloBoard?> FindBoardAsync(string name)
    {
        // "members/me" = den användare som äger token.
        // "fields=name,closed" = be Trello bara skicka de fälten (mindre data).
        var boards = await GetAsync<List<TrelloBoard>>("members/me/boards?fields=name,closed");

        // FirstOrDefault: första som matchar, annars null.
        // OrdinalIgnoreCase: "Planering av spel" == "planering av spel".
        return boards.FirstOrDefault(b => !b.Closed &&
            string.Equals(b.Name.Trim(), name.Trim(), StringComparison.OrdinalIgnoreCase));
    }

    // => är en kort metodkropp: metoden returnerar det som står efter pilen.

    /// <summary>Alla listor på boarden (de blir "status").</summary>
    public Task<List<TrelloList>> GetListsAsync(string boardId) =>
        GetAsync<List<TrelloList>>($"boards/{boardId}/lists?fields=name");

    /// <summary>Alla medlemmar på boarden (de blir "ansvarig").</summary>
    public Task<List<TrelloMember>> GetMembersAsync(string boardId) =>
        GetAsync<List<TrelloMember>>($"boards/{boardId}/members?fields=fullName,username");

    /// <summary>Alla öppna kort på boarden.</summary>
    public Task<List<TrelloCard>> GetCardsAsync(string boardId) =>
        GetAsync<List<TrelloCard>>($"boards/{boardId}/cards?fields=name,idList,idMembers");

    /// <summary>
    /// Gemensam hjälpmetod för alla GET-anrop: skicka, kolla svaret, gör om JSON till T.
    /// <c>T</c> är en generisk typ – den som anropar bestämmer vad svaret ska bli.
    /// </summary>
    private async Task<T> GetAsync<T>(string url)
    {
        // using = svaret stängs automatiskt när metoden är klar.
        using var response = await _http.GetAsync(url);

        if (!response.IsSuccessStatusCode)
        {
            // Trello förklarar ofta felet i svaret, t.ex. "invalid token".
            // Ta med det i felmeddelandet – det sparar mycket felsökning.
            var body = await response.Content.ReadAsStringAsync();
            throw new HttpRequestException($"Trello svarade {(int)response.StatusCode}: {body}");
        }

        // ! säger till kompilatorn "jag lovar att detta inte är null".
        return (await response.Content.ReadFromJsonAsync<T>(JsonOptions))!;
    }
}
