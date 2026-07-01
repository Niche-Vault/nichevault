# Build Spec: Solar Panel Installers UK
**Prepared by:** Data Builder Agent  
**Date:** 2026-06-30  
**Status:** Build spec (no data collected)

---

## 1. Target SIC Codes

| Code | Description | Include/Exclude |
|------|-------------|-----------------|
| **43220** | Plumbing, heat and air-conditioning installation | ✅ **Primary — includes solar thermal installation** |
| 43210 | Electrical installation | ✅ Secondary — includes solar PV installation |
| 35110 | Production of electricity | ✅ Secondary — solar farms and generation |
| 71122 | Engineering related scientific and technical consulting activities | ✅ Tertiary — renewable energy engineering consultants |

**SIC precision rating:** ⭐⭐⭐ (No single perfect SIC — needs keyword filtering across multiple codes)

**Recommended approach:** Query SIC 43220 + SIC 43210, then keyword-filter company descriptions for:
```
SOLAR, PHOTOVOLTAIC, PV, RENEWABLE ENERGY, SOLAR PANEL, SOLAR THERMAL,
SOLAR INSTALL, GREEN ENERGY, SUSTAINABLE ENERGY
```

---

## 2. Required Field Schema

| # | Field | Type | Required | Notes |
|---|-------|------|----------|-------|
| 1 | business_name | string | ✅ | Registered company name, cleaned |
| 2 | email | string | ✅ | Sourced from website or verified directory |
| 3 | phone | string | ✅ | UK format: 01xxx xxxxxx or 07xxx xxxxxx |
| 4 | postcode | string | ✅ | Full UK postcode from registered address |
| 5 | website | string | ✅ | Company website (if available) |
| 6 | sic_code | string | ✅ | Primary SIC code |
| 7 | town | string | ✅ | Town/city from registered address |
| 8 | company_number | string | ✅ | Companies House registration number |
| 9 | company_type | string | No | e.g. ltd, plc, LLP |
| 10 | incorporation_date | date | No | For filtering |
| 11 | address_line_1 | string | No | Full registered address |
| 12 | county | string | No | For regional segmentation |
| 13 | employee_count | int | No | From filing data if available |
| 14 | mcs_certification | string | No | MCS certified? (quality signal for solar) |

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
- GAS INSTALLATION ONLY (no solar)
- BOILER REPAIR (domestic heating only)
- PLUMBING ONLY (no solar mention)
- ROOFING ONLY (unless also doing solar)
```

Exclude companies with filing status: *dissolved*, *liquidation*, *administration*

**Keyword confidence filter — include only if company description or name contains:**
```
SOLAR, PHOTOVOLTAIC, PV PANEL, SOLAR PANEL, 
SOLAR THERMAL, SOLAR PV, RENEWABLE ENERGY,
SOLAR INSTALLER, SOLAR POWER, SOLAR ENERGY,
MICROGENERATION, SOLAR SYSTEMS
```

**Disqualifiers (exclude if description contains ONLY these, no solar):**
```
PLUMBING, GAS, HEATING, BOILER, RADIATOR, CENTRAL HEATING
(Unless a solar keyword also appears)
```

---

## 4. Cleaning Rules

| Rule | Action |
|------|--------|
| **Duplicate business_name** | Keep record with most complete data |
| **Email format** | Must match `*@*.*` pattern |
| **Phone format** | Normalise to `+44 xxxx xxx xxx` |
| **Postcode validation** | Must match UK postcode regex |
| **Turnover filter** | Remove companies with `DORMANT` filing status |
| **Incorporation date** | Exclude companies registered < 3 months ago |
| **Website check** | Remove if domain returns 404 or parked page |
| **Keyword confirmation** | Any company without "solar" in name or SIC description: must confirm via website visit |

---

## 5. Collection Strategy

### Phase 1 — Companies House Cross-SIC Query
This needs more work than single-SIC niches. Recommended approach:

1. **Query A:** SIC 43220 + keyword "solar" in description
2. **Query B:** SIC 43210 + keyword "solar" in description
3. **Query C:** SIC 35110 (solar generation companies — these are often larger)
4. **Merge & dedup** all three queries
5. Expected yield: ~1,500-2,000 after keyword filtering

### Phase 2 — MCS Certification Cross-Reference
MCS (Microgeneration Certification Scheme) is a quality differentiator for solar installers. Cross-reference Companies House results against:
- MCS certified installers directory
- Solar Energy UK member directory
- RECC (Renewable Energy Consumer Code) members

### Phase 3 — Website & Contact Discovery
For the top 500 candidates:
1. Visit each website
2. Extract email from mailto: links  
3. Find phone in footer/contact page
4. Confirm they install solar panels (not just sell them)
5. Note MCS certification status (marketing point)

### Phase 4 — Verification
- Verify 100 best contacts
- Prioritise MCS-certified installers
- Ensure a geographic spread (not all South East)
- Final list: 100 verified records

### Recommended Data Sources

| Source | Priority | Details |
|--------|----------|---------|
| Companies House API | Primary | Multi-SIC + keyword filtering needed |
| MCS website | Supplementary | Certified installer directory |
| Solar Energy UK | Supplementary | Trade association members |
| RECC directory | Supplementary | Consumer code members |
| Google Maps | Supplementary | "Solar panel installer near me" for geographic spread |

---

## 6. Estimated Timeline & Effort

| Step | Effort | Notes |
|------|--------|-------|
| Companies House multi-query + dedup | 2 hours | Most complex query of the 4 niches |
| MCS/renewable cross-reference | 3 hours | Adding quality filter |
| Website research (300 companies) | 15-20 hours | Many have sites but need verification |
| Email verification | 4 hours | 100 records |
| Final QA & dedup | 2 hours | |
| **Total** | **~26-31 hours** | More front-loaded query work |

---

## 7. Pricing & Positioning Notes

- **Unique angle:** Growing market driven by energy costs and net-zero. Solar installers are actively buying equipment and expanding.
- **Target buyer:** Solar panel distributors (JA Solar, Longi, Trina), inverter suppliers (SMA, Sungrow, Huawei), battery storage manufacturers, scaffolding companies, electrical wholesalers, vehicle leasing.
- **Differentiator:** MCS-certified filter option available. Not just scraped data.
- **Competition check:** Some solar installer lists exist but are poorly maintained. A fresh, verified list at £75 is competitive.
- **Market timing:** Post-energy crisis UK has seen major solar adoption. Installers are expanding and have active purchasing needs. Good for Q3/Q4 selling.
