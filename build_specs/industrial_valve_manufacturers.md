# Data Builder Spec: Industrial Valve Manufacturers UK
**Prepared by:** Data Builder Agent  
**Date:** 2026-07-01  
**Status:** Build spec (no data collected yet)

---

## SIC Code(s) to Target

| Code | Description | Include/Exclude | Notes |
|------|-------------|-----------------|-------|
| **28120** | Manufacture of taps and valves | ✅ **Primary — include all** | Purpose-built SIC for industrial valve, tap, and pneumatic/hydraulic valve manufacturing. Extremely clean. |
| 28291 | Manufacture of other general-purpose machinery n.e.c. | ❌ Exclude | Too broad — only include if keyword "valve" appears in company description |

**SIC precision rating:** ⭐⭐⭐⭐⭐ (single-purpose SIC, near-zero noise)

**Note:** SIC 28120 covers manufacturers of industrial valves, taps, solenoid valves, pneumatic valves, hydraulic valves, valve actuators, and valve servicing/repair companies that also manufacture.

---

## Field Schema

| # | Field | Type | Description |
|---|-------|------|-------------|
| 1 | **business_name** | string | Registered company name from Companies House |
| 2 | **company_number** | string | Companies House registration number |
| 3 | **email** | string | Business email found on company website |
| 4 | **phone** | string | UK landline with area code |
| 5 | **website** | string | Company website URL |
| 6 | **sic_code** | string | Primary SIC code (28120) |
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
- `ADMINISTRATION`, `LIQUIDATION`, `RECEIVERSHIP`
- `PLUMBING MERCHANT` — distributors, not manufacturers
- `BUILDERS MERCHANT` — general building suppliers
- `DO IT YOURSELF` / `DIY` — retail sellers

### Include (prefer records with these signals)
- Name or description contains: `VALVE`, `VALVES`, `MANUFACTURING`, `ENGINEERING`, `FLUID CONTROL`, `PNEUMATIC`, `HYDRAULIC`, `ACTUATOR`, `PROCESS EQUIPMENT`, `INDUSTRIAL SUPPLY`

### Business Type Filter
- Include: `ltd`, `plc`, `LLP`
- Exclude: `registered-society`, `royal-charter`, `ordinary-business`, `individual` (sole traders without Ltd status are harder to verify)

---

## Cleaning Rules

| Rule | Action |
|------|--------|
| **Email format** | Must match `*@*.*` with no spaces |
| **Phone format** | Normalise to `+44 xxxx xxx xxx`. Strip spaces, dashes, brackets |
| **Postcode validation** | Match regex `[A-Z]{1,2}[0-9][A-Z0-9]? [0-9][A-Z]{2}` |
| **Dedup by company_number** | Keep record with the most filled fields |
| **Dedup by business_name** | Remove exact duplicates |
| **Dormant removal** | Remove `Dormant` filing status |
| **Young company removal** | Remove incorporation < 6 months ago |
| **Website check** | Remove if domain returns HTTP 404 or parked |
| **Description cross-check** | If company description mentions `RETAIL`, `DISTRIBUTION ONLY`, or `WHOLESALE ONLY` without also mentioning manufacturing: flag for manual review |

---

## Collection Strategy

### Phase 1 — Companies House API Query
```
GET https://api.company-information.service.gov.uk/advanced-search/companies
Params:
  sic_codes: 28120
  company_status: active
  company_type: ltd,plc,llp
  size: 100 (paginated)
```
Expected raw yield: ~1,200 total, ~800-900 active

### Phase 2 — Geographic & Size Filter
Valve manufacturing in the UK is concentrated in:
- Midlands: Birmingham, Wolverhampton, Coventry, Leicester, Derby
- North West: Manchester, Bolton, Blackburn, Preston
- Yorkshire: Leeds, Sheffield, Bradford
- Scotland: Glasgow area

Aim for a representative geographic spread — don't over-sample the Midlands.

### Phase 3 — Website Discovery
For each active company:
1. Look up website from CH filing or Google search
2. Visit and confirm they manufacture valves (not just plumbing fittings)
3. Extract email from Contact page `mailto:` links
4. Extract phone from footer

Expected contact discovery yield: ~500 with email found (better website presence than marine)

### Phase 4 — Final Filter
- Remove any company that is clearly a plumbing merchant or general distributor
- Apply all cleaning rules
- Verify 100 clean records

Target final yield: **100 verified records**

---

## Data Quality Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **SIC 28120 includes plumbing taps** | The SIC covers both industrial valves AND domestic taps/faucets. Domestic tap manufacturers are NOT good B2B targets | Keyword filter in Phase 3: exclude companies whose description mentions "bathroom," "kitchen tap," "plumbing fitting" without mention of industrial/process use |
| **Geographic concentration** | Heavy Midlands bias may make the list look same-y | Note geographic concentration in product description. Regional segmentation is valuable for targeted marketing |
| **Small company = limited online presence** | Many small valve manufacturers have no email listed on website | Fallback to phone-only contact for these; flag in the list |
| **Dormant companies retained on CH** | Companies House keeps dissolved/dormant records in search results | Always filter by `company_status: active` |
| **Multiple SIC codes per company** | Some valve manufacturers also have unrelated SIC codes (e.g. property management) | Check the full SIC list per company. The primary SIC 28120 is the most important signal |

---

## Estimated Effort

| Step | Effort | Notes |
|------|--------|-------|
| Companies House query + cleanup | 30 min | Single SIC, fast extraction |
| Website research (500 companies) | 15-20h | Many established websites |
| Email/phone extraction | 4h | |
| Final verification & dedup | 2h | |
| **Total** | **~22-27h** | Most efficient SIC of the three |
