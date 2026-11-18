# Backlog

## Klart
- [x] Slice 1: Lista kort med ansvarig och status från en board (secrets i gitignorerad JSON, 4 enhetstester)

- [x] Verifierad mot riktiga boarden "Planering av spel" (2026-11-18), 45 spel-tasks skapade i "To Do"

- [x] Pedagogiska kommentarer för CLO26 + utskrift utbruten till TaskTable (en klass = ett ansvar)

- [x] Promptplanner på GitHub Pages: startsida + 3 generatorer (miniprompt, projektplanering, bästa praxis enligt Anthropic). Testad i Node (mallar) och headless Edge (formulär, validering, kopiering, mobilbredd)

- [x] CLO26-kursprompter i promptplannern: förklara uppgift, gör kort (Trello/GitHub), dela upp kort, jag har fastnat (15-minutersregeln), förklara kod, granska uppdelning (SRP/SoC), UML. Ledtrådar som standard. Testad i Node + headless Edge. (2026-11-18)

## Att göra
- [ ] Radera Trello-appen "jsonimport" och generera nya nycklar (de gamla har synts i en chatt)

## Beslut
- Status = namnet på listan kortet ligger i.
- Nycklar skickas i `Authorization`-header, inte i URL, så de inte hamnar i loggar.

## Öppna frågor
- Ska arkiverade kort visas? (Just nu: Trellos standard = bara öppna kort.)

## Idéer (sist i kön)
- Akronym-generatorer för AI-kursen (RTF, CO-STAR, CREATE m.fl., se https://teachandlearnai.com/uncategorized/acronyms-for-ai-prompts/). Återanvänd generator.js. Öppen fråga: eget repo för AI-kursen i stället för detta CLO26-repo?
- Kursprompter för kurs 4–9 när de tilldelas (källa: school/yrgo/clo26/students – det studenterna fått).
