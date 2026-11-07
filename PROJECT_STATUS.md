# HabbekratsAlgorythms — vijf afzonderlijke sporen
Bijgewerkt: 7 november 2026. Dit overzicht meldt uitgevoerd werk, geen bewezen omzet.

## 1. Urenregistratie
- Bestaande app + Supabase-project tgpvissgdojcqgagyfpw geïnspecteerd.
- Persoonlijke lijst en export expliciet op gebruiker gefilterd; pagina's van 500 geladen in plaats van afkappen op 100. CSV geblokkeerd bij laadfout.
- Uitleg en pilotaanvraag op /uren/. Geen actieve betaalabonnementen.
- RLS staat op alle vijf openbare tabellen aan. Vier SECURITY DEFINER-functies controleren login en rol/eigendom en gebruiken een lege search_path.
- Nog nodig: test met meerdere accounts (tenantisolatie, rollen, uitnodigingen, vergrendeling), SMTP, wachtwoordherstel, zakelijke/betaal- en privacyvoorwaarden.
- Beveiligingsadviseur: gelekte-wachtwoordcontrole uit; vier verhoogde functies als waarschuwing; private uitnodigingstabel zonder beleid is afgesloten, niet vrij open. Geen productie-DDL uitgevoerd.

## 2. Offertecalculator
- Lege invoer en ongeldige grenzen afgewezen; printknop geblokkeerd bij ongeldige invoer.
- Invoerlabels gekoppeld, afdrukstijl toegevoegd.
- Rekencontrole: 2 uur × €24 + €1,95 + €2 = €51,95 kosten; 25% marge => €69,27 excl., €83,81 incl. bij ingevoerde 21%.
- Gratis testversie, geen betaald downloadproduct of levering actief.
- Nog nodig: browsercontrole mobiel/print, productverpakking en definitieve prijs/voorwaarden.

## 3. AI-microservices
- /microservices/: voorbeeld, afgebakend aanbod, briefinggenerator en expliciete mailto-offerteaanvraag.
- Tien captions, planning, één correctieronde; €79 richtprijs uit bestaand aanbod, btw/totaalprijs eerst via offerte.
- Generator maakt alleen een briefing; geen AI-API aangeroepen, geen automatische levering, geen contact verzonden.
- Nog nodig: definitieve levertermijn/voorwaarden, betaalwijze en uitvoeringstest op een goedgekeurde opdracht.

## 4. Klyptiq Gaming
- /klyptiq/: aparte zakelijke contactpagina met bestaande Gmail, samenwerkingsintake en transparantie over vergoeding.
- Metricool merk 7945934: plugin staat ingeschakeld volgens pluginregister, maar geen Metricool-functies aan deze sessie geleverd. Browser start niet door lokale uitvoeringsfout.
- Oude chat vermeldt 32 geplande Instagram-posts t/m 15 november; niet live geverifieerd.
- Geen nieuwe posts ingepland, geen bereikcijfers verzonnen. Eerst live kalender en publicatiestatus controleren; geen duplicaten maken.
- Bestaande relevante link: https://app.metricool.com/planner/calendar?blogId=7945934

## 5. Affiliate / AI-influencer
- /affiliate/: zelfstandig prototype met interactieve keuzecheck voor taak, datagevoeligheid en budget.
- Geen affiliate-links, tracking, commissie- of ervaringsclaims. Geen producten gerangschikt zonder onderzoek.
- Nog nodig: naam/persona kiezen, actuele primaire productbronnen onderzoeken en geschikte affiliatevoorwaarden controleren; geen lidmaatschappen afsluiten zonder toestemming.

## Validatie
Run `node tests/verify.cjs` met Node.js. Geen externe packages vereist.
Controleert script-syntax, calculatorreferentie, ongeldige invoer, briefing/mailto, affiliatecheck en een urenlijst van 1001 regels over drie pagina's.
Getest met tijdelijke programmastukken in deze sessie; volledige broncontrole volgt na opslag.
Geen browser-, authenticatie- of productie-eindtest geclaimd.

## Kosten en publicatie
€0 aankopen/abonnementen/budgetwijzigingen via deze sessie. Bestaande kosten niet onderzocht.
Wijzigingen uitsluitend op codex/five-tracks-2026-11-07, niet op main.
Geen productiegegevens veranderd. Merge naar main kan GitHub Pages publiceren; eerst browser- en accountcontroles afronden.
