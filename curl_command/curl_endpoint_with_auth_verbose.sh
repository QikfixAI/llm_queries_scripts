#!/bin/bash

#INFERENCE_URL="https://inference.apps.ocp35.king.lab/demo/redhataiministral-3-3b-insllmd"
#MODEL="redhataiministral-3-3b-insllmd"
INFERENCE_URL="https://deepseek-r1-distill-qwen-15b-demo.apps.ocp35.king.lab"
MODEL="deepseek-r1-distill-qwen-15b"
YOUR_TOKEN=""

curl -k -v $INFERENCE_URL/v1/chat/completions \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $YOUR_TOKEN" \
      -d '{
        "model": "'$MODEL'",
        "messages": [
          {"role": "user", "content": "Hello, are you working?"}
        ],
        "max_tokens": 100
      }'
