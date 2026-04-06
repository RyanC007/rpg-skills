# SDR Lead Scraper Agent - Manus Agent Skill

**Agent that scrapes Google Maps for business leads and exports to Google Sheets.**

## Purpose

This agent searches Google Maps for businesses by type and location, scrapes all contact and business data (regardless of website status), and exports the results to a Google Sheet in the `SDR-lead-gen` folder.

## When to Use

Use this agent when you need to:
- Generate leads for outbound sales campaigns
- Build business databases for specific industries
- Research competitors in a geographic area
- Find potential partners or vendors
- Collect business contact information at scale

## How to Invoke

### From Chat Window

```
Run sdr-lead-scraper-agent to find 25 architects in Raleigh, NC
```

### From Another Agent (Trinity, Scarlett, Thor)

```
Invoke the sdr-lead-scraper-agent to search for plumbers in Austin, TX (30 businesses)
```

## Required Inputs

1. **Business Type** - Type of business to search for (e.g., "architects", "plumbers", "dentists")
2. **Location** - Geographic location (e.g., "Raleigh, NC", "Austin, TX")
3. **Count** (optional) - Number of businesses to find (default: 25)

## Workflow

1. **Navigate to Google Maps** - Open Google Maps in browser
2. **Search for businesses** - Enter search query (business type + location)
3. **Scrape business listings** - Extract data from search results
4. **Collect details** - Click into each business to get full contact info
5. **Export to CSV** - Create CSV with all business data
6. **Upload to Google Drive** - Save to `SDR-lead-gen` folder as Google Sheet
7. **Return shareable link** - Provide link to the created Google Sheet

## Output Data Fields

- Business Name
- Full Address (street, city, state, postal code, country)
- Phone Number
- Email (if available)
- Website (if available)
- Business Type
- Category
- Services Offered
- Rating (0-5 stars)
- Number of Reviews
- Google Maps URL
- Google Place ID
- GPS Coordinates (latitude, longitude)
- Description
- Notes

## Output Format

**Google Sheet Name:** `{Business Type} - {Location} - {Timestamp}`  
**Example:** `Architects - Raleigh, NC - 2026-02-05 15:30`

**Location:** Google Drive > `SDR-lead-gen` folder

## Implementation Instructions

When this agent is invoked, follow these steps:

### Step 1: Parse Inputs

Extract business type, location, and count from the user's request.

### Step 2: Navigate to Google Maps

```
Use browser_navigate to open: https://www.google.com/maps
```

### Step 3: Search for Businesses

```
Use browser_input to enter search query: "{business_type} in {location}"
Press Enter to search
```

### Step 4: Scrape Business Listings

```
Use browser_view to see search results
Extract business names, addresses, ratings from visible listings
Scroll down to load more results if needed
```

### Step 5: Collect Detailed Information

For each business in the results (up to target count):
```
Click on business listing
Wait for details panel to load
Extract: phone, website, hours, services, reviews, etc.
Go back to search results
Repeat for next business
```

### Step 6: Create CSV

```
Compile all scraped data into CSV format
Headers: Business Name, Address, City, State, Postal Code, Country, Phone, Email, Website, Business Type, Category, Services, Rating, Reviews Count, Google Maps URL, Google Place ID, Latitude, Longitude, Description, Notes
```

### Step 7: Upload to Google Drive

```
Use rclone to upload CSV to SDR-lead-gen folder
Convert to Google Sheet (or upload as CSV)
Generate shareable link
```

### Step 8: Return Results

```
Provide user with:
- Link to Google Sheet
- Summary of businesses found
- Any issues encountered
```

## Error Handling

- **No results found:** Try broader search terms or different location
- **Google Maps rate limiting:** Add delays between requests, use scrolling instead of clicking
- **Missing data:** Note which fields are unavailable, continue with partial data
- **Google Drive upload fails:** Save CSV locally and provide download link

## Best Practices

1. **Add delays** between business clicks (1-2 seconds) to avoid detection
2. **Save progress** periodically in case of interruption
3. **Handle missing data gracefully** - not all businesses have email/website
4. **Respect rate limits** - don't scrape too aggressively
5. **Verify data quality** - check that addresses and phone numbers look valid

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
  ✓ Downtown Dentistry
  ... (22 more)
[5/7] Creating CSV with 25 businesses...
[6/7] Uploading to Google Drive (SDR-lead-gen folder)...
[7/7] Complete!

📊 Google Sheet: https://drive.google.com/...
📁 Sheet Name: Dentists - Boston, MA - 2026-02-05 15:30
📈 Total Leads: 25

Ready for HubSpot import.
```

## Integration with HubSpot

1. Open the Google Sheet
2. Download as CSV
3. Go to HubSpot > Contacts > Import
4. Upload CSV
5. Map columns to HubSpot properties
6. Complete import

## Notes

- This agent uses browser automation, so it requires a Manus task with browser access
- Scraping time depends on number of businesses (approximately 5-10 seconds per business)
- Google Maps may show different results based on location and personalization
- Some businesses may have incomplete data (missing phone, email, website)

## Version

**Version:** 1.0  
**Last Updated:** February 5, 2026  
**Built by:** Trinity for Ready, Plan, Grow!
