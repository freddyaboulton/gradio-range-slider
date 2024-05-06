<script lang="ts">
	export let value: number[];
	export let type: "gallery" | "table";
	export let selected = false;

	let [min, max] = value;
</script>

<div
	class:table={type === "table"}
	class:gallery={type === "gallery"}
	class:selected
>
	[{min}, {max}]
</div>

<style>
	.gallery {
		padding: var(--size-1) var(--size-2);
	}
</style>
