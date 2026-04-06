# SDR Lead Scraper Agent

**Manus Agent Skill that scrapes Google Maps for business leads and exports to Google Sheets.**

## Overview

This agent searches Google Maps for businesses by type and location using browser automation, scrapes all contact and business data, and exports the results to a Google Sheet in the `SDR-lead-gen` folder on Google Drive.

**Key Features:**
- Scrapes Google Maps using Manus browser automation (no API required)
- Searches ALL businesses (with or without websites)
- Exports to Google Sheets automatically
- Creates new sheet per search with timestamp
- Includes all contact data (name, address, phone, email, website, etc.)
- Ready for HubSpot import

## Quick Start

### Invoke from Chat Window

```
Run sdr-lead-scraper-agent to find 25 architects in Raleigh, NC
```

### Invoke from Another Agent

```
Invoke the sdr-lead-scraper-agent to search for plumbers in Austin, TX (30 businesses)
```

## How It Works

1. Opens Google Maps in browser
2. Searches for businesses by type and location
3. Scrapes business listings from search results
4. Clicks into each business to collect detailed contact info
5. Compiles data into CSV format
6. Uploads to Google Drive `SDR-lead-gen` folder as Google Sheet
7. Returns shareable link to the created sheet

## Required Inputs

| Input | Required | Description | Example |
|-------|----------|-------------|---------|
| Business Type | Yes | Type of business to search | "architects", "plumbers", "dentists" |
| Location | Yes | Geographic location | "Raleigh, NC", "Austin, TX" |
| Count | No | Number of businesses (default: 25) | 25, 30, 50 |

## Output

### Google Sheet

Each search creates a new Google Sheet in the `SDR-lead-gen` folder with:

**Sheet Name Format:** `{Business Type} - {Location} - {Timestamp}`  
**Example:** `Architects - Raleigh, NC - 2026-02-05 15:30`

**Columns:**
- Business Name
- Address (street, city, state, postal code, country)
- Phone, Email, Website
- Business Type, Category, Services
- Rating, Reviews Count
- Google Maps URL, Google Place ID
- GPS Coordinates (latitude, longitude)
- Description, Notes

## Use Cases

### 1. Pure Lead Generation
Scrape businesses for cold calling or email campaigns.

### 2. Market Research
Analyze business density, ratings, and competition in specific areas.

### 3. Database Building
Build comprehensive business databases for specific industries.

### 4. Competitive Analysis
Identify all competitors in a given market.

### 5. Partnership Outreach
Find potential partners or vendors in specific locations.

## Integration with HubSpot

1. Open the Google Sheet from `SDR-lead-gen` folder
2. Download as CSV
3. Go to HubSpot > Contacts > Import
4. Upload CSV
5. Map columns to HubSpot properties
6. Complete import

## Technical Details

- **Browser Automation:** Uses Manus browser tools (no external API required)
- **Scraping Speed:** Approximately 5-10 seconds per business
- **Rate Limiting:** Built-in delays to avoid detection
- **Data Quality:** Handles missing fields gracefully
- **Error Handling:** Continues on errors, reports issues at end

## Documentation

- **SKILL.md** - Complete skill implementation guide
- **docs/SETUP.md** - Installation and configuration (deprecated for skill-based approach)
- **docs/USAGE.md** - Usage examples and use cases
- **docs/RECOVERY.md** - Disaster recovery procedures

## Example Invocation

**User:** "Run sdr-lead-scraper-agent to find 25 dentists in Boston, MA"

**Agent Response:**
```
Starting SDR Lead Scraper Agent...

Business Type: dentists
Location: Boston, MA
Target Count: 25

[1/7] Navigating to Google Maps...
[2/7] Searching for dentists in Boston, MA...
[3/7] Found 150+ results, scraping first 25...
[4/7] Collecting detailed information...
  ✓ Boston Dental Associates
  ✓ Smile Center of Boston
  ... (23 more)
[5/7] Creating CSV with 25 businesses...
[6/7] Uploading to Google Drive...
[7/7] Complete!

📊 Google Sheet: https://drive.google.com/...
📁 Sheet Name: Dentists - Boston, MA - 2026-02-05 15:30
📈 Total Leads: 25
```

## Notes

- This agent uses browser automation and must be invoked from a Manus task
- Scraping time varies based on number of businesses requested
- Google Maps results may vary based on location and personalization
- Some businesses may have incomplete data (missing phone, email, website)

## Cost

**Free** - No API costs, uses Manus browser automation

## Support

For issues or questions, contact Ryan at Ready, Plan, Grow!

## License

Private - Ready, Plan, Grow! internal use only

---

**Built by Trinity for Ready, Plan, Grow!**  
**Last Updated:** February 5, 2026
