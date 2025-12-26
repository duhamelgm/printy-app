<script lang="ts">
	import { goto } from '$app/navigation';
	import { PUBLIC_API_URL } from '$env/static/public';
	import Button from '$lib/components/ui/button/button.svelte';
	import { getContext } from 'svelte';
	import type { Writable } from 'svelte/store';
	import * as Field from '$lib/components/ui/field';
	import * as InputOTP from '$lib/components/ui/input-otp';

	let inputToken = $state('');
	let interacted = getContext<Writable<boolean>>('interacted');
	let loading = $state(false);

	const onLogin = async (e: Event) => {
		e.preventDefault();
		loading = true;

		try {
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
		} catch (error) {
			console.error(error);
		} finally {
			loading = false;
		}
	};
</script>

<div class="relative flex h-full min-h-screen w-full flex-col overflow-hidden bg-[#050A14]">
	<!-- Decorative Background Elements -->
	<!-- Retro Floor Grid -->
	<div class="retro-grid bg-synth-grid opacity-30 pointer-events-none"></div>
	<!-- Top Gradient Glow -->
	<div
		class="absolute top-0 left-0 w-full h-64 bg-linear-to-b from-secondary/10 to-transparent pointer-events-none"
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
				<Field.Field>
					<div class="flex flex-col items-center gap-4">
						<Field.Label for="token" class="text-left w-full px-6">Auth Token</Field.Label>

						<InputOTP.Root maxlength={6} bind:value={inputToken}>
							{#snippet children({ cells })}
								<InputOTP.Group>
									{#each cells.slice(0, 3) as cell (cell)}
										<InputOTP.Slot {cell} />
									{/each}
								</InputOTP.Group>
								<InputOTP.Separator />
								<InputOTP.Group>
									{#each cells.slice(3, 6) as cell (cell)}
										<InputOTP.Slot {cell} />
									{/each}
								</InputOTP.Group>
							{/snippet}
						</InputOTP.Root>
					</div>
				</Field.Field>

				<Button disabled={loading} loading={loading} class="w-full mt-8" size="xl" type="submit">Login</Button>
			</form>
		</div>
	</div>
</div>
