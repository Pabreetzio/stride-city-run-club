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

## Events

Races, fun runs, socials, volunteer events, and other gatherings are an Astro **content collection** (`src/content/events/*.md`),
schema defined in `src/content.config.ts`. This replaced the old hardcoded
single-article events page.

**Adding an event:** drop a Markdown file in `src/content/events/`. Key
frontmatter: `title`, `description`, `date` (drives logic), optional `endDate`
(multi-day), `dateLabel` (human string shown to visitors), `location`,
`image` (a path into `src/assets/…`, optimized by `astro:assets`),
`registerUrl`, optional `category` (e.g. Race, Run, Social, or a new event kind), legacy `featured` (no longer needed), and an optional `details` array of
`{label, value}` rows rendered as a stat grid.

**Archiving is date-driven — preserve the event file, don't delete or move it.** `src/lib/events.ts` splits events
by date: an event is "past" once the end of its `date` (or `endDate`) day has
elapsed. Past events drop off the Upcoming list and appear on
`/events/archive`. After a fresh build/deploy, elapsed events appear in the archive; this Astro site is statically generated, so dates do not cause already-deployed HTML to refresh by themselves. Trigger a fresh deployment if past events are still showing as upcoming.

**Homepage Upcoming Events:** `getUpcomingEvents()` powers the section on the homepage and the Events page. Show **all** upcoming entries, sorted by start date/time, with no featured-only selection. If the list is empty, omit the entire homepage section (no empty-state message). Use `EventCard` for consistent display with and without images. The copy and CTAs must be event-neutral: not every event is a race or requires registration. Give each entry a `category` like `Race`, `Run`, `Social`, `Volunteer`, or another appropriate descriptive kind. Don't invent competition/team participation for informal events.

Pages: `/events` (upcoming + link to archive), `/events/archive` (past),
`/events/[slug]` (detail, via `src/layouts/EventPost.astro` +
`src/components/EventCard.astro`).

Event publishing workflow:
1. Confirm date, exact start time, venue address, packet-pickup and registration with the organizer's official site; prefer its registration URL over a generic landing page. Do not guess missing details. Specify time zone when ambiguity exists.
2. Add one `src/content/events/<event-slug>.md` per event, even when several events share a date. The `date` timestamp should represent the main event's start, for chronological ordering; use `dateLabel` to show multiple starts and secondary activity times. Cross-link same-day events where helpful.
3. Set a human-readable `category` for the event (Run/Race/Social/etc.). The homepage automatically shows every upcoming event, even those without images. Do not add or rely on `featured: true`.
4. Preserve completed event Markdown as historical content; check `/events/archive` after the next deployment. For a real recap, edit the existing past event's body with verified results/photos, avoiding unsubstantiated claims.
5. Run `npm run build`, deploy, and verify `/events`, `/events/archive`, and each new event detail page; on a static site the build time determines upcoming/past classification. A further deployment after race day refreshes classification.

Current events:
- `ctc-5k-showdown-2026.md` — upcoming Oct 17, 2026 morning 9 AM; morning race.
- `out-of-the-ashes-2026.md` — upcoming Oct 17, 2026 evening 5 PM 5K / 5:45 PM remembrance walk.
- `donut-run-2026-10-02.md` — past Oct 2 donut run; archived automatically on rebuild; keep file and details.
- `around-the-crown.md` — past (Sep 6 2026). Image is a 2023
  Around the Crown team photo (`src/assets/races/around-the-crown.jpg`).
- `run-jen-run.md` — past (Mar 21 2026, auto-archived). Go Jen Go breast-cancer
  benefit 5K at Symphony Park. Image `src/assets/races/run-jen-run.jpg` is the
  team-with-medals photo (originally "Photo Apr 14 2026").
- `run-the-south.md` — past (Jun 2026, auto-archived), no image.

Race photos live in `src/assets/races/` so `astro:assets` optimizes them; pass
`<Image>` a `width` only (no height) so portrait/landscape source aspect is
preserved and CSS `object-fit: cover` handles cropping.

Note: an older duplicate of the Run the South writeup still exists as a blog
post (`src/content/blog/run-the-south-with-stride-city.md`); the blog/News nav
is currently hidden.

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
