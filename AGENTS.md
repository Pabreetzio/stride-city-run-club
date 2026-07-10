# AGENTS.md

Incidental project context for agents working on this repo. Not derivable from
the code alone — captured from what the site owner has mentioned.

## Project

- Stride City Run Club — community run club in Charlotte, NC. Astro site,
  deployed to Netlify (`stride-city-run-club.netlify.app`).
- Club meets Wednesdays 6:30pm at Edge City Brewery; base address is
  6697 Monroe Rd, Charlotte, NC 28212 (the "MoRA" / Monroe Road corridor, near
  the Oakhurst neighborhood and the Old Post Rd / Meridian Place shopping area).

## People

- **Ari** — the club organizer. Also works in real estate; her branding is
  "Move with Ari" / "Muévete con Ari" / "Sold on Running" (house + keyhole
  logo). Realtor site: https://www.keynchomes.com/home (Key NC Homes).
  Ari emailed over the sponsor logo artwork.

## Sponsors / Community Partners

- Source art: `brand-assets/Sponsors Logo.ai` — a single-page Illustrator/PDF
  Ari sent, containing all sponsor logos in a 2-column grid. Kept in
  `brand-assets/` (NOT `public/`) so the ~1MB source is not deployed with the
  site.
- Individual logos were extracted to `public/sponsors/*.png` by
  `brand-assets/extract_sponsors.py` (re-runnable; renders the PDF, segments
  each logo, trims + whitens the background, exports web-sized PNGs).
- Rendered on the homepage (`src/pages/index.astro`) as the "Our Community
  Partners" section — a data-driven `sponsors` array + a `.sponsor-grid` styled
  in `src/styles/home.scss`.
- Where a partner has a location near the club, the link points to that specific
  spot (Ari's request):

  | Sponsor | Link |
  | --- | --- |
  | Edge City Brewery | https://edgecitybrewery-clt.com/ |
  | Move with Ari (Key NC Homes) | https://www.keynchomes.com/home |
  | Hawthorne's NY Pizza & Bar (Old Post Rd / Meridian Place, 6215 Old Post Rd) | online-ordering page (order.online) — confirm preferred URL |
  | East Side Animal Hospital (6209 Old Post Rd) | https://eastsideahclt.com/ |
  | Anytime Fitness (Oakhurst, 1610 Oakhurst Commons Dr) | https://www.anytimefitness.com/locations/charlotte-north-carolina-4913 |
  | Monroe Road Advocates (MoRA) | https://moraclt.org/ |
  | Smoothie King (Old Post Rd, 6215 Old Post Rd) | https://locations.smoothieking.com/ll/us/nc/charlotte/6215-old-post-road-ste-102/ |
