<script lang="ts">
	import Topbar from '$lib/components/shared/Topbar.svelte';
	import authorizedPost from '$lib/authorizedPost';
	import { goto } from '$app/navigation';
	import * as Field from '$lib/components/ui/field';
	import { Input } from '$lib/components/ui/input';
	import { Textarea } from '$lib/components/ui/textarea';
	import Button from '$lib/components/ui/button/button.svelte';

	let title = $state('');
	let description = $state('');
	let assignee = $state('');
	let priority = $state('medium');
	let loading = $state(false);

	const onSubmit = async (e: Event) => {
		e.preventDefault();
		loading = true;
		const payload = {
			title,
			description,
			assignee,
			priority
		};
		console.log(payload);

		try {
			const response = await authorizedPost('/v1/print/ticket', payload);
			console.log(response);
		} catch (error) {
			console.error(error);
		} finally {
			loading = false;
		}

		goto('/print/success');
	};
</script>

<div
	class="relative flex items-center h-full min-h-screen w-full flex-col bg-background-light dark:bg-background-dark font-display text-white overflow-x-hidden selection:bg-synth-pink selection:text-white"
>
	<Topbar backHref="/print" />
	<div class="h-full overflow-y-auto w-full max-w-[600px] mx-auto">
		<form onsubmit={onSubmit}>
			<div class="flex-1 flex flex-col relative z-10 p-4 space-y-6">
				<!-- Welcome/Hero Text -->
				<div class="pt-2 pb-4">
					<h1
						class="text-3xl font-black text-transparent bg-clip-text bg-linear-to-r from-white via-blue-100 to-white tracking-tight drop-shadow-[0_0_10px_rgba(19,91,236,0.5)]"
					>
						New Ticket
					</h1>
					<p class="text-blue-200/60 text-sm mt-1 font-medium tracking-wide">
						ENTER MISSION PARAMETERS
					</p>
				</div>
				<!-- Title Input -->
				<Field.Field>
					<Field.Label icon="edit" for="title">Subject Line</Field.Label>
					<Input required name="title" bind:value={title} type="text"/>
				</Field.Field>

				<Field.Field>
					<Field.Label icon="description" for="description">Description</Field.Label>
					<Textarea name="description" bind:value={description} class="min-h-[120px]"/>
				</Field.Field>

				<Field.Field>
					<Field.Label icon="person_add" for="assignee">Operative</Field.Label>
					<Input required name="assignee" bind:value={assignee} type="text"/>
				</Field.Field>

				<Field.Field>
					<Field.Label icon="warning" for="assignee">Urgency Level</Field.Label>
					<div class="grid grid-cols-3 gap-3">
						<Button variant="outline" size="xl" onclick={() => priority = 'low'} class={`text-sm h-12 border-primary/30 bg-primary/5 hover:bg-primary/10 hover:text-primary ${priority === 'low' ? 'border-primary bg-primary/20 shadow-neon-blue' : ''}`}>Low</Button>
						<Button variant="outline" size="xl" onclick={() => priority = 'medium'} class={`text-sm h-12 border-primary/30 bg-primary/5 hover:bg-primary/10 hover:text-primary ${priority === 'medium' ? 'border-primary bg-primary/20 shadow-neon-blue' : ''}`}>Medium</Button>
						<Button variant="outline" size="xl" onclick={() => priority = 'high'} class={`text-sm h-12 border-primary/30 bg-primary/5 hover:bg-primary/10 hover:text-primary ${priority === 'high' ? 'border-primary bg-primary/20 shadow-neon-blue' : ''}`}>High</Button>
					</div>
				</Field.Field>
			</div>
			<!-- Floating Action Button Area -->
			<div class="w-full p-4 from-[#050510] via-[#050510]/95 to-transparent z-40 pb-8">
				<Button
					size="lg"
					endIcon="rocket_launch"
					onclick={onSubmit}
					disabled={loading}
					class="w-full"
					type="submit"
				>
					Transmit Ticket
				</Button>
			</div>
		</form>
	</div>
</div>
