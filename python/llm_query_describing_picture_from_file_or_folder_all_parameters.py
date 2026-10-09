#!/bin/env python
#
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
#    - Set --ogx-url to the base URL of your OGX server
#
# Model Configuration:
#    - The selected model (e.g., "llama3.2:3b") must be available in your OGX deployment with the correct API key.
#
# Tools (MCP Integration):
#    - Any tools used must be properly pre-configured in your OGX setup.
#
# Vision (Image Input):
#    - Use --folder to point to a directory of local image files (.jpg/.jpeg/.png)
#    - Or use --file to describe a single image
#    - Each image will be base64-encoded and passed to the model in turn
#
# Examples:
#    ./llm_query_describing_picture_from_folder.py --folder photo
#    ./llm_query_describing_picture_from_folder.py --file photo/cat.jpg --msg "What breed is this?"
#    ./llm_query_describing_picture_from_folder.py --ogx-url https://my.server --model-name my-model --folder photo

import argparse
import base64
import mimetypes
import os

import httpx
from openai import OpenAI

# Client configuration — adjust these if you experience timeouts with RAG or large file uploads.
# timeout: Maximum seconds to wait for a response (default: 600s / 10 minutes).
# max_retries: Number of automatic retries on transient errors (default: 2).
MAX_RETRIES = 2
REQUEST_TIMEOUT = 600.0
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
system_instructions = """You are a helpful AI assistant. You are designed to answer questions in a concise and professional manner.
"""


def parse_args():
    parser = argparse.ArgumentParser(description="Describe images using an OpenAI-compatible vision endpoint.")
    parser.add_argument(
        "--ogx-url",
        default="https://redhataigemma-4-12b-it-fp8-dyn-demo.apps.ocp35.king.lab",
        help="Base URL of the inference endpoint.",
    )
    parser.add_argument(
        "--model-name",
        default="redhataigemma-4-12b-it-fp8-dyn",
        help="Name of the model to query.",
    )
    parser.add_argument(
        "--token",
        default="unused",
        help="API token for authentication.",
    )
    parser.add_argument(
        "--msg",
        default="Describe the image",
        help="Question to ask about each image. Don't forget the \"\"",
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument(
        "--folder",
        help="Directory containing image files (.jpg/.jpeg/.png).",
    )
    source.add_argument(
        "--file",
        help="Path to a single image file.",
    )
    return parser.parse_args()


def collect_images(args):
    if args.file:
        if not os.path.isfile(args.file):
            raise SystemExit(f"Not a file: {args.file!r}")
        return [args.file]

    if not os.path.isdir(args.folder):
        raise SystemExit(f"Not a directory: {args.folder!r}")

    images = sorted(
        os.path.join(args.folder, f)
        for f in os.listdir(args.folder)
        if os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS
    )

    if not images:
        raise SystemExit(f"No images found in {args.folder!r}")

    return images


def main():
    args = parse_args()

    image_paths = collect_images(args)

    http_client = httpx.Client(verify=False)
    client = OpenAI(
        base_url=f"{args.ogx_url}/v1",
        api_key=args.token,
        max_retries=MAX_RETRIES,
        timeout=REQUEST_TIMEOUT,
        http_client=http_client,
    )

    for image_path in image_paths:
        mime_type = mimetypes.guess_type(image_path)[0] or "image/jpeg"

        with open(image_path, "rb") as image_file:
            b64_image = base64.b64encode(image_file.read()).decode("utf-8")

        response = client.chat.completions.create(
            model=args.model_name,
            messages=[
                {"role": "system", "content": system_instructions},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": args.msg},
                        {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{b64_image}"}},
                    ],
                },
            ],
        )

        print(f"=== {os.path.basename(image_path)} ===")
        print("agent>", response.choices[0].message.content)
        print()


if __name__ == "__main__":
    main()
