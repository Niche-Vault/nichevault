# NicheVault Quality Standard
**Last updated:** 2026-06-30

---

## The 100-Record Standard

Every NicheVault lead list must contain a minimum of **100 verified records** before it may be marked "Ready to Upload."

### Why 100?
- Delivers a usable day's worth of cold outreach for a single salesperson
- Large enough to be statistically meaningful (industry sub-segments, geographic spread)
- Small enough to keep per-record verification feasible and quality high

---

## Required Fields (Minimum Viable Record)

Every record MUST contain these 8 fields:

| # | Field | Format | Validation |
|---|-------|--------|------------|
| 1 | **business_name** | Registered company name | Must match Companies House record |
| 2 | **email** | user@domain.com | Extracted from website (not guessed) |
| 3 | **phone** | +44 xxxx xxx xxx | UK phone format, digits verified |
| 4 | **postcode** | SW1A 1AA | Full UK postcode |
| 5 | **website** | https://example.com | Domain must resolve + return 200 |
| 6 | **sic_code** | 5-digit | Must be a valid ONS SIC code |
| 7 | **town** | City/town name | From registered or trading address |
| 8 | **company_number** | Companies House registration | Must be active on CH register |

### Optional (but encouraged) Fields
- incorporation_date
- company_type (ltd, plc, LLP)
- employee_count (from filing data)
- turnover_indicator (micro/small/medium)
- county / region
- industry certification (e.g. MCS, NSI, SSAIB, ISO)

---

## QA Checklist (Pass/Fail)

A list passes QA only when ALL the following are true:

### Quantity Checks
- [ ] 100+ records in the final list
- [ ] No fewer than 100 verified records (raw extraction count may be higher)

### Field Completeness
- [ ] Every record has all 8 required fields populated
- [ ] No empty cells in required fields
- [ ] No placeholder values ("TODO", "N/A", "-", blank string)

### Deduplication
- [ ] No duplicate `business_name` entries (fuzzy match > 90% similarity flagged for review)
- [ ] No duplicate `email` entries
- [ ] No duplicate `company_number` entries

### Data Quality
- [ ] All `email` values match `*@*.*` pattern
- [ ] All `phone` values have 10-11 digits after stripping spaces
- [ ] All `postcode` values match UK postcode regex: `[A-Z]{1,2}[0-9][A-Z0-9]? [0-9][A-Z]{2}`
- [ ] All `website` values start with http:// or https://
- [ ] All `sic_code` values are 5-digit numbers found in ONS SIC classification
- [ ] No records with `DORMANT` or `NO ACCOUNTS FILED` filing status
- [ ] No records with `(DISSOLVED)` or `(LIQUIDATION)` in company name

### Business Verification
- [ ] Every website domain returns HTTP 200 or 30x
- [ ] Every website displays real business content (not parked/placeholder)
- [ ] Company is actively trading (not dissolved, struck-off, or in liquidation)

---

## Failure Thresholds

| Issue | Threshold | Action |
|-------|-----------|--------|
| Missing required fields | Any record | Fail — entire list returned to Data Builder |
| Duplicate entries | Any | Fail — dedup required |
| HTTP 404 / parked domain | >2% of records | Fail — verify remainder |
| Email format invalid | >2% of records | Fail — re-extract emails |
| Below 100 verified records | <100 | Fail — return to Market Scout (insufficient population) |

---

## Pricing & Positioning Guidelines

- **Standard price:** £75 per list
- **Differentiator:** Hand-verified, scraped-free provenance
- **Buyer promise:** "100 verified UK companies in [niche], each checked against Companies House and their own website"
- **Not suitable for:** Lists under 100 records, lists built from automated scraping only, lists without per-company verification

---

## Versioning

- A list "build spec" defines the target (SIC codes, fields, filters)
- Each build produces v1.0, updated quarterly (v1.1, v1.2...)
- Version history recorded in card metadata
-