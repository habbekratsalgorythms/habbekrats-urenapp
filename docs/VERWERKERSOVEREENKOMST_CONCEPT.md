# CONCEPT verwerkersovereenkomst (AVG art. 28) — Habbekrats Uren
**STATUS: DRAFT / NIET ONDERTEKENEN ZONDER RECHTSPERSOON, TECHNISCHE CONTROLE EN JURIDISCHE REVIEW.**

## Partijen
**Verwerkingsverantwoordelijke:** [naam en vestigingsadres werkgever/klant], vertegenwoordigd door [naam].
**Verwerker:** [juridische handelsnaam, vestigingsadres, KvK-nummer HabbekratsAlgorythms of gekozen onderneming], vertegenwoordigd door [naam].
**Hoofdovereenkomst en ingangsdatum:** [invullen na de pilot].

Deze overeenkomst is bedoeld voor uitsluitend in opdracht van de werkgever uitgevoerde SaaS-urenregistraties; persoonsgegevens die de aanbieder voor eigen zakelijke administratie verwerkt vallen onder diens eigen privacyverklaring.

## Onderwerp en duur
De verwerker biedt een gehoste urenregistratiedienst aan gedurende de looptijd van de hoofdovereenkomst. Na het einde gelden het afgesproken export-, verwijderings- en back-upbeleid: **[concreet vaststellen]**.

## Verwerkingsdoel, categorieën en betrokkenen
- **Doel:** uren, pauzes, manuren, opdrachtgevers, accordering, correctie en auditsporen registreren en aan de betreffende werkgever beschikbaar stellen.
- **Betrokkenen:** medewerkers van de klant, beheerders/eigenaren en voor zover noodzakelijk contactpersonen van klantbedrijven.
- **Gegevens:** accountnaam/e-mail, organisatie- en klantidentificatie, datums en tijden, aantal personen, pauzes, status, autorisatie/auditregistraties, beperkte notities.
- **Geen bedoeld gebruik:** medische informatie, bijzondere persoonsgegevens, betalingskaartgegevens, beleidsmatige geautomatiseerde personeelsbeoordelingen. Verantwoordelijke instrueert gebruikers zulke gegevens niet in vrije notitievelden te zetten.

## Verplichtingen verwerker
1. Verwerkt persoonsgegevens uitsluitend op gedocumenteerde instructie van de verantwoordelijke, tenzij een wettelijke plicht anders voorschrijft, en meldt die plicht indien toegestaan.
2. Legt geheimhouding op aan iedere persoon die toegang heeft.
3. Biedt passende organisatorische en technische maatregelen: toegang per tenant, sterke authenticatie, veilige secretopslag, herstel-/back-up- en incidentprocedures, periodieke herbeoordeling. Exacte maatregelen en meetbare garanties: **[beveiligingsbijlage vaststellen]**.
4. Ondersteunt, voor zover redelijk en contractueel vastgelegd, inzage-/correctie-/verwijderingsverzoeken, DPIA's en incidentbeoordeling.
5. Meldt een (vermoedelijk) datalek onverwijld na ontdekking conform een afgesproken incidentproces; tijdslimiet, contact en escalatie: **[afspreken]**.
6. Documenteert relevante beveiligingsmaatregelen en verleent medewerking aan redelijke audits onder waarborgen voor andere klanten.
7. Geeft geen toegang aan andere klanten/tenants; toegangsrechten blijven beperkt tot aantoonbaar gemachtigde medewerkers en beheerders.
8. Verwijdert of retourneert klantgegevens na contractbeëindiging volgens het bevestigde bewaarschema, behoudens wettelijke bewaarplicht, inclusief behandeling van back-ups.

## Subverwerkers en internationale doorgiften
Bekende technische dienst: **Supabase** voor Postgres-database/authenticatie, projectregio `eu-central-1` (feitelijke gegevensopslag, back-upplaats, subverwerkers en internationale verwerkingen contractueel verifiëren). Hosting/monitoring/e-mailleveranciers en betaalprovider moeten apart in een actuele subverwerkersbijlage worden opgenomen.

De verwerker schakelt nieuwe subverwerkers alleen volgens een schriftelijk goedgekeurde algemene of specifieke toestemming in; bij een algemene toestemming hoort een procedure om wijzigingen vooraf te melden en bezwaar mogelijk te maken.

## Instructie, wijziging en aansprakelijkheid
De klant is verantwoordelijk voor de rechtmatigheid en noodzakelijkheid van de ingevoerde personeelsgegevens, toegangstoekenning en bewaarplichten. Verwerker meldt instructies die naar zijn mening in strijd met AVG-verplichtingen zijn. Verdeling van kosten, schade, aansprakelijkheid en auditwerkzaamheden: **[in de hoofd-/voorwaardenovereenkomst uitwerken]**.

## Veiligheidsbijlage — nog in te vullen
- [ ] Echte multi-tenant en medewerker-RLS tests met twee werkgevers en meerdere accounts afgerond.
- [ ] Data-export, veilige account-/tenantverwijdering en audit opgeleverd.
- [ ] Back-up-, recovery-, logretentie- en datalekprocedure vastgesteld en getest.
- [ ] Verwerkersovereenkomst en bijlagen bij de betrokken subverwerkers geverifieerd.
- [ ] Security-definer functies en toegangsrechten geaudit.
- [ ] SSO/MFA/wachtwoordbeleid en SMTP-beveiliging beoordeeld.
- [ ] Bevoegde partijen en contractuele contactpersonen ingevuld.

**Juridische bron:** https://autoriteitpersoonsgegevens.nl/themas/basis-avg/avg-algemeen/verwerkersovereenkomst

Dit document geeft geen daadwerkelijke rechten of live toestemming zolang het niet definitief is goedgekeurd en ondertekend.
