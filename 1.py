import gradio as gr

def process_url(url, word_count, image_count):
    # This function will be implemented later
    return f"Will process URL: {url} to extract {word_count} words and {image_count} images"

# Create the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Web Content Extractor")
    
    with gr.Row():
        url_input = gr.Textbox(label="Enter URL", placeholder="https://example.com")
    
    with gr.Row():
        word_count = gr.Number(label="Number of words to extract", value=100, minimum=1, step=1)
        image_count = gr.Number(label="Number of images needed", value=4, minimum=1, step=1)
    
    generate_btn = gr.Button("Generate")
    output = gr.Textbox(label="Output")
    
    # Connect the button to the processing function
    generate_btn.click(
        fn=process_url,
        inputs=[url_input, word_count, image_count],
        outputs=output
    )

if __name__ == "__main__":
    demo.launch()
