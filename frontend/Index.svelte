<script context="module">
	let _id = 0;
</script>

<script lang="ts">
	import type { Gradio } from "@gradio/utils";
	import { Block, BlockTitle } from "@gradio/atoms";
	import { StatusTracker } from "@gradio/statustracker";
	import type { LoadingStatus } from "@gradio/statustracker";

	export let gradio: Gradio<{
		change: number[];
		input: number[];
		clear_status: LoadingStatus;
    release: number[];
	}>;
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value: number[];
	export let label = gradio.i18n("slider.slider");
	export let info: string | undefined = undefined;
	export let container = true;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let minimum = 0;
	export let maximum = 100;
	export let step: number;
	export let show_label: boolean;
	export let interactive: boolean;
	export let loading_status: LoadingStatus;
	export let value_is_output = false;

    function handle_change(selected_min, selected_max): void {
	    value = [selected_min, selected_max];
      gradio.dispatch("change", [selected_min, selected_max]);
	  
      if (!value_is_output) {
		    gradio.dispatch("input", [selected_min, selected_max])
	    }
    }
  
    function handle_min_change(event) {
      selected_min = parseInt(event.target.value);
      if (selected_min > selected_max) {
        selected_max = selected_min;
      }
    }
  
    function handle_max_change(event) {
      selected_max = parseInt(event.target.value);
      if (selected_max < selected_min) {
        selected_min = selected_max;
      }
    }

    function handle_release(e: MouseEvent): void {
		  gradio.dispatch("release", value);
	}

	let old_value = value;
	let [selected_min, selected_max] = value;

	$: if (JSON.stringify(old_value) !== JSON.stringify(value)) {
		  [selected_min, selected_max] = value;
		  old_value = value;
	}

    $: handle_change(selected_min, selected_max);

    $: rangeLine = `
      left: ${( (selected_min - minimum) / (maximum - minimum)) * 100}%;
      width: ${ ((selected_max - selected_min) / (maximum - minimum)) * 100}%;
    `;
</script>

<Block {visible} {elem_id} {elem_classes} {container} {scale} {min_width}>
	<StatusTracker
		autoscroll={gradio.autoscroll}
		i18n={gradio.i18n}
		{...loading_status}
		on:clear_status={() => gradio.dispatch("clear_status", loading_status)}
	/>

    <div class="wrap">
		<div class="head">
			<BlockTitle {show_label} {info}>{label}</BlockTitle>
			<div class="numbers">
			  <input
				  aria-label={`max input for ${label}`}
				  data-testid="max-input"
				  type="number"
				  bind:value={selected_max}
				  min={minimum}
				  max={maximum}
				  disabled={!interactive}
          on:pointerup={handle_release}
			  />
			  <input
          aria-label={`min input for ${label}`}
          data-testid="min-input"
          type="number"
          bind:value={selected_min}
          min={minimum}
          max={maximum}
          disabled={!interactive}
          on:pointerup={handle_release}
			  />
			</div>
		</div>
	  </div>
	  <div class="range-slider">
		<div class="range-bg"></div>
		<div class="range-line" style={rangeLine}></div>
		<input type="range" disabled={!interactive} min={minimum} max={maximum} {step} bind:value={selected_min} on:input={handle_min_change} on:pointerup={handle_release} />
		<input type="range" disabled={!interactive} min={minimum} max={maximum} {step} bind:value={selected_max} on:input={handle_max_change} on:pointerup={handle_release} />
	  </div>
</Block>

 <style>
    .wrap {
      display: flex;
      flex-direction: column;
      width: 100%;
	  }
    
    .head {
      display: flex;
      justify-content: space-between;
    }

    .numbers {
	  	display: flex;
      flex-direction: row-reverse;
      max-width: var(--size-6);
	  }

    input[type="number"] {
        display: block;
        position: relative;
        outline: none !important;
        box-shadow: var(--input-shadow);
        border: var(--input-border-width) solid var(--input-border-color);
        border-radius: var(--input-radius);
        background: var(--input-background-fill);
        padding: var(--size-2) var(--size-2);
        height: var(--size-6);
        color: var(--body-text-color);
        font-size: var(--input-text-size);
        line-height: var(--line-sm);
        text-align: center;
	}

    .range-slider {
      position: relative;
      width: 100%;
      height: 30px;
    }
  
    .range-slider input[type="range"] {
      position: absolute;
      left: 0;
      bottom: 0;
      width: 100%;
      appearance: none;
      outline: none;
      background: transparent;
      pointer-events: none;
    }
  
    .range-slider input[type="range"]::-webkit-slider-thumb {
      appearance: none;
      width: 20px;
      height: 20px;
      background: white;
      border-radius: 50%;
      border: solid 0.5px #ddd;
      pointer-events: auto;
      cursor: pointer;
    }
  
    .range-slider input[type="range"]::-moz-range-thumb {
      width: 20px;
      height: 20px;
      background: white;
      border-radius: 50%;
      border: solid 0.5px #ddd;
      pointer-events: auto;
      cursor: pointer;
    }
  
    .range-line {
      position: absolute;
      left: 0;
      bottom: 8px;
      height: 4px;
      background: var(--slider-color);
      pointer-events: none;
    }

    .range-bg {
      position: absolute;
      left: 0;
      width: 100%;
      bottom: 8px;
      height: 4px;
      z-index: 0;
      background: var(--neutral-200);
      pointer-events: none;
    }
  
  </style>



