import { getCollection, type CollectionEntry } from 'astro:content';

export type Event = CollectionEntry<'events'>;

/**
 * An event is "past" once the whole of its final day has elapsed. Using the end
 * of the day (rather than the raw start time) keeps a race listed as "upcoming"
 * through its own race day. This is what drives archiving — no manual step: once
 * the date passes, the event drops off the upcoming lists and appears in the
 * archive automatically.
 */
export function isPast(event: Event, now: Date = new Date()): boolean {
	const end = event.data.endDate ?? event.data.date;
	const endOfDay = new Date(end);
	endOfDay.setHours(23, 59, 59, 999);
	return endOfDay.getTime() < now.getTime();
}

/** Upcoming events, soonest first. */
export async function getUpcomingEvents(now: Date = new Date()): Promise<Event[]> {
	const events = await getCollection('events');
	return events
		.filter((e) => !isPast(e, now))
		.sort((a, b) => a.data.date.getTime() - b.data.date.getTime());
}

/** Past events, most recent first. */
export async function getPastEvents(now: Date = new Date()): Promise<Event[]> {
	const events = await getCollection('events');
	return events
		.filter((e) => isPast(e, now))
		.sort((a, b) => b.data.date.getTime() - a.data.date.getTime());
}

/**
 * The single event to spotlight on the homepage: the one flagged `featured`
 * among upcoming events, falling back to the soonest upcoming event, or null
 * when nothing is on the calendar.
 */
export async function getFeaturedEvent(now: Date = new Date()): Promise<Event | null> {
	const upcoming = await getUpcomingEvents(now);
	return upcoming.find((e) => e.data.featured) ?? upcoming[0] ?? null;
}
