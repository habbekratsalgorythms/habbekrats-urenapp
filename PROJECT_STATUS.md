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
Geslaagd op de volledige bronbestanden, onafhankelijk gedownload op commit 2e50f5f4859b5d00a6621fde7c2398dc2960b606. Acht interne links gecontroleerd; zeven pagina's bevatten taal- en mobiele viewportmetadata. Anonieme SELECT op organizations wordt geweigerd door tabelrechten; deze weigering is de verwachte uitkomst, geen reden om rechten te verruimen.
Aanvullend: authenticated-rol zonder gebruikersidentiteit ziet nul rijen in alle vijf openbare tabellen. Dit vervangt geen test met twee echte gebruikers/bedrijven. Geen browser- of volledige productie-eindtest geclaimd.

## Kosten en publicatie
€0 aankopen/abonnementen/budgetwijzigingen via deze sessie. Bestaande kosten niet onderzocht.
Wijzigingen uitsluitend op codex/five-tracks-2026-11-07, niet op main.
Geen productiegegevens veranderd. Merge naar main kan GitHub Pages publiceren; eerst browser- en accountcontroles afronden.

## Ontbrekende zakelijke inrichting — bevestigd door eigenaar
Er is nog geen KvK-nummer en er zijn nog geen betaalopties aangemaakt. Daarom uitsluitend vrijblijvende pilot-/offerteaanvragen. Geen fictieve KvK-, btw- of betaalgegevens invullen. Zakelijke registratie en betaalproviderverificatie vereisen feitelijke eigenaargegevens en diens identiteits-/bankverificatie; kosten alleen na expliciet akkoord. Geen betaling of aankoop in deze sessie gestart.

## Aanvullend zelfstandig werkblok — 8 november 2026

**Uitgevoerd in de bestaande draft-branch, nog niet op de live hoofdpagina:**

1. **Urenapp** — read-only Supabase-securityreview. De organisaties-SELECT is eigenaargebonden, maar de app heeft al een fallback via het eigen lidmaatschapsrecord; een medewerker ziet mogelijk de generieke naam 'Team'. Geen aangetoonde datalekken en geen bewezen werkende multi-tenant pilot. Uitgebreide test-/releasevoorwaarden in [docs/UREN_RELEASE_SECURITY.md](docs/UREN_RELEASE_SECURITY.md). Geen databasewijziging uitgevoerd.
2. **Offertecalculator** — drie prijs-/margescenario's, huidig tarief versus werkelijke brutomarge, jaarlijkse brutowinst en download van een lokale CSV toegevoegd. Geen opslag of verzending van invoer. Rekentests uitgebreid.
3. **AI-microservices** — [volledig fictief voorbeeldpakket](microservices/voorbeeldpakket.html) van tien inhoudelijk verschillende captions en vijfweekse planning, gekoppeld aan de vrijblijvende briefing.
4. **Klyptiq Gaming** — de lokale Kokoro-videomotor is al op de eigen GitHub-repo opgenomen. Een optionele versie met dynamisch wisselende captions en opvallendere visuals wordt afzonderlijk getest in een featurebranch; **niet gepubliceerd in Metricool**. Merk 7945934 en planning werden in de recente sessie wél live via de beschikbare Metricool-koppeling gecontroleerd: 42 Instagram-publicaties en één video voor elk van TikTok/YouTube gepland voor 8–17 nov. De eerdere vermelding 'Metricool-tools niet beschikbaar' in dit document was een historische beperking en geldt niet meer.
5. **Affiliate / AI-influencer** — [redactiebeleid](affiliate/redactiebeleid.html) met expliciete beoordelingscriteria, disclosure-regels en grenzen voor virtuele presentatoren; nog geen programma, trackinglink of commissionering.

