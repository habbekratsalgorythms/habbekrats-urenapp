# 10-caption production and delivery — €79 excl. btw

Definitieve opdrachtvoorwaarden: maximaal 5 werkdagen na **complete briefing en schriftelijke opdrachtbevestiging**; 2 gebundelde correctierondes binnen oorspronkelijke briefing; wijzigingsverzoek binnen 5 werkdagen na de eerste levering.

**Doel:** herhaalbaar werk zonder klantdata naar willekeurige tools te verzenden en zonder geld of publicatie automatisch te starten.

## Praktisch productieproces

1. Beoordeel binnenkomende mail: alleen echte zakelijke leads; stuur nooit onverwacht automatisch een factuur of betaallink.
2. Leg een orderreferentie vast buiten de publieke repo; bewaar echte klantgegevens alleen in een daartoe toegestane beveiligde administratie. Vul nooit klantgegevens in GitHub-issues of openbare JSON-bestanden.
3. Maak een factchecklijst van het aanbod, de doelgroep, beweringen, bronlinks, eventuele actievoorwaarden en de gewenste CTA. Onbevestigde feiten worden niet als vastgesteld gepubliceerd.
4. Maak een matrix met tien verschillende invalshoeken: probleem, tip, mini-checklist, FAQ, misverstand, dienstuitleg, praktisch scenario, klantvraag zonder fictief citaat, seizoensmoment, relevante CTA.
5. Stel originele captions op met AI-assistentie waar toegestaan. Variatie en feitelijke onderbouwing zijn belangrijker dan het aantal AI-aanroepen.
6. Menselijke redactionele controle: spelling, toon, transparantie, juridische/medische/financiële claims, eventuele prijzen/aanbiedingen, locatie, links, dubbele teksten en gevoelige gegevens.
7. Vul een **lokale** JSON in volgens het fictieve `voorbeeldpakket.json` (alleen als structuur). Zet `briefing_complete`, `order_confirmed` en `human_editor_reviewed` pas waarheidsgetrouw op `true`; laatste waarde betekent geen automatische factcheck, alleen dat een redacteur de inhoud heeft gecontroleerd.
8. Draai in een lokale Python 3.10+ omgeving: `python3 microservices/content_pack.py /VEILIG/PAD/order.json --out /VEILIG/PAD/levering`. De tool weigert onvolledige/ongecontroleerde opdrachten, ontbrekende/gelijke captions en placeholders. Er worden twee bestanden gemaakt: CSV (met Excel-compatibele UTF-8 BOM) en leesbare TXT.
9. Controleer die bestanden en voeg eventueel handmatig een nette PDF toe; laat de klant vóór publicatie nog gemarkeerde feitclaims bevestigen.
10. Lever buiten de publieke GitHub-repository via het afgesproken beveiligde kanaal. Registreer datum eerste oplevering; ontvang maximaal twee gebundelde correctierondes aangevraagd binnen vijf werkdagen. Controleer opnieuw en lever bijgewerkte bestanden.
11. Sluit af zonder accounts te beheren of social posts automatisch te plaatsen. Aanvullende content of nieuwe strategie is offertewerk.

## Belangrijk: wat de tool wel/niet doet
- **Wel:** controle van het aantalslot (10), postnummers, ingevulde platforms/plandata, unieke captions, redactiegate en uitvoerformaten.
- **Niet:** waarheidsgehalte van feitclaims automatisch bewijzen, teksten voor een specifieke klant bedenken, klantgoedkeuring simuleren, foto's ontwerpen, rechtsgeldig klantenbeheer, e-mail automatisch verzenden, betalingen verwerken of Instagram publiceren.
- **Niet:** beschouwen van de voorbeeld-JSON als een betaalde bestelling. De demo blijft standaard op `human_editor_reviewed: false` en wordt daarom niet geëxporteerd.

## Eerste echte proefopdracht
Gebruik uitsluitend fictieve bedrijfsdata, bijvoorbeeld de bestaande fictieve fietsenmaker. Kopieer lokaal de demo-JSON; simuleer dat de redacteur alles heeft beoordeeld door in een testkopie `human_editor_reviewed: true` te zetten. Draai de CLI, open de tien CSV-rijen en lees de TXT. Voer vóór echte verkoop de fiscale, privacy- en opdrachtvoorwaardencontrole uit.

Test de code: `python3 -m unittest discover -s microservices/tests -v`.
