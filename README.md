# Nina's Dilligence Automator (NDA)

This project aims to retrieve targetted data from sources, then sort, tag, and then generate a finalized report according to specifications.

**NDA** currently relies solely on web scraping as a means of collecting data. If additional documents are provided per target, we can OCR or parse with new adapters as needed. Consider an `./input` directory, and an `ingester` engine that combines useful data into the current collection.

## General Concept & Process Outline

NDA's general concept is to:

- Retrieve data from multiple sources for the target entity, and save all relevant data found, sorted, tagged and grouped into a collection.
- Process the data with an LLM capable of generating summaries as you desire.
- Generate a finalized report consisting of raw and processed data as required, according to output spec.

## Prerequisits

- Run `gcloud login` to authenticate with the gcloud API (used for Document AI processing). Install gcloud CLI if you don't already have it (<https://cloud.google.com/sdk/docs/install>). I recommend `gcloud components update` if your CLI hasn't been updated in some time.
- Run `auth.py` and follow the prompts to generate valid authentication sessions for each source. This will create a new `Chrome User Profile` called `NDA_Profile`.
- Verify valid write access in `./output` directory

## Getting Started

### Scraping

1. `pip install -r requirements`
2. `python auth.py`. Login to all sources where appropriate. Pay attention to the authentication status of each source as prompted.
3. `python scrape.py`. Generates output to `./output`.
4. TODO: Process results with AI and generate summaries.
5. TODO: Generate a report based on sample template(s).

Note: Output Data is sent to the `./output` folder, on a per-user and per-source basis.

### Processing & Generattion

- `python report.py <path_to_json_in_outputdir>` for Dynamic Report Generation
- `python process.py <path_to_pdf>` for `Document AI` processing.
- TODO: `python generate.py <input_path>` for Report generation.

TODO: DB Layer for cached data? We can always generate new reports with AI tool, based on stored/raw data (unless deleted). However, to avoid needless db hits, we could have a db/cache layer here. PG data (`jsonb`) or `mongodb` would work for sub-value filtering. Alternatively, a `redis` layer could save us a lot of hassle with pricing/free limits during dev, as target specific collection efforts may be persisted between scraping events.

## Process Description & Extensibility

Scraping is completed with a chrome driver *in browser*, with a `headless=False` flag. This is done to ensure simpler use of credential cookies (without storing credentials), and bypasses most basic bot detection. You will want to fine-tune the data stored for each source in the list to accommodate all data you require, and categorize each section correctly (tagged for AI).

Note: Running `auth.py` does a pre-run of each source domain to ensure a valid login before taking action. It is critical to verify the validity of authentication on each source before proceeding with any scraping. Complete proper login authentication on each source, as specified in the prompts.

For now, data is dumped into local `.json`/`.txt` documents for simpler use, found in our `./output` directory. At scale, this system would be replaced with a document store db with subtext searching, comparison, distancing and filtering features. Eventually, the AI tool will access this DB directly for data enrichment.

Collected data should then be sent for processing (OpenAI?) llm, ensuring the correct insights are summarized from the collected data. The processed data should be conformed into a template specification, either using template variable injection, or having OpenAI generate the report automatically based on a sample template.

NOTE: It would be ideal to provide a real `output.pdf` sample in this project source to be used as a reference. Also see `./models/samples`.

## Issues

### Login Sessions

Although we have the capability to save/load valid login sessions, we are electing to authenticate the user within a specified `Chrome User Profile`, for increased security, stealth and simplicity. Make sure to properly authenticate before running the scraper. Running `auth.py` will have you verify yourself on each source and save valid sessions in the browser profile.

### WebDriver Issues

If you have issues pertaining to the navigation of sources, further webdriver manipulation may be needed. To get started, you can try:
`brew install chromedriver`, then use the WebDriver library to instantiate a driver if you want shared session manipulation/access.

### Bot Detection & Workarounds

All scripting relies on currently active chrome sessions. We bypass bot detection by using a real browser instance and real sessions. Undetected-chromedriver will mask significant portions of the webdriver footprint. With this method, once authenticated under your normal chrome-user, we can retrieve and use the active sessions in our automation. No captchas, or strange behavior should catch us.

Running this from the cloud, or other easily identified ip blocks will trigger bot detection systems on most sources.

IMPORTANT: Our `undetected-chromedriver` WebDriver cannot access the same `Chrome Profile` that might currently be in-use as your normal browser. This is unfortunately due to the way Chrome handles locking writing in `User Directories` (<https://github.com/ultrafunkamsterdam/undetected-chromedriver/issues/586>). So, you must authenticate on all of the sources normally with `auth.py`, before running the `scrape.py` script. This way, one can load the Chrome Profile (that contains valid & active sessions).

TLDR: Run `auth.py`, and validation your authentication status by following the prompts, before running `scrape.py` to generate output.

## TODO

- Decide on list of scraping sites (`list.py`)
- Decide on HTML selectors on a per-site basis. Retrieve all data, tagged as appropriate. Make additional scraping calls if data is found on subsequent pages.
- Decide on standards for non-scraped data and add sample data to this project. Then create adapters to parse and aggregate them within the collection.
- OpenAI token or alternative/additional processing adapter for text sorting, tagging, summarizing and report generation.
- Create a reference output PDF as a sample target
- Create charts and graphs for output document
- Better Collection modeling. Need to better standardized grouped data, and tag as appropriate
- DB Layer for cached data
- ...
- Add cool stuff and make stuff better!

## MISC

- Google's (Vertext) Document AI is interesting <https://cloud.google.com/document-ai#demo>. This will solve for Parsing, OCR and extraction from physical/scanned documents and otherwise. Some of this is overkill for needs here <https://cloud.google.com/vertex-ai>, since we don't need to do full manual classifications. Some of the provided text/document models seem to work very well, particularly `AI Document Summarization`. This *should* get us a decent output product.
- Visual Presentation adapter? We could generate additional presentation layers with a tool such as this <https://www.visme.co/>. This is probably overkill, but we could use the same data collection to generate visual presentations. It would be nice to be able to do simple charts/graphs, and insert them into the document.

## Report Model Discussion

- And then I want it to generate: company overview, product overview, competitors, mgmt team bios (from Linkedin), fundraising history, questions for mgmt 
Mgmt team bios are typically in the form of like Name Role: previous roles of note (especially if they have sold previous companies or worked at other companies in related spaces), educational background + CEO, founders, etc
- Fundraising history should be in the form “company has raised a total of $XXX. Last round was a $XX round led by YY at a $ZZ post money valuation in MM-YY. Summary of the previous rounds ($xx, led by, valuation, date), and other key investors include aa, bb, cc
- It’s typically: revenue / scale / growth, key use cases, types of customers, customer breakdown by industry / concentration, GTM sales motion, sales efficiency, net dollar retention / gross dollar retention / churn, margin profile, bridge to breakeven, path to steady-stage ebitda margins, key items in their product roadmap moving forward, biggest levers for growth, capital needs / valuation expectations,  current burn, gaps in management team
