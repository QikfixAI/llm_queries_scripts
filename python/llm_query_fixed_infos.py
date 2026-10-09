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

# Configuration adjust as needed:
#OGX_URL = "https://deepseek-r1-distill-qwen-15b-demo.apps.ocp35.king.lab"
OGX_URL = "https://inference.apps.ocp35.king.lab/demo/redhataiministral-3-3b-insllmd"
# Client configuration — adjust these if you experience timeouts with RAG or large file uploads.
# timeout: Maximum seconds to wait for a response (default: 600s / 10 minutes).
# max_retries: Number of automatic retries on transient errors (default: 2).
MAX_RETRIES = 2
REQUEST_TIMEOUT = 600.0
FILES_BASE_PATH = ""
input_text = "Hello, tell me something interesting about AI"
#model_name = "vllm-inference-1/deepseek-r1-distill-qwen-15b"
#model_name = "deepseek-r1-distill-qwen-15b"
model_name = "redhataiministral-3-3b-insllmd"
system_instructions = """You are a helpful AI assistant. You are designed to answer questions in a concise and professional manner.
"""

import os
import httpx

http_client = httpx.Client(verify=False)

from openai import OpenAI

API_TOKEN="something"

client = OpenAI(
             base_url=f"{OGX_URL}/v1", 
             api_key=API_TOKEN, 
             max_retries=MAX_RETRIES, 
             timeout=REQUEST_TIMEOUT, 
             http_client=http_client,
         )

config = {
    "input": input_text,
    "model": model_name,
    "instructions": system_instructions
}

response = client.responses.create(**config)

print("agent>", response.output_text)
