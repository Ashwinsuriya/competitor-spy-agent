import base64
from dotenv import load_dotenv
from groq import Groq

# 1. Load Secrets
load_dotenv()

# 2. Setup the Vision Brain
client = Groq()

def encode_image(image_file):
    """Turns an image file into a string of text (base64) so the AI can read it."""
    return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image(image_file):
    """Sends the image to Llama-4-Scout to extract data."""
    try:
        # A. Prepare the image
        base64_image = encode_image(image_file)
        
        # B. The Vision Prompt
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Analyze this screenshot of a pricing page or product interface. Extract all pricing tiers, features, and distinct numbers you see. Return the result as a clean Markdown table. Do not summarize, just extract exact data."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            # --- UPDATED MODEL NAME BELOW ---
            model="meta-llama/llama-4-scout-17b-16e-instruct", 
            temperature=0,
        )
        
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"❌ Vision Error: {str(e)}"