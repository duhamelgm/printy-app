<script lang="ts">
	import { goto } from '$app/navigation';
	import { PUBLIC_API_URL } from '$env/static/public';
	import Button from '$lib/components/ui/button/button.svelte';
	import { getContext } from 'svelte';
	import type { Writable } from 'svelte/store';

	let inputToken = $state('');
	let interacted = getContext<Writable<boolean>>('interacted');

	const onLogin = async (e: Event) => {
		e.preventDefault();

		const response = await fetch(`${PUBLIC_API_URL}/v1/auth/verify`, {
			method: 'POST',
			headers: {
				Authorization: inputToken
			}
		});

		const data = await response.json();
		if (data.status === 'ok') {
			localStorage.setItem('authToken', inputToken);
			interacted.set(true);
			goto('/');
		} else {
			alert('Invalid token');
		}
	};
</script>

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
		<!-- Login Form -->
		<div class="mt-4 sm:mx-auto sm:w-full sm:max-w-sm">
			<form action="#" class="space-y-6" method="POST" onsubmit={onLogin}>
				<!-- Password Field -->
				<div>
					<div class="flex items-center justify-between ml-1 mb-2">
						<label class="block text-sm font-medium leading-6 text-white/80" for="password">
							Auth Token
						</label>
					</div>
					<div
						class="relative mt-2 rounded-xl bg-surface-dark/80 backdrop-blur-sm neon-border-glow border border-[#315f68] transition-all duration-300"
					>
						<div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-4">
							<span class="material-symbols-outlined text-[#90c1cb]">lock</span>
						</div>
						<input
							autocomplete="current-password"
							class="block w-full rounded-xl border-0 bg-transparent py-4 pl-12 pr-12 text-white placeholder:text-[#90c1cb]/50 focus:ring-0 sm:text-base sm:leading-6"
							id="password"
							name="password"
							placeholder="Enter your auth token"
							required={true}
              bind:value={inputToken}
							type="password"
						/>
					</div>
				</div>
        <Button class="w-full" size="xl" type="submit">Login</Button>
			</form>
		</div>
	</div>
</div>
