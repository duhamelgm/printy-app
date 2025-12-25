<script lang="ts">
import { playAudio, stopAudio } from '$lib/musicPlayer';
import { onDestroy, onMount } from 'svelte';
import { setContext } from 'svelte';
import { writable } from 'svelte/store';
import { goto } from '$app/navigation';

let audio = writable<{
  audio: HTMLAudioElement;
  analyser: AnalyserNode | null;
  source: MediaElementAudioSourceNode | null;
  frequencyData: Float32Array | null;
} | null>(null);
let initialized = $state(false);
let { children } = $props();
let authToken = $state(localStorage.getItem("authToken"));

if(!authToken) {
  goto("/login");
}

onMount(() => {
  setContext('audio', audio);
  setContext("authToken", authToken);
});

onDestroy(() => {
  stopAudio();
  audio.set(null);
});

function onInitialize() {
  initialized = true;
  playAudio().then((audioData) => {
    audio.set(audioData);
  });
}
</script>

{#if initialized}
  {@render children()}
{:else}
  <div class="flex items-center justify-center h-full">
    <button class="bg-primary text-white px-4 py-2 rounded-md" onclick={onInitialize}
      >Initialize</button
    >
  </div>
{/if}
  