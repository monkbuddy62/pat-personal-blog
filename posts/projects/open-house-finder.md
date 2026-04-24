---
title: Building an open house scraper
date: April 2026
---

I go to a lot of open houses. Not because I'm buying — I work in real estate adjacent stuff and it's useful to meet agents in person. You show up, walk around, grab their card, have a two minute conversation. Do that enough Saturdays and you start to know people.

The problem is figuring out which open houses are happening and where. Redfin has the data but you have to dig for it. So I built a scraper.

It's a Python script using Playwright — a browser automation library that drives a real Chromium instance so the site doesn't block you like it would a raw HTTP request. You give it a Redfin neighborhood URL and it scrolls through all the listings, grabs each one, pulls the address, agent name, and open house time, and dumps everything into a SQLite database.

The anti-detection stuff was the most interesting part. Redfin is pretty aggressive about blocking scrapers. Random delays between requests, human-style scrolling, spoofing browser properties that automation frameworks expose. It works well enough for perstest test aosnajsdhojashdojhasd
aosjdoajshdo
asjdhoajshdojashdojahsodjahsodjhoasd
aosjdhaojsdh
