<script lang="ts">
	import { Label as LabelPrimitive } from "bits-ui";
	import { cn } from "$lib/utils.js";

	let {
		ref = $bindable(null),
		class: className,
		children,
		icon,
		...restProps
	}: LabelPrimitive.RootProps & {
		icon?: string;
	} = $props();
</script>

<LabelPrimitive.Root
	bind:ref
	data-slot="label"
	class={cn(
		"font-bold font-display tracking-widest uppercase flex items-center gap-2 text-xs text-primary leading-none select-none group-data-[disabled=true]:pointer-events-none group-data-[disabled=true]:opacity-50 peer-disabled:cursor-not-allowed peer-disabled:opacity-50",
		className
	)}
	{...restProps}
>
	{#if icon}
		<span class="material-symbols-outlined text-sm">{icon}</span>
	{/if}
	{@render children?.()}
</LabelPrimitive.Root>