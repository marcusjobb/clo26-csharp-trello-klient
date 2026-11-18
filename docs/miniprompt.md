# Miniprompt: dela upp ett projekt i uppgifter

## 1. Beskriv projektet med tre rader

| Rad | Svara på |
|---|---|
| **Vad appen gör** | En mening: vad gör appen, och för vem? |
| **Klart när** | Vad kan användaren göra när appen är färdig? Konkret och kontrollerbart. |
| **Delar** | Vilka delar består appen av? (sidor, klasser, databas, API …) |

## 2. Prompten – fyll i och klistra in till AI:n

```text
Jag ska bygga ett projekt och vill ha hjälp att dela upp det i uppgifter.

Vad appen gör: [en mening]
Klart när: [vad användaren kan göra när appen är färdig]
Delar: [appens delar]

Dela upp projektet i små uppgifter som var och en tar högst 30 minuter.
Sätt dem i den ordning de bör göras och ge en grov tidsåtgång per uppgift.
Svara med en tabell: Nr | Uppgift | Tid.
Jag är nybörjare i [språk/teknik], så håll uppgifterna små och konkreta.
```

## 3. Granska förslaget – innan du använder det

Gå igenom tabellen rad för rad:

- [ ] **Kan jag förklara uppgiften med egna ord?** Säg den högt eller skriv en mening. Går det inte → **ta bort den** (eller fråga läraren vad den betyder).
- [ ] **Är den för stor?** Tar den mer än en timme, eller innehåller den flera "och" → **skriv om den** till två eller fler mindre uppgifter.
- [ ] **Är ordningen rimlig?** Kan jag göra uppgift 5 utan att 1–4 är klara?
- [ ] **Leder den mot "klart när"?** Uppgifter som inte hjälper till att uppfylla den raden kan vänta.

Det är **din** lista när du är klar – inte AI:ns.

---

Ifyllt exempel: [miniprompt-labyrintspel.md](miniprompt-labyrintspel.md)
