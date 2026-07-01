# Data Builder Spec: UK Security Companies (Alarm/CCTV Installers)
**Prepared by:** Data Builder Agent  
**Date:** 2026-07-01  
**Status:** Build spec (no data collected yet)

---

## SIC Code(s) to Target

| Code | Description | Include/Exclude | Notes |
|------|-------------|-----------------|-------|
| **80200** | Security systems service activities | ✅ **Primary — include all** | Captures alarm installers, CCTV installers, access control, intruder detection, and security monitoring companies. Highly specific. |
| 80100 | Private security activities | ❌ **Exclude explicitly** | Manned guarding, security patrols — different industry, different buyer profile. Ensures list is installer-focused. |

**SIC precision rating:** ⭐⭐⭐⭐⭐ (SIC 80200 is purpose-built for systems installers)

**Critical note:** SIC 80100 (manned guarding) is deliberately excluded. Many security companies have multiple SICs. If a company has BOTH 80200 and 80100, flag for manual review — they may be a mixed business that does both installation and guarding.

---

## Field Schema

| # | Field | Type | Description |
|---|-------|------|-------------|
| 1 | **business_name** | string | Registered company name from Companies House |
| 2 | **company_number** | string | Companies House registration number |
| 3 | **email** | string | Business email found on company website |
| 4 | **phone** | string | UK landline (security companies nearly always have a landline) |
| 5 | **website** | string | Company website URL |
| 6 | **sic_code** | string | Primary SIC code (80200) |
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
- `MANNED GUARDING`, `SECURITY GUARD`
- `DOOR SUPERVISOR` — nightclub/venue security, not systems
- `EVENT SECURITY` — staffing, not installation
- `CLOSE PROTECTION` — bodyguard services
- `DOG HANDLING`, `DOG PATROL`, `K9` — dog unit security
- `CASH IN TRANSIT` — money transport, not installers
- `KEY HOLDING` (alone — key holding is a separate service, not installation)

### Include (prefer records matching these signals)
- Description contains: `ALARM`, `CCTV`, `SECURITY SYSTEM`, `ACCESS CONTROL`, `INTRUDER`, `MONITORING`, `SURVEILLANCE`, `FIRE ALARM`, `SECURITY INSTALLATION`, `ELECTRONIC SECURITY`, `REMOTE MONITORING`, `INTERCOM`, `GATE AUTOMATION`

### Disqualifiers (if description contains ONLY these, no installation keywords)
- `MANNED GUARD`, `GUARD PATROL`, `BODYGUARD`, `EVENT STAFF`, `STEWARDING`, `VIP PROTECTION`

---

## Cleaning Rules

| Rule | Action |
|------|--------|
| **Email format** | Must match `*@*.*` with no spaces |
| **Phone format** | Normalise to `+44 xxxx xxx xxx` |
| **Postcode validation** | Match regex `[A-Z]{1,2}[0-9][A-Z0-9]? [0-9][A-Z]{2}` |
| **Dedup by company_number** | Keep record with the most filled fields |
| **Dedup by business_name** | Remove exact duplicates |
| **Dormant removal** | Remove `Dormant` filing status |
| **Young company removal** | Remove incorporation < 6 months ago |
| **Website check** | Remove if domain returns HTTP 404 or parked |
| **SIC cross-check** | If company has BOTH 80200 and 80100: flag for manual review — could be mixed business |
| **NSI/SSAIB tagging** | If company is NSI or SSAIB accredited (check website): tag in a `certification` field. This is a quality differentiator worth £5-10 premium |

---

## Collection Strategy

### Phase 1 — Companies House API Query
```
GET https://api.company-information.service.gov.uk/advanced-search/companies
Params:
  sic_codes: 80200
  company_status: active
  company_type: ltd,plc,llp
  size: 100 (paginated)
```
Expected raw yield: ~4,000 total, ~2,500-3,000 active

### Phase 2 — Size Segmentation (Optional but Recommended)
The security installer market splits into natural tiers:

| Tier | Size | Est. Count | Approach |
|------|------|------------|----------|
| National/regional chains | 50+ employees | ~100-200 | Multi-branch, high-value targets. Best online presence |
| Local specialists | 5-49 employees | ~800-1,200 | Core list — owner-operated, fast decision-making |
| Sole traders | 1-4 employees | ~1,500+ | Many but harder to verify, lower ticket value |

**Recommendation:** Focus on tiers 1+2 for the 100-record core list.

### Phase 3 — NSI/SSAIB Cross-Reference (Quality Signal)
Two UK accreditation bodies for security installers:
- **NSI** (National Security Inspectorate) — gold standard
- **SSAIB** (Security Systems and Alarms Inspection Board) — silver standard

Cross-referencing adds a quality differentiator worth noting in product description:
- "100 UK security installers — fully verified, NSI/SSAIB accredited where available"

### Phase 4 — Website Discovery
For top 1,000 active companies (focusing on tiers 1+2):
1. Visit company website
2. Extract email from Contact page `mailto:` links
3. Extract phone from footer
4. Confirm the company installs security systems (not just manned guarding)
5. Note NSI or SSAIB accreditation for quality tagging

Expected contact discovery yield: ~600 with email found

### Phase 5 — Final Filter
- Remove any company that is predominantly manned guarding
- Apply all cleaning rules
- Ensure geographic spread (London, South East, Midlands, North West, Scotland, Wales, NI)
- Verify 100 clean records

Target final yield: **100 verified records**

---

## Data Quality Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **SIC 80200 mixes installers with monitoring-only** | Some companies listed under 80200 are remote monitoring centres, not field installers | Website check confirms actual service offering. Monitoring-only companies still buy equipment — include if they sell systems too |
| **80100/80200 co-listed companies** | Some large security firms do BOTH guarding and installation | Flag for manual review. Include if at least 30% of business is installation |
| **Geographic oversaturation** | London and SE have the most security installers per capita | Deliberately spread across 9 UK regions. Product description: "Nationwide coverage" |
| **NSI/SSAIB lists are not free** | These directories may require registration or payment to access | Check whether free search exists. If not, rely on company website claims (usually prominently displayed) |
| **High employee churn in security** | Company may be active on CH but no longer trading | Cross-reference with website activity. If site is <6 months old or shows no recent content, flag |
| **Many one-man-band installers** | Work from home, PO box address, hard to verify | Exclude sole traders from primary list. Use as backup pool if yield is low |

---

## Estimated Effort

| Step | Effort | Notes |
|------|--------|-------|
| Companies House query + cleanup | 1h | Largest pool (4,000+), needs filtering for tiers |
| NSI/SSAIB cross-reference | 2h | Quality signal addition |
| Website research (600 companies) | 20-24h | Largest pool but best websites |
| Email/phone extraction | 5h | |
| Final verification & dedup | 2h | |
| **Total** | **~30-34h** | Largest market = best yield but most work |

---

## Pricing & Positioning Notes

- **Unique angle:** Systems installers only — not manned guards. Most generic "security company" lists mix both. This separation is rare.
- **Target buyer:** Security equipment distributors (Hikvision, Dahua, Bosch), alarm monitoring software vendors, vehicle leasing (installers run fleets of vans), insurance brokers (liability coverage), tool/equipment suppliers
- **Differentiator:** Clean SIC 80200 + NSI/SSAIB accreditation tagging = quality signal above scraped lists
- **Competition:** Some security installer lists exist on Apollo.io but are low quality (scraped, mixed with manned guarding). A hand-verified list at £75 is competitive.
