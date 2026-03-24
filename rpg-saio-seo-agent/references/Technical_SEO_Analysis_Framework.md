# Technical SEO Analysis Framework
## Screaming Frog Data Processing & Issue Prioritization System

**Purpose:** This framework provides a systematic methodology for analyzing Screaming Frog crawl data, categorizing technical SEO issues, and creating actionable fix roadmaps.

---

## Overview

When a Screaming Frog export file is provided, the AI agent will parse the data, identify all technical SEO issues, categorize them by priority, and generate a comprehensive audit spreadsheet with detailed fix instructions. This framework ensures consistent, high-quality technical analysis across all projects.

---

## Step 1: Data Ingestion & Parsing

### Accepted File Formats
The system accepts Screaming Frog exports in the following formats:
- CSV export (single tab or multiple CSV files)
- Excel export (.xlsx) with multiple tabs
- "All Tabs" export (preferred for comprehensive analysis)

### Key Data Tabs to Process

When processing a Screaming Frog export, focus on extracting data from these critical tabs:

**1. Internal Tab**
- URL
- Status Code
- Content Type
- Title 1
- Title 1 Length
- Meta Description 1
- Meta Description 1 Length
- H1-1
- H1-2 (if present)
- Word Count
- Indexability
- Indexability Status

**2. Response Codes Tab**
- URL
- Status Code
- Status

**3. Page Titles Tab**
- URL
- Title 1
- Title 1 Length
- Title 1 Pixel Width
- Occurrences (for duplicate detection)

**4. Meta Description Tab**
- URL
- Meta Description 1
- Meta Description 1 Length
- Meta Description 1 Pixel Width
- Occurrences (for duplicate detection)

**5. H1 Tab**
- URL
- H1-1
- H1-1 Length
- Occurrences (for duplicate H1 detection)

**6. Canonicals Tab**
- URL
- Canonical Link Element 1
- Canonical Link Element 1 Indexability

**7. Images Tab**
- Source
- Alt Text
- Size (KB)

**8. Structured Data Tab**
- URL
- Structured Data Type
- Structured Data Errors

**9. Directives Tab**
- URL
- Meta Robots 1
- X-Robots-Tag 1

---

## Step 2: Issue Identification & Categorization

The system identifies issues across the following categories. Each issue is assigned to one of four priority levels based on its SEO impact and urgency.

### Issue Categories

#### A. Crawlability Issues
Issues that prevent search engines from properly crawling the site.

**Examples:**
- Broken internal links (404 errors)
- Redirect chains (3+ redirects)
- Redirect loops
- Server errors (5xx status codes)
- Blocked by robots.txt
- Slow server response time

#### B. Indexability Issues
Issues that prevent pages from being indexed or cause incorrect indexing.

**Examples:**
- Noindex tag on important pages
- Incorrect canonical tags
- Canonical pointing to 404 or redirected page
- Orphan pages (no internal links pointing to them)
- Duplicate content without proper canonicalization

#### C. On-Page SEO Issues
Issues related to on-page optimization elements.

**Examples:**
- Missing title tags
- Duplicate title tags
- Title tags too short (<30 characters) or too long (>60 characters)
- Missing meta descriptions
- Duplicate meta descriptions
- Meta descriptions too short or too long
- Missing H1 tags
- Multiple H1 tags on a single page
- Duplicate H1 tags across pages

#### D. Content Quality Issues
Issues related to content depth and quality.

**Examples:**
- Thin content (word count <300 words)
- Duplicate content across multiple URLs
- Pages with no content
- Low text-to-HTML ratio

#### E. Technical Performance Issues
Issues affecting site speed and user experience.

**Examples:**
- Large page sizes (>1MB)
- Slow-loading pages (>3 seconds)
- Uncompressed images
- Missing mobile-friendly tags
- Mixed content warnings (HTTP resources on HTTPS pages)

#### F. Schema Markup Issues
Issues related to structured data implementation.

**Examples:**
- Missing schema markup on key pages
- Schema markup errors
- Incomplete schema implementation
- Incorrect schema types

#### G. Image Optimization Issues
Issues related to image SEO.

**Examples:**
- Missing alt text on images
- Generic alt text ("image1.jpg")
- Oversized images (>200KB)
- Images in non-optimized formats

---

## Step 3: Priority Assignment Logic

