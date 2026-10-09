#!/bin/env python

import argparse
import random
import httpx
from openai import OpenAI

# Client configuration — adjust these if you experience timeouts with RAG or large file uploads.
# timeout: Maximum seconds to wait for a response (default: 600s / 10 minutes).
# max_retries: Number of automatic retries on transient errors (default: 2).
MAX_RETRIES = 2
REQUEST_TIMEOUT = 600.0
FILES_BASE_PATH = ""
#input_text = "Hello, tell me something interesting about AI"
system_instructions = """You are a helpful AI assistant. You are designed to answer questions in a concise and professional manner.
"""


def parse_args():
    parser = argparse.ArgumentParser(description="Query an OpenAI-compatible inference endpoint.")
    parser.add_argument(
        "--ogx-url",
        default="https://inference.apps.ocp35.king.lab/demo/redhataiministral-3-3b-insllmd",
        help="Base URL of the inference endpoint.",
    )
    parser.add_argument(
        "--model-name",
        default="redhataiministral-3-3b-insllmd",
        help="Name of the model to query.",
    )
    parser.add_argument(
        "--token",
        default="something",
        help="API token for authentication.",
    )
    parser.add_argument(
        "--questions-file",
        required=True,
        help="Path to a text file with one question per line.",
    )
    return parser.parse_args()


def load_questions(path):
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def main():
    args = parse_args()

    questions = load_questions(args.questions_file)
    random.shuffle(questions)

    http_client = httpx.Client(verify=False)
    client = OpenAI(
        base_url=f"{args.ogx_url}/v1",
        api_key=args.token,
        max_retries=MAX_RETRIES,
        timeout=REQUEST_TIMEOUT,
        http_client=http_client,
    )

    for question in questions:
        config = {
            "input": question,
            "model": args.model_name,
            "instructions": system_instructions,
        }

        response = client.responses.create(**config)

        print("question>", question)
        print("agent>", response.output_text)
        print()


if __name__ == "__main__":
    main()






