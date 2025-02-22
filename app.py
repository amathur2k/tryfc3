import gradio as gr
from api_client import APIClient
import logging

logger = logging.getLogger(__name__)

def process_url(url: str, word_count: int, image_count: int) -> tuple[str, list[str]]:
    # Call the API
    result = APIClient.extract_content(url, word_count, image_count)
    
    # Check for errors
    if not result["success"]:
        return result["error"], []
    
    # Get the response
    api_response = result["response"]
    
    # Extract marketing statement and pictures
    marketing_statement = api_response.get("data", {}).get("marketing_statement", "No marketing statement available")
    pictures = api_response.get("data", {}).get("pictures", [])
    
    logger.info("Extracted marketing statement and pictures from response")
    
    return marketing_statement, pictures

# Create the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Web Content Extractor")
    
    with gr.Row():
        url_input = gr.Textbox(
            label="Enter URL", 
            placeholder="https://example.com",
            value="https://adenlandscaping.com/",
            interactive=True
        )
    
    # Clear URL input on focus
    url_input.focus(
        fn=lambda: "",
        outputs=url_input
    )
    
    with gr.Row():
        word_count = gr.Number(label="Number of words to extract", value=100, minimum=1, step=1)
        image_count = gr.Number(label="Number of images needed", value=4, minimum=1, step=1)
    
    generate_btn = gr.Button("Generate")
    
    with gr.Row():
        marketing_output = gr.Textbox(label="Marketing Statement", lines=5)
    
    with gr.Row():
        gallery = gr.Gallery(label="Extracted Images")
    
    # Connect the button to the processing function
    generate_btn.click(
        fn=process_url,
        inputs=[url_input, word_count, image_count],
        outputs=[marketing_output, gallery]
    )

if __name__ == "__main__":
    demo.launch(share=True) 