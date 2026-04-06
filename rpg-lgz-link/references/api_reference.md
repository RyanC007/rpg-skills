# Rpg Lgz Link — SDR & Lead Generation API Reference

**Version:** 1.0
**Last Updated:** March 18, 2026

---

## 1. Overview

Link uses external APIs to source and enrich leads for Logoclothz outbound campaigns. The primary tools are LinkedIn (via Proxycurl or similar scraping APIs) and Hunter.io for email enrichment.

---

## 2. Lead Sourcing (LinkedIn via Proxycurl)

### 2.1. Company Search
- **Endpoint:** `GET https://nubela.co/proxycurl/api/linkedin/company/resolve`
- **Purpose:** Find a company's LinkedIn profile based on name and domain.
- **Headers:** `Authorization: Bearer {PROXYCURL_API_KEY}`
- **Example Request:**
  ```bash
  curl -G \
    -H "Authorization: Bearer YOUR_API_KEY" \
    --data-urlencode "company_name=Acme Corp" \
    --data-urlencode "company_domain=acme.com" \
    "https://nubela.co/proxycurl/api/linkedin/company/resolve"
  ```

### 2.2. Employee Search (Decision Makers)
- **Endpoint:** `GET https://nubela.co/proxycurl/api/linkedin/company/employees`
- **Purpose:** Find employees at a specific company, filtering by role (e.g., "HR", "Operations", "Marketing").
- **Headers:** `Authorization: Bearer {PROXYCURL_API_KEY}`
- **Example Request:**
  ```bash
  curl -G \
    -H "Authorization: Bearer YOUR_API_KEY" \
    --data-urlencode "url=https://www.linkedin.com/company/acme-corp" \
    --data-urlencode "keyword_title=HR OR Operations" \
    "https://nubela.co/proxycurl/api/linkedin/company/employees"
  ```

---

## 3. Email Enrichment (Hunter.io)

### 3.1. Email Finder
- **Endpoint:** `GET https://api.hunter.io/v2/email-finder`
- **Purpose:** Find the professional email address of a decision maker.
- **Example Request:**
  ```bash
  curl "https://api.hunter.io/v2/email-finder?domain=acme.com&first_name=John&last_name=Doe&api_key=YOUR_API_KEY"
  ```

### 3.2. Domain Search
- **Endpoint:** `GET https://api.hunter.io/v2/domain-search`
- **Purpose:** Find all known email addresses for a specific company domain.
- **Example Request:**
  ```bash
  curl "https://api.hunter.io/v2/domain-search?domain=acme.com&api_key=YOUR_API_KEY"
  ```