Each identified issue is assigned a priority level (P1-P4) based on two factors: **SEO Impact** and **Page Importance**.

### Priority Level Definitions

**P1 - Critical (Fix Immediately)**
- **Criteria:** High SEO impact AND affects important pages (homepage, key service pages, high-traffic pages)
- **Timeline:** Fix within 1-2 weeks
- **Examples:**
  - 404 errors on high-traffic pages
  - Noindex tag on homepage or key service pages
  - Redirect chains on important pages
  - Server errors (5xx) on any page
  - Broken internal links from homepage
  - Missing title tags on key pages

**P2 - High Priority (Fix Within 2-4 Weeks)**
- **Criteria:** High SEO impact OR affects moderately important pages
- **Timeline:** Fix within 2-4 weeks
- **Examples:**
  - Missing meta descriptions on key pages
  - Duplicate title tags
  - Missing H1 tags on service pages
  - Orphan pages with valuable content
  - Slow page speed on key pages (>3 seconds)
  - Missing schema markup on homepage/service pages
  - Mobile usability issues

**P3 - Medium Priority (Fix Within 1-3 Months)**
- **Criteria:** Moderate SEO impact on less critical pages
- **Timeline:** Fix within 1-3 months
- **Examples:**
  - Thin content on blog posts
  - Missing alt text on images
  - Suboptimal title/description length
  - Redirect chains on less important pages
  - Minor canonicalization issues
  - Duplicate meta descriptions on blog posts

**P4 - Low Priority (Fix When Possible)**
- **Criteria:** Low SEO impact or cosmetic improvements
- **Timeline:** Fix within 3-6 months or as resources allow
- **Examples:**
  - Image optimization opportunities (file size reduction)
  - Minor HTML validation errors
  - Cosmetic improvements to title tags
  - Nice-to-have schema additions
  - Low-traffic pages with minor issues

### Page Importance Classification

To determine priority, pages are classified by importance:

**High Importance:**
- Homepage
- Key service/product pages
- Top 10 traffic-generating pages (if analytics data available)
- Key conversion pages
- Main category pages

**Medium Importance:**
- Secondary service pages
- Blog posts with traffic
- Resource pages
- Location pages

**Low Importance:**
- Old blog posts with no traffic
- Archive pages
- Tag pages
- Author pages

---

## Step 4: Fix Instructions Development

For each identified issue, the system generates detailed, step-by-step fix instructions tailored to the specific issue type. Instructions are written for an SEO technician or developer to implement.

### Fix Instruction Template

Each fix instruction includes:

1. **Issue Description:** Clear explanation of what the problem is
2. **Why It Matters:** SEO impact and business impact
3. **How to Fix:** Step-by-step instructions
4. **Verification:** How to confirm the fix was successful
5. **Estimated Time:** Time required to implement the fix
6. **Required Skills:** Technical skills needed (HTML, CSS, CMS knowledge, etc.)

### Example Fix Instructions

#### Fix: Missing Title Tag

**Issue Description:** The page at [URL] is missing a title tag, which is a critical on-page SEO element.

**Why It Matters:** Title tags are one of the most important ranking factors. Pages without title tags will not rank well in search results and will display poorly in SERPs.

**How to Fix:**
1. Access the page in your CMS or HTML editor
2. Locate the `<head>` section of the HTML
3. Add a `<title>` tag with a descriptive, keyword-rich title (50-60 characters)
4. Format: `<title>Primary Keyword - Secondary Keyword | Brand Name</title>`
5. Save and publish the page

**Verification:**
1. View the page source (right-click > View Page Source)
2. Confirm the `<title>` tag is present in the `<head>` section
3. Check the page in Google Search Console to ensure it's being crawled correctly

**Estimated Time:** 5-10 minutes per page  
**Required Skills:** Basic HTML or CMS knowledge

---

#### Fix: Redirect Chain

**Issue Description:** The URL [URL] redirects multiple times before reaching the final destination, creating a redirect chain.

**Why It Matters:** Redirect chains slow down page load times, waste crawl budget, and dilute link equity. Search engines may not follow long redirect chains, resulting in indexing issues.

**How to Fix:**
1. Identify the full redirect chain using a tool like Screaming Frog or Redirect Mapper
2. Update all internal links to point directly to the final destination URL
3. Update the initial redirect to point directly to the final URL (bypass intermediate redirects)
4. If using .htaccess, consolidate multiple redirect rules into a single direct redirect

