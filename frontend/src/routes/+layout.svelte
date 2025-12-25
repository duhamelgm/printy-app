<script lang="ts">
import '../app.css';

import favicon from '$lib/assets/favicon.svg';
import { writable } from 'svelte/store';
import { setContext } from 'svelte';

const interacted = writable(false);
setContext('interacted', interacted);

let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<link
		href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap"
		rel="stylesheet"
	/>
	<link
		href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;700&amp;family=Noto+Sans:wght@400;500;700&amp;display=swap"
		rel="stylesheet"
	/>
	<link
		href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap"
		rel="stylesheet"
	/>
</svelte:head>

{@render children()}