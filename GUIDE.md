# Daily Etsy publishing — 3 digital products per day (shop DElisaES)

Owner: Khaled. Report to him in Arabic at the end. Shop id 57330467, USD, Spain-based seller.

## Daily mix (decided by Gemini, Oct 21 2026; review after 30 days or 1000 visits)
- 2 products: caregiving / family logistics (aging parent, siblings sharing care, medication, appointments, home safety, moving a parent, hospital stay, caregiver self-care, school/family schedules, household admin).
- 1 product: New Year / Q1 planning (budget, savings challenges, goals, habit trackers, debt payoff, meal/expense planners).
- Prices: real prices $3.99–$8.99. NO inflated "was" price + big discount (EU reference-price rules).

## Quality rules (non-negotiable)
1. Check `log.json` and the shop's active listings (GET `/shops/57330467/listings/active?limit=100`, page with offset) — never repeat a product or a near-duplicate title.
2. Original content only: no copyrighted characters, trademarks, brand names, competitor copy, PLR.
3. Real, useful files: print-ready PDFs (US Letter + A4, ink-friendly, fillable lines/tables with real structure) and/or a working .xlsx with formulas you tested (open it with openpyxl / LibreOffice recalc and check values). No empty or filler pages.
4. Render every page to PNG and look at it before publishing (overflow, overlapping text, typos).
5. 4–5 listing images, 2700×2025 JPG/PNG. Image 1 = big readable text on mobile (product name + "what you get"), then page previews, what's included, how to use, sizes/FAQ.
6. English listing: title ≤140 chars (no ALL CAPS, no keyword stuffing, at most one "|" ), description with WHAT'S INSIDE / HOW IT WORKS / SIZES / NOTE (digital download, no physical item) and the line
   `• Created with the help of AI tools and checked before publishing.`
   13 tags, each ≤20 chars, comma-separated without spaces after commas. taxonomy_id 12476 (Planner Templates) unless a better digital taxonomy fits.
7. Put the buyer files in one ZIP (or upload ≤5 PDFs directly) named clearly.

## How to publish (all via Make tools, team 1232334)
1. Put each product's images + files in a folder, e.g. `media/A/…`, `media/B/…`, `media/C/…`.
2. Host them: `bash publish_media.sh media` (from this branch). It force-pushes them to branch `etsy-media` of khaledkorichi34/khaled-website and prints raw.githubusercontent.com URLs pinned to the commit SHA. (Needs push access — add the repo with access "push" first.) The sandbox cannot reach Make webhooks; Make downloads from these URLs.
3. Create draft: Make tool `s9902218_etsy_create_draft` (title, description, price, tags, taxonomy_id) → returns listing_id.
4. Images: run scenario **10019186** with `scenarios_run` (responsive true), data `{listing_id, image_url, rank, alt}` — one call per image, rank 1..n. Do calls sequentially-ish; Make returns "Too Many Requests" if hammered — wait and retry.
5. Files: scenario **10019189**, data `{listing_id, file_url, file_name}`.
6. Publish: `s9902221_etsy_set_listing_state` with state `active` (Khaled approved daily publishing of these 3 products on Oct 21 2026).
7. Verify: `s9902217_etsy_api_get` url `/listings/<id>?includes=Images` → state active, image count, then `/listings/<id>/files` (via shop path `/shops/57330467/listings/<id>/files`).
8. Append the 3 entries to `log.json` (date, listing_id, title, price, niche) and push this branch (`etsy-daily`).

## Limits
- Don't delete listings, spend money (no Etsy Ads, no paid tools) or change shop settings.
- Never paste API keys. If an Etsy/Make connection breaks, stop and tell Khaled what to reconnect.
- If something fails mid-way, leave the listing as a draft and report it — don't publish a listing missing images or files.

## Report (Arabic, short)
Three lines: title (English) – price – listing id/link `https://www.etsy.com/listing/<id>`; anything that failed; anything that needs Khaled.
