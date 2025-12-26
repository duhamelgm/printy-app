<script lang="ts">
	import { goto } from '$app/navigation';
	import authorizedPost from '$lib/authorizedPost';
	import Topbar from '$lib/components/shared/Topbar.svelte';
	import Button from '$lib/components/ui/button/button.svelte';

	let inputRef = $state<HTMLInputElement | null>(null);
	let imageFile = $state<File | null>(null);
	let imagePreview = $state<string | null>(null);
  let loading = $state(false);

	const onUpload = () => {
		inputRef?.click();
	};

	const handleFileChange = (e: Event) => {
		const file = (e.target as HTMLInputElement).files?.[0];

		if (file) {
			imageFile = file;
			imagePreview = URL.createObjectURL(file);
		}
	};

  const handleSubmit = async () => {
    loading = true;

    if (!imageFile) {
      return;
    }

    try {
      const formData = new FormData();
      formData.append('image', imageFile);

      const data = await authorizedPost('/v1/print/photo', formData, 'form-data');

      if (data.status === 'ok') {
        goto(`/print/success`);
      }
    } catch (error) {
      console.error(error);
    } finally {
      loading = false;
    }
  };
</script>

<div
	class="relative flex h-full min-h-screen w-full flex-col bg-background-light dark:bg-background-dark font-display text-white overflow-x-hidden selection:bg-synth-pink selection:text-white"
>
	<Topbar backHref="/print" />
	<!-- Main Scroll Content -->
	<main class="flex-1 overflow-y-auto px-4 pb-32">
		<!-- Headline -->
		<div class="flex flex-col items-center pt-6 pb-6">
			<h1
				class="text-transparent bg-clip-text bg-gradient-to-r from-white via-[#ffd6f9] to-primary text-[32px] font-bold leading-tight tracking-tight text-center drop-shadow-sm"
			>
				Capture the Glitch
			</h1>
			<p class="text-gray-300 text-sm font-normal leading-relaxed mt-2 text-center max-w-[280px]">
				Upload a photo or snap a picture of the issue to initiate the ticket sequence.
			</p>
		</div>
		<!-- Photo Drop Zone / Preview -->
		<div class="flex justify-center mt-4 mb-6">
			<Button size="lg" endIcon="photo_library" onclick={onUpload}>Upload from Gallery</Button>
		</div>

		<button
			class="w-full aspect-[4/5] max-h-[400px] relative group rounded-2xl overflow-hidden border-2 border-dashed border-primary/40 bg-black/20 hover:border-primary hover:shadow-neon transition-all duration-300 flex flex-col items-center justify-center cursor-pointer mb-6"
			onclick={onUpload}
		>
			<!-- Placeholder State -->
			<input
				type="file"
        capture
				accept="image/*"
				style="display: none;"
				bind:this={inputRef}
				onchange={handleFileChange}
			/>

			<!-- Preview -->
			{#if imagePreview}
				<div class="w-full h-full">
					<img src={imagePreview} alt="Preview" class="w-full h-full object-cover" />
				</div>
			{:else}
				<div
					class="flex flex-col items-center justify-center p-6 text-center space-y-4 group-hover:scale-105 transition-transform duration-300"
				>
					<div
						class="w-20 h-20 rounded-full bg-surface-dark border border-primary/30 flex items-center justify-center shadow-lg"
					>
						<span class="material-symbols-outlined text-primary text-[40px] animate-pulse">
							add_a_photo
						</span>
					</div>
					<div>
						<p class="text-white font-bold text-lg tracking-wide">TAP TO SNAP</p>
						<p class="text-primary/70 text-xs uppercase tracking-widest mt-1">
							or upload from grid
						</p>
					</div>
				</div>
			{/if}
		</button>
		<div class="flex justify-center">
			<Button size="lg" endIcon="center_focus_strong" onclick={handleSubmit}>Print the Capture</Button>
		</div>
	</main>
</div>
