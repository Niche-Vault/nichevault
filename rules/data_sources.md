# NicheVault Data Sources Policy
**Last updated:** 2026-06-30

---

## Allowed Data Sources

These sources are approved for building lead lists. Priority order matters — use Primary first.

### Primary Sources
| Source | Why | Notes |
|--------|-----|-------|
| **Companies House API** | Official UK company register — most authoritative source of company names, SIC codes, registered addresses, incorporation dates, and filing status | Free tier available. Filter by SIC code, active status, company type. Best single source. |
| **Company websites** | Email and phone extraction from `mailto:` links or contact pages | Must be manually verified — visit the site, confirm the email exists on the page. Not guessed `info@` addresses. |

### Supplementary Sources
| Source | Why | Notes |
|--------|-----|-------|
| **Industry trade association directories** | Adds quality signal (e.g. NSI for security, MCS for solar, BVAA for valves, British Marine for marine) | Cross-reference against Companies House to avoid outdated listings |
| **Google Maps / Places API** | Good for geographic spread and verifying businesses are still trading | Use for spot-checking, not bulk extraction |
| **SIC code directories** | Third-party SIC lookup tools to validate code assignments | Verify against official ONS SIC classification |

---

## Disallowed Data Sources

The following are **never** acceptable for NicheVault lists:

| Source | Why Banned |
|--------|------------|
| **Scraped/aggregated directories** (Yell.com, 192.com, FreeIndex, etc.) | No per-company verification. Data is stale, often duplicated, and has no guarantee of accuracy. |
| **Social media profile scraping** (LinkedIn, Facebook, Twitter) | Violates terms of service. Unethical. Data quality is poor for B2B lead lists. |
| **Purchased/rented third-party lists** | No provenance. Seller cannot guarantee consent or accuracy. Damages NicheVault's reputation and deliverability. |
| **Public apology / data dump sites** | Illegal or grey-market data with no rights to use. Never acceptable. |
| **AI-generated company data** | Fabricated companies are useless and waste buyer time. All entries must correspond to real registered companies. |

---

## Verification Standard

Every record in a NicheVault list must pass:
1. **Companies House registration confirmed** — company_number maps to an active filing on CH
2. **Website accessible** — the domain returns a 200 status and displays real business content
3. **Email found on site** — the email address appears in a `mailto:` link or contact page of the company website (not guessed as `info@domain.com`)
4. **Business name matches** — the name on Companies House matches the name used on the website

Records failing any check are removed from the list. No exceptions.

---

## Geographic Scope

- **Primary:** United Kingdom (England, Scotland, Wales, Northern Ireland)
- **Excluded:** Channel Islands (Jersey, Guernsey), Isle of Man — separate legal registers
- **Excluded:** Companies registered at non-UK addresses or using a UK service address with no trading presence

---

## Data Freshness

| Data Point | Maximum Age Before Refresh |
|------------|---------------------------|
| Company name + number | 12 months |
| Address / postcode | 12 months |
| Email | 6 months |
| Phone | 6 months |
| Website | 6 months |
|