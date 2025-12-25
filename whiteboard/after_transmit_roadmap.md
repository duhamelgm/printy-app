## Goal
After ticket transmit → redirect to new page

## Stack
- **SvelteKit** - meta-framework (like Next.js for React)
- **Svelte 5** - UI library with reactivity via runes ($state, $derived)
- **Tailwind** - styling
- **Three.js** - 3D stuff (via Threlte)

## Routing (SvelteKit file-based)
```
frontend/src/routes/
├── +page.svelte              → /
├── print/
│   ├── +page.svelte          → /print
│   └── ticket/
│       └── +page.svelte      → /print/ticket  ← transmit form is here
```

**How it works:**
- File name = route: `+page.svelte` in folder = page
- Create folder with `+page.svelte` → instant route
- Navigate: import `goto` from `$app/navigation`, call `goto('/path')`

## Locating files
- **Pages:** `frontend/src/routes/**/*.svelte`
- **Components:** `frontend/src/lib/components/`
- **Config:** `frontend/src/env/` or root config files
- **Transmit code:** [frontend/src/routes/print/ticket/+page.svelte:11-36](frontend/src/routes/print/ticket/+page.svelte#L11-L36)

## Next steps
1. Create new success page (where to redirect?)
2. Add redirect after successful transmit
