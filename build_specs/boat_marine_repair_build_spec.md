# Build Spec: UK Boat & Marine Repair Services
**Prepared by:** Data Builder Agent  
**Date:** 2026-06-30  
**Status:** Build spec (no data collected)

---

## 1. Target SIC Codes

| Code | Description | Include/Exclude |
|------|-------------|-----------------|
| **33150** | Repair and maintenance of ships and boats | ✅ **Primary — include all** |
| 30110 | Building of ships and floating structures | ❌ Exclude (shipbuilding, not repair) |
| 30120 | Building of pleasure and sporting boats | ❌ Exclude unless also doing repair work |

**SIC precision rating:** ⭐⭐⭐⭐⭐ (near-perfect — catch all marine repair businesses)

---

## 2. Required Field Schema

| # | Field | Type | Required | Notes |
|---|-------|------|----------|-------|
| 1 | business_name | string | ✅ | Registered company name, cleaned |
| 2 | email | string | ✅ | Sourced from website or verified directory |
| 3 | phone | string | ✅ | UK format: 01xxx xxxxxx or 07xxx xxxxxx |
| 4 | postcode | string | ✅ | Full UK postcode from registered address |
| 5 | website | string | ✅ | Company website (if available) |
| 6 | sic_code | string | ✅ | Primary SIC code (33150) |
| 7 | town | string | ✅ | Town/city from registered address |
| 8 | company_number | string | ✅ | Companies House registration number |
| 9 | company_type | string | No | e.g. ltd, plc, LLP (for filtering) |
| 10 | incorporation_date | date | No | To filter out recently registered |
| 11 | address_line_1 | string | No | Full registered address |
| 12 | county | string | No | For regional segmentation |
| 13 | employee_count | int | No | If available from filing data |
| 14 | turnover_indicator | string | No | Micro/small/medium from filing status |

**Minimum viable record:** 8 required fields (1-8 above)

---

## 3. Name Filters (Exclusion Patterns)

Exclude companies whose registered name contains:

```
- (DISSOLVED)
- (INACTIVE)
- (STRIKE-OFF)
- ADMINISTRATION
- LIQUIDATION
- RECEIVERSHIP
- TRUSTEE IN BANKRUPTCY
- YACHT BROKERAGE (not repair)
- MARINE SURVEYOR (unless also doing repair)
- CHARTER (charter companies, not repair)
```

Exclude companies with filing status: *dissolved*, *liquidation*, *administration*

**Keyword confidence filter (include only if):**
```
Contains: REPAIR, MAINTENANCE, MARINE ENGINEERING, BOATYARD, MARINA SERVICE, 
          SHIP REPAIR, DOCKYARD, DRY DOCK, MOORING SERVICES, 
          YACHT SERVICES, BOAT SERVICES
OR SIC code = 33150 (the primary code is already highly specific)
```

---

## 4. Cleaning Rules

| Rule | Action |
|------|--------|
| **Duplicate business_name** | Keep record with most complete data; flag for manual review |
| **Email format** | Must match `*@*.*` pattern. Reject addresses with spaces |
| **Phone format** | Normalise to `+44 xxxx xxx xxx`. Strip non-numeric characters |
| **Postcode validation** | Must match UK postcode regex: `[A-Z]{1,2}[0-9][A-Z0-9]? [0-9][A-Z]{2}` |
| **Turnover filter** | Remove companies with `DORMANT` filing status or `NO ACCOUNTS FILED` |
| **Incorporation date** | Exclude companies registered < 6 months ago (high risk of being shell/paper companies) |
| **Website check** | Remove entries where domain returns 404 or parked page |

---

## 5. Collection Strategy

### Phase 1 — Companies House Bulk Extraction
- Query SIC 33150 via Companies House API
- Filter: active status, not dissolved, not dormant
- Export: company_number, business_name, registered address, incorporation_date, filing_status
- Expected yield: ~400-600 active (from 800+ total, ~20% dormant/closed)

### Phase 2 — Website & Contact Discovery
For the top 400 active companies:
1. Visit each company website (or search if no website on file)
2. Extract email from mailto: links (`document.querySelectorAll('a[href^="mailto:"]')`)
3. Find phone number in footer or contact page
4. Confirm the company actually does marine repair (not just owns a boat)

### Phase 3 — Verification
- Verify 100+ of the best contacts
- Remove any that are: charter-only, brokerage-only, survey-only
- Confirm phone number works and email is correct
- Final list: 100 verified records

### Recommended Data Sources
| Source | Priority | Details |
|--------|----------|---------|
| Companies House API | Primary | Free API, bulk SIC query, company status |
| Company websites | Secondary | Email/phone extraction per domain |
| SIC 33150 directories | Supplementary | Marine industry directories (BYA, British Marine) |
| Google Maps | Supplementary | "Marine repair near me" for coastally-focused businesses |

---

## 6. Estimated Timeline & Effort

| Step | Effort | Notes |
|------|--------|-------|
| Companies House query | 30 min | API extraction + filtering |
| Website research (400 companies) | 20-30 hours | ~3-4 min per company |
| Email verification | 5 hours | Confirm emails are valid |
| Final QA & dedup | 2 hours | Cross-check 100 records |
| **Total** | **~30-35 hours** | Can parallelise with a helper |

---

## 7. Pricing & Positioning Notes

- **Unique angle:** Coastal/underserved — most data vendors focus on London-centric industries
- **Target buyer:** Marine equipment suppliers (engine parts, electronics, paints), tool distributors, insurance brokers
- **Differentiator:** Hand-verified, no generic scraped data. Each record checked against the actual business
- **Competition check:** No Gumroad/Apollo list found for SIC 33150 specifically. Clean field.
