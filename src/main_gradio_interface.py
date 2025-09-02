import gradio as gr
from rag_tools import process_query, generate_random_question

# Create the Gradio interface
with gr.Blocks(title="Diary Bot") as demo:
    gr.Markdown("""
    # Your Diary Bot Assistant
    Ask questions about anything that's in your diary! The Diary Bot will remember!
    """)
    
    with gr.Row():
        with gr.Column():
            question = gr.Textbox(
                label="What would you like to know about?",
                placeholder="e.g., When was the last time I called Grandma?",
                lines=3
            )
            with gr.Row():
                submit_btn = gr.Button("Ask")
                random_btn = gr.Button("🎲 Random Question")
        
        with gr.Column():
            response = gr.Textbox(
                label="Response",
                lines=10,
                show_copy_button=True
            )
    
    submit_btn.click(
        fn=process_query,
        inputs=question,
        outputs=response
    )
    
    question.submit(
        fn=process_query,
        inputs=question,
        outputs=response
    )
    
    random_btn.click(
        fn=generate_random_question,
        inputs=None,
        outputs=question
    )

if __name__ == "__main__":
    demo.launch() 

