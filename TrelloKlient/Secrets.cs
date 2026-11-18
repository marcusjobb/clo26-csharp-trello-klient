using System.Text.Json;

namespace TrelloKlient;

/// <summary>
/// Innehållet i secrets.json. Filen är gitignorerad och ska ALDRIG committas.
/// </summary>
/// <remarks>
/// Ett <c>record</c> är en klass som främst håller data. Den här raden ger oss
/// automatiskt en konstruktor och tre egenskaper: ApiKey, Token och BoardName.
/// </remarks>
public record Secrets(string ApiKey, string Token, string BoardName)
{
    /// <summary>Läser och kontrollerar secrets.json.</summary>
    /// <exception cref="FileNotFoundException">Filen finns inte.</exception>
    /// <exception cref="InvalidOperationException">Filen saknar nycklar.</exception>
    public static Secrets Load(string path)
    {
        // Ge ett tydligt felmeddelande som berättar hur man löser problemet.
        if (!File.Exists(path))
            throw new FileNotFoundException(
                $"Hittar inte {path}. Kopiera secrets.example.json till secrets.json och fyll i dina nycklar.");

        // Gör om JSON-texten till ett Secrets-objekt.
        // PropertyNameCaseInsensitive: "apiKey" och "ApiKey" räknas som samma sak.
        // ?? betyder "om vänster sida är null, gör det som står till höger".
        var secrets = JsonSerializer.Deserialize<Secrets>(
            File.ReadAllText(path),
            new JsonSerializerOptions { PropertyNameCaseInsensitive = true })
            ?? throw new InvalidOperationException("secrets.json är tom eller ogiltig.");

        // Hellre stoppa här än få ett kryptiskt 401-fel från Trello senare.
        if (string.IsNullOrWhiteSpace(secrets.ApiKey) || string.IsNullOrWhiteSpace(secrets.Token))
            throw new InvalidOperationException("ApiKey och Token måste vara ifyllda i secrets.json.");

        return secrets;
    }
}
