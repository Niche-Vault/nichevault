# Build Spec: UK Security Companies (Alarm/CCTV Installers)
**Prepared by:** Data Builder Agent  
**Date:** 2026-06-30  
**Status:** Build spec (no data collected)

---

## 1. Target SIC Codes

| Code | Description | Include/Exclude |
|------|-------------|-----------------|
| **80200** | Security systems service activities | ✅ **Primary — include all** |
| 80100 | Private security activities | ❌ Exclude (manned guarding — different buyer profile) |

**SIC precision rating:** ⭐⭐⭐⭐⭐ (SIC 80200 cleanly captures alarm, CCTV, and access control installers)

**Note:** SIC 80100 (manned guarding) is deliberately excluded — security guards are not the target. We want companies that *install and service* security systems. SIC 80200 is perfect for this.

---

## 2. Required Field Schema

| # | Field | Type | Required | Notes |
|---|-------|------|----------|-------|
| 1 | business_name | string | ✅ | Registered company name, cleaned |
| 2 | email | string | ✅ | Sourced from website or verified directory |
| 3 | phone | string | ✅ | UK format: 01xxx xxxxxx or 07xxx xxxxxx |
| 4 | postcode | string | ✅ | Full UK postcode from registered address |
| 5 | website | string | ✅ | Company website (if available) |
| 6 | sic_code | string | ✅ | Primary SIC code (80200) |
| 7 | town | string | ✅ | Town/city from registered address |
| 8 | company_number | string | ✅ | Companies House registration number |
| 9 | company_type | string | No | e.g. ltd, plc, LLP |
| 10 | incorporation_date | date | No | For filtering out recently registered |
| 11 | address_line_1 | string | No | Full registered address |
| 12 | county | string | No | For regional segmentation |
| 13 | employee_count | int | No | From filing data if available |
| 14 | turnover_indicator | string | No | Micro/small/medium |

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
- MANNED GUARDING
- SECURITY GUARD
- DOOR SUPERVISOR (nightclub/venue security, not systems)
- EVENT SECURITY (event staffing, not installers)
- CLOSE PROTECTION (bodyguard services)
- DOG HANDLING (dog patrol security)
```

Exclude companies with filing status: *dissolved*, *liquidation*, *administration*

**Keyword confidence filter (include only if company description contains):**
```
ALARM, CCTV, SECURITY SYSTEM, ACCESS CONTROL, INTRUDER, 
MONITORING, SURVEILLANCE, FIRE ALARM, FIRE SYSTEM,
SECURITY INSTALLATION, ELECTRONIC SECURITY, 
REMOTE MONITORING, INTERCOM, GATE AUTOMATION
```

**Disqualifiers (exclude if description contains):**
```
MANNED GUARD, GUARD PATROL, DOG, BODYGUARD, 
EVENT STAFF, STEWARDING, VIP PROTECTION
(Security installation companies do not do manned guarding)
```

---

## 4. Cleaning Rules

| Rule | Action |
|------|--------|
| **Duplicate business_name** | Keep record with most complete data; remove exact name duplicates |
| **Email format** | Must match `*@*.*` pattern |
| **Phone format** | Normalise to `+44 xxxx xxx xxx`. Strip non-numeric characters |
| **Postcode validation** | Must match UK postcode regex |
| **Turnover filter** | Remove companies with `DORMANT` filing status or `NO ACCOUNTS FILED` |
| **Incorporation date** | Exclude companies registered < 6 months ago |
| **Website check** | Remove if domain returns 404, parked page, or redirects to manned guarding company |
| **SIC cross-check** | If company has BOTH 80100 and 80200, review manually — could be mixed business |

---

## 5. Collection Strategy

### Phase 1 — Companies House Bulk Extraction
- Query SIC 80200 via Companies House API
- Filter: active status, not dissolved, not dormant
- Exclude any with SIC 80100 as secondary (mixed businesses need manual review)
- Expected yield: ~2,500-3,000 active (from 4,000+ total)

### Phase 2 — Sub-Segmentation (Optional)
The security installer market can be split into tiers:
- **National/regional chains** (50+ employees): Multi-branch installers, high-value targets
- **Local specialists** (5-49 employees): Core list — owner-operated, fast decision-making
- **Sole traders** (1-4 employees): Many but harder to verify and lower ticket value

**Recommendation:** Focus on tiers 1+2 for the 100-record list. Use employee count from filing data or turnover indicators to filter.

### Phase 3 — Website & Contact Discovery
For the top 1,000 active companies (focusing on tiers 1+2):
1. Visit each company website
2. Extract email from mailto: links  
3. Find phone in footer/contact page
4. Confirm the company installs security systems (not just manned guarding)
5. Note any NSI or SSAIB accreditation (quality signal)

### Phase 4 — Verification
- Verify 100 best contacts
- Confirm phone works
- Check SSAIB/NSI membership (a quality differentiator for the list)
- Final list: 100 verified records

### Recommended Data Sources

| Source | Priority | Details |
|--------|----------|---------|
| Companies House API | Primary | SIC 80200, company status, turnover |
| Company websites | Secondary | Email/phone extraction |
| NSI (National Security Inspectorate) website | Supplementary | Accredited installers directory |
| SSAIB website | Supplementary | Accredited installers directory |
| Security行业内 magazines (Professional Security, IFSEC Global) | Supplementary | Exhibitor/advertiser lists |

---

## 6. Estimated Timeline & Effort

| Step | Effort | Notes |
|------|--------|-------|
| Companies House query + filtering | 1 hour | Larger pool (4,000+) needs more filtering |
| Website research (500 companies) | 20-25 hours | Larger pool but many have good websites |
| SSAIB/NSI cross-reference | 2 hours | Adds quality signal |
| Email & phone verification | 5 hours | 100 records |
| Final QA & dedup | 2 hours | 100 records |
| **Total** | **~30-35 hours** | Larger market = more filtering time |

---

## 7. Pricing & Positioning Notes

- **Unique angle:** Systems installers only — not manned guards. Most general "security company" lists mix both. This separation is rare.
- **Target buyer:** Security equipment manufacturers (Hikvision, Dahua, Bosch distributors), alarm monitoring software vendors, vehicle leasing (fleet of vans), insurance brokers (liability for installers), tool suppliers.
- **Differentiator:** Clean SIC 80200. Manual vetting removes manned guarding companies that pollute generic lists.
- **Competition check:** Some security installer lists exist on Apollo.io but are low quality (scraped data). A hand-verified list at £75 is competitive.
- **NSI accreditation note:** Offering an "NSI-accredited installers only" filter option could justify a premium price point.
