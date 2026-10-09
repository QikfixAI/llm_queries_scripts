#!/bin/bash

#INFERENCE_URL="https://inference.apps.ocp35.king.lab/demo/redhataiministral-3-3b-insllmd"
#MODEL="redhataiministral-3-3b-insllmd"
INFERENCE_URL="https://deepseek-r1-distill-qwen-15b-demo.apps.ocp35.king.lab"
MODEL="deepseek-r1-distill-qwen-15b"
YOUR_TOKEN=""
MESSAGE="Hello, are you working?"
MAX_TOKENS=100

usage() {
  cat <<EOF
Usage: $(basename "$0") [options]

  -u, --url URL        Inference URL        (default: $INFERENCE_URL)
  -m, --model MODEL    Model name           (default: $MODEL)
  -t, --token TOKEN    Bearer token         (default: \$YOUR_TOKEN env var)
  -p, --message TEXT   User message         (default: $MESSAGE)
  -n, --max-tokens N   max_tokens           (default: $MAX_TOKENS)
  -h, --help           Show this help

Example:
  $(basename "$0") -u https://my-model.example.com -m my-model -t sha256~abc -p "Why is the sky blue?"
EOF
}

need_val() {
  if [ "$2" -lt 2 ]; then echo "Missing value for $1" >&2; exit 1; fi
}

# No arguments: show the help instead of firing a request with the defaults.
if [ $# -eq 0 ]; then
  usage
  exit 0
fi

while [ $# -gt 0 ]; do
  case "$1" in
    -u|--url)        need_val "$1" $#; INFERENCE_URL="$2"; shift 2 ;;
    -m|--model)      need_val "$1" $#; MODEL="$2";         shift 2 ;;
    -t|--token)      need_val "$1" $#; YOUR_TOKEN="$2";    shift 2 ;;
    -p|--message)    need_val "$1" $#; MESSAGE="$2";       shift 2 ;;
    -n|--max-tokens) need_val "$1" $#; MAX_TOKENS="$2";    shift 2 ;;
    -h|--help)       usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 1 ;;
  esac
done

# Build the JSON body with the values safely escaped.
if command -v jq >/dev/null 2>&1; then
  BODY=$(jq -n \
    --arg model "$MODEL" \
    --arg content "$MESSAGE" \
    --argjson max_tokens "$MAX_TOKENS" \
    '{model: $model, messages: [{role: "user", content: $content}], max_tokens: $max_tokens}') || {
      echo "Failed to build JSON body (is --max-tokens a number?)" >&2
      exit 1
    }
else
  json_escape() {
    printf '%s' "$1" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' | awk 'BEGIN{ORS=""} {print sep $0; sep="\\n"}'
  }
  BODY=$(cat <<EOF
{
  "model": "$(json_escape "$MODEL")",
  "messages": [
    {"role": "user", "content": "$(json_escape "$MESSAGE")"}
  ],
  "max_tokens": $MAX_TOKENS
}
EOF
)
fi

curl -k -s "$INFERENCE_URL/v1/chat/completions" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $YOUR_TOKEN" \
      -d "$BODY"