**Verifieerbaar:** GitHub Actions [Five-track prelaunch quality checks](https://github.com/habbekratsalgorythms/habbekrats-urenapp/actions/runs/42426481383) = SUCCESS; controleert JavaScript-interacties, rekenbedragen, lokale CSV, negen HTML-pagina's, interne links en geen bekende private keys in gepubliceerde HTML. De eerdere workflowfout was een vals alarm doordat de controle zijn eigen zoekpatroon vond; dit is gecorrigeerd. **Geen browser-/mobiele handmatige test of echte twee-tenanttest geclaimd.**

**Release blijft NO-GO:** PR #1 blijft draft en main is niet bijgewerkt. Er zijn nog geen geverifieerde zakelijke/betaalgegevens; er zijn geen live betaalstromen, klantmails of Social-posts gestart. Betaalde omzet is niet aangetoond.

**Eigenaar:** voorlopig geen actie nodig voor documentatie en offline code. Vóór betaalde lancering: zakelijke identiteit, voorwaarden, betaalmogelijkheid en expliciete vrijgave; voor urenapp echte testaccounts en verificatie van rollen.
**Jesse:** kanaalprofielen/branding afmaken en bij toekomstige echte posts beeld, geluid en status steekproefsgewijs controleren; geen financiële of codehandelingen vereist.

### Aanvullende browsercontrole (8 november)

De eerder ontbrekende **echte browsercontrole is alsnog uitgevoerd op GitHub Actions** met headless Chromium en Playwright, nadat de lokale browser door beleid werd geblokkeerd. [Run #42427435000](https://github.com/habbekratsalgorythms/habbekrats-urenapp/actions/runs/42427435000) = SUCCESS.

- Desktop 1366×900 en mobiel 390×844: acht website-/productpagina's geopend; geen JavaScript-paginafouten of horizontale overflow gevonden.
- Calculator: voorbeeldbedragen, huidig tarief, actuele marge, CSV-download met UTF-8 BOM en geblokkeerde export bij ongeldige uren getest.
- AI-microservice: briefing aangemaakt en mailto-aanvraag gecontroleerd zonder e-mail te verzenden.
- Affiliate: keuzecheck met gratis budgetoptie gecontroleerd.
- Screenshots en test-CSV's opgeslagen als GitHub-artifact `Habbekrats-browser-review-screens`, veertien dagen beschikbaar.
- Afzonderlijk artifact `Habbekrats-five-track-review-pages` bevat de review-only pagina's, niet de live app.

**Nog niet bewezen:** daadwerkelijke print/PDF-opmaak, productie Supabase-auth met echte medewerkers/tenants, e-mailverificatie, betaalacceptatie, uitgevoerde leveringen en commerciële klanten. PR #1 blijft bewust draft.

## 8 november 2026 — snelle publieke voorlancering & beveiligingstest

- **Publieke marketing-/proefpagina's zijn gepubliceerd** via afzonderlijke laag-risico PR #2: https://github.com/habbekratsalgorythms/habbekrats-urenapp/pull/2 (merged, main `4a8b8b18f6e700aa259ea6891c34c1d3c34e3947`).
- GitHub Pages deploy `42498052184` is **SUCCESS**: https://github.com/habbekratsalgorythms/habbekrats-urenapp/actions/runs/42498052184.
- Nieuw gepubliceerde paden: `/studio/`, `/offertecalculator/`, `/microservices/`, `/microservices/voorbeeldpakket.html`, `/affiliate/`, `/affiliate/redactiebeleid.html`, `/klyptiq/`, `/uren/`. **Geen checkout of persoonsgegevensverzameling toegevoegd.**
- Bevestigde website-QA `42497969706`: Chromium desktop en mobiel, linktest, rekenfunctie, CSV, aanvraagbriefing en geen private keys in HTML = SUCCESS.
- **Supabase READ ONLY tenant-isolatie:** twee bestaande bedrijfs-eigenaren bleken verschillende accounts; in een READ ONLY transactie met tijdelijke rol `authenticated` + hun eigen JWT-sub-claim zag ieder **precies 1 eigen bedrijf, 0 andere bedrijven, 0 buitenlandse urenregistraties**. Wel eigen respectievelijk 1 en 8 urenregistraties zichtbaar. Alle testtransacties beëindigd met ROLLBACK, geen records aangepast. Dit toont alleen eigenaar/eigenaar-isolatie; medewerkersuitnodiging/acceptatie/review en mailverificatie blijven onbewezen.
- Bestaande database-trigger `public.protect_time_entries()` is gecontroleerd: eigenaar/gebruikersidentificatievelden onveranderlijk, goedkeuringsvelden beschermd bij requests als `authenticated`, reeds ingediende/goedgekeurde uren niet direct wijzigbaar. Niet opnieuw gebouwd. Four existing SECDEF RPC warnings en leaked-password-protection setting moeten nog apart worden beoordeeld.
- **Klyptiq release-week:** drie officiële bronverifieerbare scripts en drie 1080p Kokoro-videorenders zijn getest en via afzonderlijke PR #5 geïntegreerd in de Klyptiq-code. Social posts/onbetaalde rechten blijven ongewijzigd.
- **Gmail-leadbewaking**: de gekoppelde zakelijke inbox `habbekratsalgorythms@gmail.com` is bevestigd; nieuwe dagelijkse automatisering `Habbekrats zakelijke aanvragen` aangemaakt, controleert op relevante zakelijke leads en toont uitsluitend echte nieuwe aanvragen, geen automatische replies of betalingen.

**Nog niet geregeld en vereist vóór betaalde verkoop:** keuze bestaande/nieuwe KvK-bedrijfsregistratie, juiste btw-/prijsstelling, formele voorwaarden en betaalprovider; gebruiker heeft prioriteitenlijst gekregen. Urenapp blijft NO-GO voor echte personeelsdata zonder volledige medeweker-/RLS-test. De eerder bestaande concept-PR #1 blijft draft en wordt niet geheel gemerged. Tests ≠ vijf bedrijven met omzet.
