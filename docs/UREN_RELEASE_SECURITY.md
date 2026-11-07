# Urenapp — vrijgaveblokkades en meergebruikertest (8 november 2026)

**Status:** NO-GO voor betalende klanten en echte personeelsgegevens. Dit document is een reviewplan, geen uitgevoerde productiemigratie.

## Vastgestelde technische uitgangspunten

- Supabase-project `tgpvissgdojcqgagyfpw` is actief, Postgres 17; RLS staat aan op de vijf tabellen in `public`.
- De app haalt `organizations` op via een SELECT met `limit(1)` in `refresh()` en heeft die organisatie nodig voor medewerkerfuncties.
- De aanwezige policy `org_owner_read` laat alleen records lezen met `owner_id = auth.uid()`.
- **Waarschijnlijke functionele blokkade:** een uitgenodigde medewerker die geen eigenaar is kan na aanmelden zijn organisatie niet via deze SELECT ophalen. Dit is op basis van code en policies vastgesteld; het is nog niet met twee echte gebruikers geverifieerd.
- Er staan momenteel nul regels in `public.organization_members`. Een werkelijke werkgever/medewerker-beveiligingstest is dus nog niet uitgevoerd.
- `get_pending_time_reviews` retourneert maximaal 500 ingediende uren; de UI moet paginering of een bewust begrensde weergave aanbieden voordat grote teams worden ondersteund.
- Vier public RPC's zijn bewust `SECURITY DEFINER` met lege `search_path` en zichtbare controle op `auth.uid()` en eigenaar/admin. Supabase signaleert deze alsnog terecht ter handmatige review. Vermijd het uitschakelen van die waarschuwingen zonder onderzoek.
- De beveiligingsadviseur meldt dat leaked-password protection uitgeschakeld is. Inschakelen en bevestigen vereist dashboardbevoegdheden; niet stilzwijgend aangepast.
- De uitnodigingstabel in `private` is niet aan de Data API blootgesteld, heeft RLS aan en geen RLS-policy; dat is niet automatisch een lek.

## Voorstel voor veilige oplossing — eerst in een testomgeving

Maak een minimaal geprivilegieerde manier om een ingelogde medewerker alleen de organisaties te laten ophalen waarvan hij lid is. **Voeg niet zomaar een policy toe die onderling via `organizations` en `organization_members` verwijst.** Omdat de bestaande policies in de andere richting verwijzen, kan dat RLS-recursie veroorzaken. Toets een kleine, geïsoleerde `SECURITY DEFINER`-helper in een niet-blootgestelde schema of een andere gecontroleerde architectuur, inclusief expliciete EXECUTE-rechten. De helper moet altijd aan `auth.uid()` gebonden zijn, de `search_path` vastzetten en nooit gegevens van andere tenants teruggeven. Een nieuw publieke RPC of generiek `TO authenticated`-beleid zonder eigendomsfilter is niet acceptabel.

## Echte end-to-end testmatrix (minimaal drie accounts, twee fictieve bedrijven)

1. Eigenaar A maakt een testorganisatie en een testklant. Eigenaar B maakt een tweede organisatie.
2. Medewerker A accepteert éénmalig een verlopen-niet uitnodigingstoken van A en ziet uitsluitend bedrijf A.
3. Medewerker A kan een concept aanmaken, wijzigen, indienen en afgewezen uren corrigeren, nooit goedgekeurde uren aanpassen of verwijderen.
4. Eigenaar A ziet ingediende uren van medewerkers van A, kan goedkeuren of afwijzen, en kan geen gegevens van B opvragen via de API.
5. Eigenaar B ziet nooit klanten, uren, e-mails, uitnodigingen of auditlogs van A.
6. Externe gebruiker en anonieme bezoeker zien geen privégegevens; pogingen om `organization_id` of `user_id` in requests te wisselen worden geweigerd.
7. Test races: werknemer wijzigt tegelijk met de review, twee beheerders beoordelen dezelfde regel, verlopen of hergebruikte token, browser offline en gefaalde pagina 2.
8. Genereer 501 ingediende regels voor A om te verifiëren dat de reviewlijst geen records onzichtbaar achterlaat.
9. Vergelijk persoonlijke CSV en maandtotalen met ruwe databaseaantallen voor 0, 1, 500, 501 en 1001 regels.
10. Test mobiel, toetsenbordnavigatie, wachtwoordherstel, uitnodigingsmail, sessieverval en uitloggen. Sla geen echte klantdata op voordat dit is geslaagd.

**Acceptatie:** alleen na gedocumenteerde succesvolle tests, beoordeling van de vier SECURITY DEFINER-RPC's, herstel van medewerkerszichtbaarheid en bevestiging van noodzakelijke privacy-/dienstvoorwaarden. Tot die tijd blijft de gebruikersapp test-only.

## Scope en kosten

Dit document wijzigt de bestaande database of Auth-configuratie niet. Er is geen migratie toegepast, geen testgebruiker aangemaakt, geen service-role-key opgevraagd en geen betaalprovider gebruikt.

Supabase-documentatie: https://supabase.com/docs/guides/database/postgres/row-level-security
Beveiligingsadviseur: https://supabase.com/dashboard/project/tgpvissgdojcqgagyfpw/advisors/security
