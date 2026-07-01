# Data Builder Spec: UK Boat & Marine Repair Services
**Prepared by:** Data Builder Agent  
**Date:** 2026-07-01  
**Status:** Build spec (no data collected yet)

---

## SIC Code(s) to Target

| Code | Description | Include/Exclude | Notes |
|------|-------------|-----------------|-------|
| **33150** | Repair and maintenance of ships and boats | ✅ **Primary — include all** | One of the most precise SICs in the ONS register. Captures boatyards, marine engineering workshops, yacht repair, and commercial ship repair. |
| 30110 | Building of ships and floating structures | ❌ Exclude | Shipbuilding only — different industry, different buyers |
| 30120 | Building of pleasure and sporting boats | ❌ Exclude | Boat builders — exclude unless also doing repair work |

**SIC precision rating:** ⭐⭐⭐⭐⭐ (near-perfect)

---

## Field Schema

| # | Field | Type | Description |
|---|-------|------|-------------|
| 1 | **business_name** | string | Registered company name from Companies House |
| 2 | **company_number** | string | Companies House registration number |
| 3 | **email** | string | Business email found on company website |
| 4 | **phone** | string | UK landline or mobile (for business, not personal) |
| 5 | **website** | string | Company website URL |
| 6 | **sic_code** | string | Primary SIC code (33150) |
| 7 | **postcode** | string | Full UK postcode from registered address |
| 8 | **town** | string | Town/city from registered address |
| 9 | incorporated | date | Company incorporation date |
| 10 | company_type | string | ltd, plc, LLP, etc. |
| 11 | address_line_1 | string | Full registered address line 1 |
| 12 | county | string | County from registered address |
| 13 | filing_status | string | Active, Dormant, Liquidation, etc. |
| 14 | employee_count | int | From latest filing (if available) |

---

## Name Filters

### Exclude (reject records matching these patterns)
- `(DISSOLVED)`, `(INACTIVE)`, `(STRIKE-OFF)`
- `ADMINISTRATION`, `LIQUIDATION`, `RECEIVERSHIP`, `TRUSTEE IN BANKRUPTCY`
- `YACHT BROKERAGE` — brokers are selling, not repairing
- `MARINE SURVEYOR` — surveyors inspect but don't repair
- `CHARTER` — charter companies operate boats, don't fix them

### Include (prefer records matching these signals)
- Company description or name contains: `REPAIR`, `MAINTENANCE`, `MARINE ENGINEERING`, `BOATYARD`, `MARINA SERVICE`, `SHIP REPAIR`, `DOCKYARD`, `DRY DOCK`, `YACHT SERVICES`, `BOAT SERVICES`

### Filing Status Filter
- Include only: `Active`
- Exclude: `Dormant`, `Liquidation`, `Dissolved`, `Administration`, `Registered prior to liquidation`

---

## Cleaning Rules

| Rule | Action |
|------|--------|
| **Email format** | Must match `*@*.*` with no spaces. Remove records with malformed emails |
| **Phone format** | Normalise to `+44 xxxx xxx xxx`. Strip spaces, dashes, brackets |
| **Postcode validation** | Match regex `[A-Z]{1,2}[0-9][A-Z0-9]? [0-9][A-Z]{2}` |
| **Dedup by company_number** | Keep record with the most filled fields |
| **Dedup by business_name** | Fuzzy match >90% similarity → review manually |
| **Dormant removal** | Remove records with `Dormant` filing status |
| **Young company removal** | Remove records with incorporation date < 6 months ago (shell risk) |
| **Website check** | Remove if domain returns HTTP 404 or parked landing page |

---

## Collection Strategy

### Phase 1 — Companies House API Query
```
GET https://api.company-information.service.gov.uk/advanced-search/companies
Params:
  sic_codes: 33150
  company_status: active
  company_type: ltd,plc,llp
  size: 100 (paginated)
```
Expected raw yield: ~800 total, ~600 active after filtering filing_status

### Phase 2 — Website Discovery
For each active company:
1. Look up website from CH filing data or Google search
2. Visit the website, navigate to Contact page
3. Extract email via `document.querySelectorAll('a[href^="mailto:"]')`
4. Extract phone from footer or contact page
5. Confirm the company actually does marine repair (check services page)

Expected contact discovery yield: ~300 with email found

### Phase 3 — Final Clean & Filter
- Apply all cleaning rules from section 4
- Manual review of borderline cases
- Verify minimum 100 clean records
- Flag any companies that appear to be non-repair marine businesses

Target final yield: **100 verified records**

---

## Data Quality Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Small total population** | ~800 total active, ~600 after dormancy filter — tight margin above 100 target | Include some sole traders if needed, or expand to adjacent SIC codes with keyword filtering |
| **Seasonal/part-time businesses** | Some marine repair businesses are seasonal and may have dormant filing status | Check website for current trading activity before excluding |
| **Coastal concentration** | Heavy South & South West bias. Northern and inland marine repair is scarce | Note geographic limitation in product description |
| **No phone/email on many sites** | Small family-run yards often don't list email | Try contact forms as fallback; note in list if email not found |
| **Outdated CH filing data** | Some active companies haven't filed accounts in 2+ years | Cross-reference with website last-updated date |

---

## Estimated Effort

| Step | Effort | Notes |
|------|--------|-------|
| Companies House query + cleanup | 45 min | Small SIC, fast extraction |
| Website research (350 companies) | 15-18h | Many small sites, some hard to find |
| Email/phone extraction | 5h | |
| Final verification & dedup | 2h | |
| **Total** | **~23-26h** | |
