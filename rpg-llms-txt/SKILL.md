---
name: rpg-llms-txt
description: Generates a spec-compliant llms.txt file and supporting Markdown files for any website to improve AI crawler accessibility. Use when a user asks to create an llms.txt file, optimize a site for AI crawlers, or make a site readable by LLMs.
---

# RPG llms.txt Generator

This skill automates the creation of an `llms.txt` file and supporting Markdown files for a website, following the official specification at [llmstxt.org](https://llmstxt.org/). This is critical for ensuring modern AI search engines (like ChatGPT, Claude, and Perplexity) can accurately read and cite a client's website, especially if the site relies heavily on JavaScript rendering.

## Workflow

When asked to generate an `llms.txt` file for a domain, follow these steps:

1. **Run the Generator Script**
   Execute the bundled Python script to crawl the site's sitemap, extract clean text content, and generate the required files.
   
   ```bash
   python3.11 /home/ubuntu/skills/rpg-llms-txt/scripts/crawl_and_generate.py <domain.com> /home/ubuntu/llms_export
   ```
   *Note: The script automatically prioritizes the top 40 most important pages (products, about, faq, etc.) to keep the output focused and relevant for LLMs.*

2. **Review the Output**
   Check the generated files in the output directory. You should see:
   - `llms.txt` (The root index file)
   - Multiple `.md` files (Clean text versions of the crawled pages)

3. **Package for Delivery**
   Zip the output directory so it can be easily delivered to the user or web team.
   
   ```bash
   cd /home/ubuntu/llms_export && zip -r /home/ubuntu/<domain>_llms_txt.zip .
   ```

4. **Deliver and Explain**
   Send the zip file to the user using the `message` tool. You MUST include the following installation instructions for the web team:
   
   - **Step 1:** Upload `llms.txt` to the root of the site so it lives at `https://<domain.com>/llms.txt`
   - **Step 2:** Upload each `.md` file so it mirrors the existing page URL with `.md` appended. For example, `https://<domain.com>/faq/` becomes `https://<domain.com>/faq/index.html.md` (or just `faq.md` depending on their server routing).

## Why This Matters (Sales Angle)

If you are doing this as part of an audit or proposal, emphasize that traditional SEO teams often miss this. AI crawlers struggle with heavy JavaScript (like Elementor or React). Providing an `llms.txt` file is a modern, forward-looking technical SEO practice that directly improves visibility in AI-driven search.
