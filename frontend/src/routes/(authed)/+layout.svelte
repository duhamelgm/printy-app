<script lang="ts">
	import { playAudio, stopAudio } from '$lib/musicPlayer';
	import { getContext, onDestroy, onMount } from 'svelte';
	import { setContext } from 'svelte';
	import { writable, type Writable } from 'svelte/store';
	import { goto } from '$app/navigation';
	import Button from '$lib/components/ui/button/button.svelte';

	let audio = writable<{
		audio: HTMLAudioElement;
		analyser: AnalyserNode | null;
		source: MediaElementAudioSourceNode | null;
		frequencyData: Float32Array | null;
	} | null>(null);
	let { children } = $props();
	let authToken = $state(localStorage.getItem('authToken'));
	let interacted = getContext<Writable<boolean>>('interacted');

	if (!authToken) {
		goto('/login');
	}

	onMount(() => {
		setContext('audio', audio);
	});

	onDestroy(() => {
		stopAudio();
		audio.set(null);
	});

	$effect(() => {
		if ($interacted) {
			playAudio().then((audioData) => {
				audio.set(audioData);
			});
		}
	});

	function onInitialize() {
		interacted.set(true);
	}
</script>

{#if $interacted}
	{@render children()}
{:else}
<div class="relative flex h-full min-h-screen w-full flex-col overflow-hidden bg-[#050A14]">
	<!-- Decorative Background Elements -->
	<!-- Retro Floor Grid -->
	<div class="retro-grid bg-synth-grid opacity-30 pointer-events-none"></div>
	<!-- Top Gradient Glow -->
	<div
		class="absolute top-0 left-0 w-full h-64 bg-gradient-to-b from-secondary/10 to-transparent pointer-events-none"
	></div>
	<!-- Main Content Wrapper -->
	<div class="relative z-10 flex flex-1 flex-col mt-20 px-6 py-12 lg:px-8">
		<!-- Header Section -->
		<div class="sm:mx-auto sm:w-full sm:max-w-sm mb-10 text-center">
			<!-- Logo Icon Placeholder (Material Symbol) -->
			<div
				class="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-surface-dark border border-primary/30 shadow-[0_0_15px_rgba(13,204,242,0.3)]"
			>
				<span class="material-symbols-outlined text-4xl text-primary neon-text-glow">
					confirmation_number
				</span>
			</div>
			<h1 class="text-white tracking-widest text-[42px] font-bold leading-tight neon-text-glow">
				PRINTY
			</h1>
			<h2 class="mt-2 text-primary/80 text-lg font-medium tracking-[0.2em] uppercase">
				Access the Grid
			</h2>
		</div>
		<Button class="w-full" size="xl" onclick={onInitialize}>Initialize</Button>
	</div>
</div>
{/if}
