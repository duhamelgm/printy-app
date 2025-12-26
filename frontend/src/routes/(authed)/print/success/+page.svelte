<script lang="ts">
	import Topbar from '$lib/components/shared/Topbar.svelte';
	import { Button } from '$lib/components/ui/button';
</script>

<style>
	.neon-text-glow {
		text-shadow: 0 0 10px rgba(13, 204, 242, 0.5), 0 0 20px rgba(13, 204, 242, 0.3);
	}
</style>

<div class="relative flex h-full w-full flex-col justify-between overflow-hidden bg-background-dark">
	<Topbar backHref="/print" />

	<div class="relative z-10 flex-1 flex flex-col items-center justify-center px-6 w-full max-w-md mx-auto mt-36">
		<div class="relative mb-8 group">
			<div class="absolute -inset-4 bg-linear-to-tr from-primary to-neon-purple rounded-full blur-xl opacity-40 group-hover:opacity-60 transition-opacity duration-1000 animate-pulse"></div>
			<div class="relative flex items-center justify-center w-32 h-32 rounded-full bg-background-dark border-2 border-primary shadow-[0_0_30px_rgba(13,204,242,0.3)]">
				<span class="material-symbols-outlined text-6xl text-primary drop-shadow-[0_0_10px_rgba(13,204,242,0.8)]">
					check_circle
				</span>
			</div>
		</div>

		<div class="text-center space-y-4">
			<h1 class="text-white tracking-wide text-4xl font-bold leading-tight px-4 text-center neon-text-glow uppercase">
				Ticket<br/>Transmitted
			</h1>
			<p class="text-gray-300 text-lg font-normal leading-relaxed px-4 text-center max-w-xs mx-auto">
				Your request has been successfully beamed to the print server queue.
			</p>
		</div>
	</div>

	<div class="relative z-10 w-full px-6 pb-10 pt-4 flex flex-col gap-3 max-w-md mx-auto mt-8">
		<Button
			href="/print"
			variant="outline"
			size="xl"
			class="w-full rounded-xl bg-[#1a2f33]/50 border-white/10 hover:bg-[#1a2f33] hover:text-white"
		>
			Done
		</Button>
	</div>
</div>
