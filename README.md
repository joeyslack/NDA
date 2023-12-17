# Nina's Dilligence Automator (NDA)

This project aims to retrieve targetted data from sources, sort, tag and save it, then generate a finalized PDF according to report specifications.

**NDA** currently relies solely on web scraping as a means of collecting data. If additional documents are provided per target, we can OCR or parse with new adapters as needed.

## General Concept & Process Outline

NDA's general concept is to:

- Retrieve data from multiple sources for the target entity, and save all relevant data found, sorted, tagged and grouped.
- Process the data with an LLM capable of generating summaries as you desire.
- Generate a finalized report consisting of raw and processed data as required, according to a PDF spec.

## Prerequisits

- Chrome User Profile with logged in status (`NDA_Profile`)
- Write access in output subdir

## Getting Started

1. `pip install -r requirements`
2. `python auth.py`. Login to all sources where appropriate.
3. `python scrape.py`
4. TODO: Process results with AI and generate summaries
5. TODO: Generate a report based on sample template

- DB Layer for cached data? We can always generate new reports with AI tool, based on stored/raw data (unless deleted). However, to avoid needless db hits, we could have a db/cache layer here. PG data (jsonb) or Mongo would work here. If simpler, a simple Redis layer could save us a lot of hassle with pricing/free limits during dev.

## Issues

### Login Sessions

Although we have the capability to save/load valid login sessions, we are electing to authenticating the user within a specified `Chrome User Profile`, for increased security, stealth and simplicity. Make sure to properly authenticate before running the scraper. Running `python auth.py` will have you verify yourself on each property.

### WebDriver Issues

If you have issues pertaining to the navigation of sources, further webdriver manipulation may be needed. To get started, you can try:
`brew install chromedriver`.

## Explaining the Process & Extensibility

Scraping is completed with a chrome driver *in browser*, with a `headless=False` flag. This is done to ensure simpler use of credential cookies (without storing credentials), and bypasses most basic bot checking. You will want to fine-tune the data stored for each site in list, to accommodate all data you require, and categorize each section correctly (tagged for AI).

Note: Running `auth.py` does a pre-run of each domain to ensure a valid login for each domain. It is critical to verify this before proceeding with any scraping. Complete proper login authentication on each site if authentication is not yet completed for this session.

For now, data is dumped into local `.json`/`.txt` documents for simpler use. If this were to scale, it would be replaced with a document store db with subtext searching features. Eventually, the AI tool will use the db directly as it requires data within vector distances and user/company filters.

Collected data should then be sent for processing (OpenAI?) llm, ensuring the correct insights are summarized from the collected data. The processed data should be conformed into a template specification, either using template variable injection, or having OpenAI generate the report automatically based on a sample template. Note: It would be ideal to provide a real `output.pdf` sample in this project source to be used as a reference.

## Bot Detection & Workarounds

All scripting relies on currently active chrome sessions. We bypass bot detection by using a real browser instance and real sessions. Undetected-chromedriver will mask significant portions of the webdriver footprint. With this method, once authenticated under your normal chrome-user, we can retrieve and use the active sessions in our automation. No captchas, or strange behavior should catch us.

Running this from the cloud, or other easily identified ip blocks will be flagged as bot usage.

IMPORTANT: Our `undetected-chromedriver` WebDriver cannot access the same `Chrome Profile` that might currently be in-use as your normal browser. This is unfortunately due to the way Chrome handles locking writing in `User Directories` (<https://github.com/ultrafunkamsterdam/undetected-chromedriver/issues/586>). So, you must authenticate on all of our sites normally, before **closing the browser** before running the `scrape.py` script. This way, our script can load the Chrome Profile (that contains active sessions & cookies). TLDR: Run `auth.py`, and make sure each source is "logged in", and authenticate if not.

## TODO

- Decide on list of scraping sites (`list.py`)
- Decide on HTML selectors on a per-site basis. Retrieve all data, tagged as appropriate. Make additional scraping calls if data is found on subsequent pages, we should be fairly free of bot abuse detection.
- Decide on standards for non-scraped data and add sample data to this project. Then create adapters to parse them.
- OpenAI token or alternative/additional processing adapter for text sorting, tagging, summarizing and report generation.
- Create a reference output PDF as a sample target
- ...
- Add cool stuff and make stuff better!

## MISC

- Google's (Vertext) Document AI is very interesting <https://cloud.google.com/document-ai#demo>. This will solve for Parsing, OCR and extraction from physical/scanned documents and otherwise. Some of this is overkill for needs here <https://cloud.google.com/vertex-ai>, since we don't need to do full, manual classifications, some of the provided text/document models seem to work very well. This *should* get us a decent output product.
- Visual Presentation adapter? We could generate additional presentation layers with a tool such as this <https://www.visme.co/>. This is probably overkill, but we could use the same data pool (db stored AI result) to generate visual presentations. If nothing else, I like the idea of using their charts/graphcs. Would be really nice to be able to do really simple charts/graphs, and insert them into the document. Generate pitchdeck/slides, as a secondary step, to be shared with others, w/ attached PDF report?

## Report Model Discussion

- And then I want it to generate: company overview, product overview, competitors, mgmt team bios (from Linkedin), fundraising history, questions for mgmt 
Mgmt team bios are typically in the form of like Name Role: previous roles of note (especially if they have sold previous companies or worked at other companies in related spaces), educational background + CEO, founders, etc
- Fundraising history should be in the form “company has raised a total of $XXX. Last round was a $XX round led by YY at a $ZZ post money valuation in MM-YY. Summary of the previous rounds ($xx, led by, valuation, date), and other key investors include aa, bb, cc
- It’s typically: revenue / scale / growth, key use cases, types of customers, customer breakdown by industry / concentration, GTM sales motion, sales efficiency, net dollar retention / gross dollar retention / churn, margin profile, bridge to breakeven, path to steady-stage ebitda margins, key items in their product roadmap moving forward, biggest levers for growth, capital needs / valuation expectations,  current burn, gaps in management team