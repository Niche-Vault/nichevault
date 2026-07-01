# Build Spec: Industrial Valve Manufacturers UK
**Prepared by:** Data Builder Agent  
**Date:** 2026-06-30  
**Status:** Build spec (no data collected)

---

## 1. Target SIC Codes

| Code | Description | Include/Exclude |
|------|-------------|-----------------|
| **28120** | Manufacture of taps and valves | ✅ **Primary — include all** |
| 28291 | Manufacture of other general-purpose machinery | ❌ Exclude (too broad — only include if keyword "valve" matches) |

**SIC precision rating:** ⭐⭐⭐⭐⭐ (SIC 28120 is purpose-built for valve manufacturers)

**Note:** SIC 28120 is *extremely* precise — it specifically covers industrial valve, tap, and pneumatic/hydraulic valve manufacturing. No secondary codes needed. This gives the cleanest possible Companies House query.

---

## 2. Required Field Schema

| # | Field | Type | Required | Notes |
|---|-------|------|----------|-------|
| 1 | business_name | string | ✅ | Registered company name, cleaned |
| 2 | email | string | ✅ | Sourced from website or verified directory |
| 3 | phone | string | ✅ | UK format: 01xxx xxxxxx or 07xxx xxxxxx |
| 4 | postcode | string | ✅ | Full UK postcode from registered address |
| 5 | website | string | ✅ | Company website (if available) |
| 6 | sic_code | string | ✅ | Primary SIC code (28120) |
| 7 | town | string | ✅ | Town/city from registered address |
| 8 | company_number | string | ✅ | Companies House registration number |
| 9 | company_type | string | No | e.g. ltd, plc, LLP |
| 10 | incorporation_date | date | No | For filtering out recently registered |
| 11 | address_line_1 | string | No | Full registered address |
| 12 | county | string | No | For regional segmentation |
| 13 | employee_count | int | No | From filing data if available |
| 14 | turnover_indicator | string | No | Micro/small/medium/large |

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
- PLUMBING MERCHANT (valve distributors ≠ manufacturers)
```

Exclude companies with filing status: *dissolved*, *liquidation*, *administration*

**Secondary filter (quality assurance):**
```
Prefer companies whose name or description contains:
  VALVE, VALVES, VALVING, MANUFACTURING, ENGINEERING, 
  FLUID CONTROL, PNEUMATIC, HYDRAULIC, ACTUATOR, 
  PROCESS EQUIPMENT, INDUSTRIAL VALVE
```

**Disqualifiers:**
```  
  RETAIL, DISTRIBUTION ONLY, WHOLESALE ONLY, IMPORTER ONLY
(We want manufacturers and specialist suppliers, not general merchants)
```

---

## 4. Cleaning Rules

| Rule | Action |
|------|--------|
| **Duplicate business_name** | Keep record with most complete data; remove exact name duplicates |
| **Email format** | Must match `*@*.*` pattern. Reject addresses with spaces or missing @ |
| **Phone format** | Normalise to `+44 xxxx xxx xxx`. Strip non-numeric characters |
| **Postcode validation** | Must match UK postcode regex |
| **Turnover filter** | Remove companies with `DORMANT` filing status or `NO ACCOUNTS FILED` |
| **Incorporation date** | Exclude companies registered < 6 months ago (shell/paper risk) |
| **Website check** | Remove if domain returns 404, parked page, or redirects to non-relevant site |
| **SIC secondary check** | Any company with SIC 28120 but whose description suggests retail-only: flag for manual review |

---

## 5. Collection Strategy

### Phase 1 — Companies House Bulk Extraction
- Query SIC 28120 via Companies House API
- Filter: active status, not dissolved, not dormant
- Export: company_number, business_name, registered address, incorporation_date, filing_status
- Expected yield: ~700-900 active (from 1,200+ total)

### Phase 2 — Website & Contact Discovery
For the top 700 active companies:
1. Visit each company website (or search if no website on file)
2. Extract email from mailto: links on the site
3. Find phone number in footer or contact page
4. Confirm they manufacture or supply industrial valves (not just plumbing fittings)

### Phase 3 — Verification & Refinement
- Filter to 100 best contacts
- Prioritise full Ltd companies (not sole traders) with active websites
- Confirm SIC 28120 is accurate — flag any that are actually plumbing merchants
- Final list: 100 verified records

### Recommended Data Sources

| Source | Priority | Details |
|--------|----------|---------|
| Companies House API | Primary | Free API, SIC 28120 is purpose-built |
| Company websites | Secondary | Email/phone extraction |
| British Valve & Actuator Association (BVAA) | Supplementary | Industry body member directory |
| Industry exhibitions (Valve World Expo) | Supplementary | Exhibitor lists for validation |

---

## 6. Estimated Timeline & Effort

| Step | Effort | Notes |
|------|--------|-------|
| Companies House query | 30 min | Single-precision SIC, fast extraction |
| Website research (400 companies) | 15-20 hours | ~2-3 min per company (better websites) |
| Email verification | 4 hours | Confirm emails, remove non-manufacturers |
| Final QA & dedup | 2 hours | 100 records |
| **Total** | **~22-27 hours** | Faster than marine — cleaner SIC |

---

## 7. Pricing & Positioning Notes

- **Unique angle:** Highly specialised — no general "manufacturing" list. Buyers get pre-filtered valve industry contacts.
- **Target buyer:** Industrial equipment distributors (pumps, seals, gaskets, piping), raw materials suppliers (steel, brass, alloys), B2B software vendors (ERP for manufacturing), trade magazine advertisers.
- **Differentiator:** SIC 28120 gives near-zero noise. Buyer gets actual valve manufacturers, not a "likely manufacturing" guess.
- **Competition check:** No UK-specific valve manufacturers list found on Gumroad/Apollo. Clean field.
- **Geographic note:** Valve manufacturing in the UK is concentrated in the Midlands (Birmingham, Wolverhampton, Coventry, Leicester) and the North West (Manchester, Bolton, Blackburn). Marketing copy should mention this industrial heartland focus.
