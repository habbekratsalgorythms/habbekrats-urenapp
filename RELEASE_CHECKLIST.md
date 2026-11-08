# Vrijgave en eerstvolgende acties

## Klaar en gecontroleerd
- Urenexport: persoonlijk filter, alle pagina's, blokkering bij laadfout.
- Offertecalculator: lege/ongeldige invoer, juiste referentiebedragen, afdrukstijl.
- AI-content: briefing + mailto, geen automatische opdracht of verzending.
- Klyptiq: samenwerkingspagina, bestaand contactadres, geen onbevestigde statistieken.
- Affiliate: afzonderlijke keuzecheck, geen actieve affiliate-links of fictieve ervaringen.
- node tests/verify.cjs geslaagd op volledige bestanden; acht interne links bestaan.

## Voordat main wordt bijgewerkt
1. Visuele controle mobiel/desktop en afdruk van de calculator.
2. Urenapp: medewerker A, medewerker B en eigenaar in twee bedrijven testen; eigen export vergelijken met databaseaantallen; goedgekeurde registratie moet vergrendeld blijven.
3. Uitnodigen, afwijzen/corrigeren, uitloggen/inloggen en netwerkfout tijdens paginering testen.
4. Productstatus blijft test/voorlancering. Betaalde verkoop vereist geverifieerde zakelijke gegevens, voorwaarden, prijs/btw, levertermijn en betaaloplossing.
5. Geen echte klant- of personeelsgegevens vóór vrijgave.

## Metricool — los van bovenstaande websitewijzigingen
Merk: 7945934. Eerst live kalender, publicatiestatus, accountkoppelingen en contenttaal controleren.
Oude planning niet als live bewijs gebruiken. Geen dubbele posts toevoegen.
De Metricool-koppeling was in een eerdere werksessie niet beschikbaar, maar is nu opnieuw live gecontroleerd. Voor 8–17 november stonden 42 Instagram-posts en één video per TikTok/YouTube gepland; controleer actuele status opnieuw zodra publicaties hebben plaatsgevonden. De bestaande kalender is in dit werkblok ongewijzigd gebleven.
Plaats geen duplicaten of onbeoordeelde testvideo's; verifieer beeldrechten, voice-over, mediaformat en platformstatus voordat nieuwe concepten worden gepubliceerd.

## Afzonderlijke opbrengstmetingen zodra verkoop werkt
1. Urenapp: pilotaanvragen, geactiveerde bedrijven, betalende bedrijven.
2. Calculator: proefgebruik, productverkoop, terugbetalingen.
3. AI-content: aanvragen, offerteacceptatie, uitvoeringstijd en marge.
4. Klyptiq: bereik, kijktijd, relevante volgers en geaccepteerde samenwerkingen.
5. Affiliate: nuttige bezoeken, uitgaande clicks en bevestigde commissies — pas na echte links en passende transparantie.

Geen automatische omzetclaims; geen nieuwe uitgaven of platformaccounts aangemaakt.

## Uitgebreide testresultaten en onafhankelijke release-gates (8 november)
- **Tests en demo:** [laatste groene GitHub Actions-run](https://github.com/habbekratsalgorythms/habbekrats-urenapp/actions/runs/42426931871); offline test van formulier, offertecalculator, CSV, 10-postvoorbeelden, affiliatebeleid en alle lokale links. Testbundel als GitHub Actions artifact beschikbaar zonder live deploy.
- **Urenapp:** voltooi [medewerker-/RLS-acceptatie](docs/UREN_RELEASE_SECURITY.md), echte twee-organisatietest en e-mailverificatie. Geen klantdata zolang dit niet is afgerond.
- **Calculator:** test in echte mobiele browser, de print/CSV-uitvoer en klantacceptatie van het rekenmodel; bepaal contractueel wat 'brutomarge' wel/niet omvat.
- **AI-microservice:** test een volledige offerte-aanvraag, akkoord en [leverproces](microservices/LEVERPROCES.md); doe geen verkooppromises of facturen zonder zakelijke inrichting.
- **Klyptiq:** optionele pop-montage is apart succesvol in de Klyptiq-repository getest; geen automatische posts uit deze code. Nieuw materiaal en rechten blijven een vrijgavevoorwaarde.
- **Affiliate:** zonder goedgekeurde affiliatepartners en gecontroleerde producten geen commerciële links of omzetclaims. Zie [MVP-plan](affiliate/MVP_PLAN.md).
- **Eindbesluit:** alle vijf zijn nog **voorlancering/prototype**. Dit is geen bewijs van vijf volledig operationele bedrijven of inkomsten. De huidige concept-PR niet naar main mergen totdat alle relevante vrijgavecontroles zijn afgerond.
