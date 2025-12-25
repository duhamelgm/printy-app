<script lang="ts">
	import { playAudio, stopAudio } from '$lib/musicPlayer';
	import { getContext, onDestroy, onMount } from 'svelte';
	import { setContext } from 'svelte';
	import { writable, type Writable } from 'svelte/store';
	import { goto } from '$app/navigation';

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
	<div class="flex items-center justify-center h-full">
		<button class="bg-primary text-white px-4 py-2 rounded-md" onclick={onInitialize}>
			Initialize
		</button>
	</div>
{/if}
