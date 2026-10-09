# OGX Quickstart Script
#
# README:
# This example shows how to configure an assistant using the OpenAI Python SDK.
# Before using this code, make sure of the following:
#
# Required Packages:
#    - Install the required dependencies using pip:
#      pip install openai
#
# OGX Server:
#    - Your OGX instance must be running and accessible
#    - Set the OGX_URL variable to the base URL of your OGX server
#
# Model Configuration:
#    - The selected model (e.g., "llama3.2:3b") must be available in your OGX deployment with the correct API key.
#
# Tools (MCP Integration):
#    - Any tools used must be properly pre-configured in your OGX setup.
#
# Vision (Image Input):
#    - Set FILES_BASE_PATH to a directory of local image files (.jpg/.jpeg/.png)
#    - Each image will be base64-encoded and passed to the model in turn

# Configuration adjust as needed:
OGX_URL = "https://redhataigemma-4-12b-it-fp8-dyn-demo.apps.ocp35.king.lab"
#OGX_URL = "https://redhataigemma-4-12b-it-nvfp4-demo.apps.ocp35.king.lab"
# Client configuration — adjust these if you experience timeouts with RAG or large file uploads.
# timeout: Maximum seconds to wait for a response (default: 600s / 10 minutes).
# max_retries: Number of automatic retries on transient errors (default: 2).
MAX_RETRIES = 2
REQUEST_TIMEOUT = 600.0
FILES_BASE_PATH = "photo"  # Directory containing image files (.jpg/.jpeg/.png)
input_text = "Describe the image"
#model_name = "redhataigemma-4-12b-it-nvfp4"
model_name = "redhataigemma-4-12b-it-fp8-dyn"
system_instructions = """You are a helpful AI assistant. You are designed to answer questions in a concise and professional manner.
"""

import os
import mimetypes
import httpx
import base64
from openai import OpenAI

http_client = httpx.Client(verify=False)

client = OpenAI(base_url=f"{OGX_URL}/v1", api_key="unused", max_retries=MAX_RETRIES, timeout=REQUEST_TIMEOUT, http_client=http_client)

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}

image_files = sorted(
    f for f in os.listdir(FILES_BASE_PATH)
    if os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS
)

if not image_files:
    raise SystemExit(f"No images found in {FILES_BASE_PATH!r}")

for filename in image_files:
    image_path = os.path.join(FILES_BASE_PATH, filename)
    mime_type = mimetypes.guess_type(image_path)[0] or "image/jpeg"

    with open(image_path, "rb") as image_file:
        b64_image = base64.b64encode(image_file.read()).decode("utf-8")

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_instructions},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": input_text},
                    {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{b64_image}"}},
                ],
            },
        ],
    )

    print(f"=== {filename} ===")
    print("agent>", response.choices[0].message.content)
    print()
