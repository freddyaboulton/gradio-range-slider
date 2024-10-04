
import gradio as gr
from gradio_rangeslider import RangeSlider
from pathlib import Path

text = "## The range is: {min} to {max}"

docs = Path(__file__).parent / "docs.md"

with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.Tab("Demo"):
            gr.Markdown("""## 🛝 RangeSlider

            ## Drag either end and see the selected endpoints update in real-time.
            """) 
            range_slider = RangeSlider(minimum=0, maximum=100, value=(0, 100))
            range_ = gr.Markdown(value=text.format(min=0, max=100))
            range_slider.change(lambda s: text.format(min=s[0], max=s[1]), range_slider, range_,
                                show_progress="hide", trigger_mode="always_last")
            gr.Slider(label="Normal slider", minimum=0, maximum=100, value=50, interactive=True)
            gr.Examples([(20, 30), (40, 80)], inputs=[range_slider])
        with gr.Tab("Docs"):
            gr.Markdown(docs.read_text())


if __name__ == "__main__":
    demo.launch()