**Verification:**
1. Use a redirect checker tool to confirm the URL now redirects only once (or not at all if updating internal links)
2. Check that the HTTP status code is 301 (permanent redirect)
3. Verify in Screaming Frog that the redirect chain is resolved

**Estimated Time:** 15-30 minutes per chain  
**Required Skills:** Server configuration knowledge (.htaccess or server config files)

---

## Step 5: Implementation Roadmap Creation

The system generates a week-by-week implementation roadmap that organizes all fixes by priority and provides realistic timelines.

### Roadmap Structure

**Phase 1: Critical Fixes (Weeks 1-2)**
- Focus: P1 issues only
- Goal: Resolve all site-breaking and high-impact issues
- Expected Outcome: Site is crawlable, indexable, and technically sound

**Phase 2: High Priority Fixes (Weeks 3-4)**
- Focus: P2 issues
- Goal: Optimize key pages for search engines
- Expected Outcome: Key pages are fully optimized and ranking potential is maximized

**Phase 3: Medium Priority Fixes (Months 2-3)**
- Focus: P3 issues
- Goal: Address content quality and optimization issues
- Expected Outcome: All important pages are optimized, site quality is high

**Phase 4: Low Priority Fixes (Months 4-6)**
- Focus: P4 issues
- Goal: Polish and optimize remaining pages
- Expected Outcome: Site is fully optimized with no outstanding technical issues

### Roadmap Table Format

| Week/Month | Phase | Issues to Address | Estimated Hours | Required Skills | Expected Outcome | Status |
|------------|-------|-------------------|-----------------|-----------------|------------------|--------|
| Week 1 | Critical Fixes | P1-001 to P1-015 | 10-15 hours | HTML, CMS | Site is crawlable | Not Started |
| Week 2 | Critical Fixes | P1-016 to P1-030 | 10-15 hours | HTML, Server Config | Key pages are indexable | Not Started |
| Week 3-4 | High Priority | P2-001 to P2-050 | 15-20 hours | HTML, CMS, Schema | Key pages optimized | Not Started |
| Month 2-3 | Medium Priority | P3-001 to P3-100 | 20-30 hours | Content, HTML | All pages optimized | Not Started |
| Month 4-6 | Low Priority | P4-001 to P4-050 | 10-20 hours | Various | Site fully polished | Not Started |

---

## Step 6: Spreadsheet Generation

The system generates a professional Excel spreadsheet with the following tabs:

### Tab 1: Executive Summary
- Total issues found (by priority)
- Site health score (calculated based on issue severity)
- Quick wins (high impact, low effort fixes)
- Critical issues requiring immediate attention
- Estimated total time to fix all issues
- Expected impact of fixes

### Tab 2: Critical Issues (P1)
Columns:
- Issue ID (e.g., P1-001)
- Issue Type (e.g., Missing Title Tag)
- Page/URL Affected
- Issue Description
- SEO Impact (High/Medium/Low)
- Business Impact (High/Medium/Low)
- Fix Instructions (detailed)
- Estimated Time to Fix
- Required Resources/Skills
- Dependencies
- Status (Not Started/In Progress/Complete)
- Notes

### Tab 3: High Priority Issues (P2)
Same column structure as Tab 2

### Tab 4: Medium Priority Issues (P3)
Same column structure as Tab 2

### Tab 5: Low Priority Issues (P4)
Same column structure as Tab 2

### Tab 6: Implementation Roadmap
Week-by-week plan (as described in Step 5)

### Tab 7: Fix Instructions Library
A comprehensive library of fix instructions for common issues, organized by category. This serves as a reference guide for the SEO technician.

---

## Quality Standards

### Minimum Requirements
- Analyze at least 100 pages (or entire site if smaller)
- Identify and categorize at least 50 issues
- Provide detailed fix instructions for all P1 and P2 issues
- Create a realistic, achievable implementation timeline
- Include success metrics for each fix

### Professional Formatting
- Color-coded tabs by priority (Red=P1, Orange=P2, Yellow=P3, Green=P4)
- Conditional formatting for status tracking
- Data validation for dropdown fields (Status, Priority, etc.)
- Frozen header rows for easy scrolling
- Appropriate column widths for readability
- Professional fonts and styling

---

This framework ensures that every technical SEO audit is thorough, actionable, and easy for clients to implement, regardless of their technical expertise.
