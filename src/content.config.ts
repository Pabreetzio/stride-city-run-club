import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const blog = defineCollection({
	// Load Markdown and MDX files in the `src/content/blog/` directory.
	loader: glob({ base: './src/content/blog', pattern: '**/*.{md,mdx}' }),
	// Type-check frontmatter using a schema
	schema: ({ image }) =>
		z.object({
			title: z.string(),
			description: z.string(),
			// Transform string to Date object
			pubDate: z.coerce.date(),
			updatedDate: z.coerce.date().optional(),
			heroImage: z.optional(image()),
		}),
});

const events = defineCollection({
	// Load Markdown/MDX files in `src/content/events/`.
	loader: glob({ base: './src/content/events', pattern: '**/*.{md,mdx}' }),
	schema: ({ image }) =>
		z.object({
			title: z.string(),
			description: z.string(),
			// `date` drives sorting and the upcoming/past split. `endDate` is for
			// multi-day events; when it passes, the event auto-moves to the archive.
			date: z.coerce.date(),
			endDate: z.coerce.date().optional(),
			// Human-friendly date/time string shown to visitors (the schema `date`
			// is only used for logic, so this can read however you like).
			dateLabel: z.string().optional(),
			location: z.string(),
			image: z.optional(image()),
			imageAlt: z.string().optional(),
			registerUrl: z.string().url().optional(),
			// Set true on the one race you want spotlighted on the homepage.
			featured: z.boolean().default(false),
			// Optional key/value rows rendered as a details grid on the event page.
			details: z.array(z.object({ label: z.string(), value: z.string() })).optional(),
		}),
});

export const collections = { blog, events };
