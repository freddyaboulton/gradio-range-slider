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
      selected_min = parseFloat(event.target.value);
      if (selected_min > selected_max) {
        selected_max = selected_min;
      }
    }
  
    function handle_max_change(event) {
      selected_max = parseFloat(event.target.value);
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

    let initial_value = value;

    let range_input;


    // function set_slider_range(): void {
    //   const range = range_input;
    //   const min = Number(range.min) || 0;
    //   const max = Number(range.max) || 100;
    //   const val = Number(range.value) || 0;
    //   const percentage = ((val - min) / (max - min)) * 100;
    //   range.style.setProperty("--range_progress", `${percentage}%`);
	  // }

    function reset_value(): void {
      [selected_min, selected_max] = initial_value;
      // set_slider_range();
      gradio.dispatch("change");
      gradio.dispatch("release", value);
	}
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
			<div class="tab-like-container">
			  <input
          aria-label={`min input for ${label}`}
          data-testid="min-input"
          type="number"
          bind:value={selected_min}
          min={minimum}
          max={maximum}
          disabled={!interactive}
          on:pointerup={handle_release}
          on:blur={handle_release}
			  />
        <input
          aria-label={`max input for ${label}`}
          data-testid="max-input"
          type="number"
          bind:value={selected_max}
          min={minimum}
          max={maximum}
          disabled={!interactive}
          on:pointerup={handle_release}
          on:blur={handle_release}
      />
        <button
          class="reset-button"
          on:click={reset_value}
          disabled={!interactive}
          aria-label="Reset to default value"
        >
        ↺
      </button>
			</div>
		</div>
	  </div>
    <div class="slider_input_container">
      <span class="min_value">{minimum}</span>
      <div class="range-slider">
        <div class="range-bg"></div>
        <div class="range-line" style={rangeLine} class:disabled={!interactive} bind:this={range_input}></div>
        <input type="range" disabled={!interactive} min={minimum} max={maximum} {step} bind:value={selected_min} on:input={handle_min_change} on:pointerup={handle_release} />
        <input type="range" disabled={!interactive} min={minimum} max={maximum} {step} bind:value={selected_max} on:input={handle_max_change} on:pointerup={handle_release} />
      </div>
      <span class="max_value">{maximum}</span>
    </div>


</Block>

 <style>
    .wrap {
      display: flex;
      flex-direction: column;
      width: 100%;
	  }
    
    .head {
      margin-bottom: var(--size-2);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
    }

    .tab-like-container {
      display: flex;
      align-items: stretch;
      border: 1px solid var(--input-border-color);
      border-radius: var(--radius-sm);
      overflow: hidden;
      height: var(--size-6);
	}

  .slider_input_container {
		display: flex;
		align-items: center;
		gap: var(--size-2);
	}

    @media (max-width: 420px) {
      .head .tab-like-container {
        margin-bottom: var(--size-4);
      }
    }

    input[type="number"] {
      border: none;
      border-radius: 0;
      padding: var(--size-1) var(--size-2);
      height: 100%;
      min-width: var(--size-14);
      font-size: var(--text-sm);
      color: var(--body-text-color);
      background: var(--input-background-fill);
	}

	input[type="number"]:focus {
		box-shadow: none;
		border-width: 2px;
	}

    .range-slider {
      position: relative;
      width: 100%;
      height: var(--size-4);      
    }
  
    .range-slider input[type="range"] {
      position: absolute;
      left: 0;
      width: 100%;
      appearance: none;
      outline: none;
      background: transparent;
      pointer-events: none;
      top: 50%;
      transform: translateY(-50%);
      margin: 0;
    }
    .range-slider input[type="range"]::-webkit-slider-thumb {
      -webkit-appearance: none;
      appearance: none;
      height: var(--size-4);
      width: var(--size-4);
      background-color: white;
      border-radius: 50%;
      margin-top: 0;
      box-shadow:
			  0 0 0 1px rgba(247, 246, 246, 0.739),
			  1px 1px 4px rgba(0, 0, 0, 0.1);
      pointer-events: auto;
      cursor: pointer;
    }
    /* Uncomment to make slider look the same on firefox */
    .range-slider input[type="range"]::-moz-range-thumb {
      height: var(--size-4);
      width: var(--size-4);
      background-color: white;
      border-radius: 50%;
      border: none;
      box-shadow:
        0 0 0 1px rgba(247, 246, 246, 0.739),
        1px 1px 4px rgba(0, 0, 0, 0.1);
      pointer-events: auto;
      cursor: pointer;
    }

    .range-slider input[type="range"]::-moz-range-track {
      height: var(--size-2);
      background: transparent;
    }

    .min_value,
    .max_value {
      font-size: var(--text-sm);
      color: var(--body-text-color-subdued);
    }
  
    .range-line {
      position: absolute;
      left: 0;
      background: var(--slider-color);
      pointer-events: none;
      height: var(--size-2);
		  border-radius: var(--radius-xl);
    }

    .range-bg {
      position: absolute;
      left: 0;
      width: 100%;
      height: var(--size-2);
      z-index: 0;
      background: var(--neutral-200);
      pointer-events: none;
      border-radius: var(--radius-xl);
    }

    .range-line, .range-bg {
      top: 50%;
      transform: translateY(-50%);
    }

    .disabled {
		  background-color: var(--body-text-color-subdued);
	  }

    input[type="range"][disabled]::-webkit-slider-thumb {
		  cursor: not-allowed;
		  background-color: var(--body-text-color-subdued);
	  }

    input[type="range"][disabled]::-moz-range-thumb {
      background-color: var(--body-text-color-subdued);
    }

    input[type="number"][disabled] {
      cursor: not-allowed;
    }

    .reset-button {
		  display: flex;
      align-items: center;
      justify-content: center;
      background: none;
      border: none;
      border-left: 1px solid var(--input-border-color);
      cursor: pointer;
      font-size: var(--text-sm);
      color: var(--body-text-color);
      padding: 0 var(--size-2);
      min-width: var(--size-6);
      transition: background-color 0.15s ease-in-out;
	}

    .reset-button:hover:not(:disabled) {
      background-color: var(--background-fill-secondary);
    }

    .reset-button:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
</style>



