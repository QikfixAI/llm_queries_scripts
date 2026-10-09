# llm_queries_scripts

A small collection of scripts for querying OpenAI-compatible inference endpoints
(OGX / vLLM / Red Hat AI model serving). They range from quick hardcoded
smoke tests to fully parameterized CLI tools, and cover plain text prompts,
batch prompting from a file, and vision (image description).

All scripts talk to the `/v1` OpenAI-compatible API and skip TLS verification
(`curl -k` / `httpx.Client(verify=False)`), since they are aimed at lab
deployments using self-signed certificates.

## How to start

First, let's clone the repo

```bash
% git clone https://github.com/QikfixAI/llm_queries_scripts.git
% cd llm_queries_scripts
```

You should have the structure below
```
├── curl_command
│   ├── curl_endpoint_with_auth_verbose_all_parameters.sh
│   ├── curl_endpoint_with_auth_verbose.sh
│   └── curl_endpoint_without_auth_verbose.sh
├── LICENSE
├── python
│   ├── llm_query_describing_picture_from_file_or_folder_all_parameters.py
│   ├── llm_query_describing_picture_from_folder.py
│   ├── llm_query_describing_picture.py
│   ├── llm_query_fixed_infos.py
│   ├── llm_query_parameters_input_from_file.py
│   ├── llm_query_parameters.py
│   ├── photo
│   │   ├── car.jpg
│   │   ├── cat.jpg
│   │   ├── dog.jpg
│   │   └── tree.png
│   └── random_questions.txt
└── README.md
```

## Layout

```
curl_command/   Shell smoke tests using plain curl
python/         Python scripts using the OpenAI SDK
python/photo/   Sample images used by the vision scripts
```

## curl_command/

Minimal `curl` calls against `/v1/chat/completions` — useful for checking that
an endpoint is up and answering before involving any SDK.

| Script | Purpose |
| --- | --- |
| `curl_endpoint_without_auth_verbose.sh` | Sends a fixed "Hello, are you working?" prompt with no `Authorization` header. Edit `INFERENCE_URL` / `MODEL` at the top. Runs with `-v` so you see the full request/response exchange. |
| `curl_endpoint_with_auth_verbose.sh` | Same as above, plus an `Authorization: Bearer $YOUR_TOKEN` header. Set `YOUR_TOKEN` at the top of the file. |
| `curl_endpoint_with_auth_verbose_all_parameters.sh` | The parameterized version: URL, model, token, message, and `max_tokens` all come from command-line flags. Builds the JSON body with `jq` when available and falls back to manual escaping otherwise. Prints usage when run with no arguments. |

Example:

```bash
./curl_command/curl_endpoint_with_auth_verbose_all_parameters.sh \
  -u https://my-model.example.com \
  -m my-model \
  -t sha256~abc \
  -p "Why is the sky blue?"
```

## python/

Requires the OpenAI Python SDK and httpx:

```bash
python -m venv ~/.venv/llm_queries_scripts
source ~/.venv/llm_queries_scripts/bin/activate
(llm_queries_scripts) % pip install openai httpx
```

### Text queries

| Script | Purpose |
| --- | --- |
| `llm_query_fixed_infos.py` | Everything hardcoded at the top of the file (URL, model, token, prompt, system instructions). The simplest starting point — edit the constants and run it. Uses the Responses API (`client.responses.create`). |
| `llm_query_parameters.py` | Same single-query flow, driven by flags instead: `--ogx-url` and `--model-name` are required, plus `--msg` for the question and an optional `--token`. |
| `llm_query_parameters_input_from_file.py` | Batch mode: reads one question per line from `--questions-file`, shuffles them, and sends each to the model in turn, printing question and answer pairs. URL, model, and token have lab defaults. |

Examples:

```bash
python python/llm_query_parameters.py \
  --ogx-url https://my-model.example.com \
  --model-name my-model \
  --msg "Tell me something interesting about AI"

python python/llm_query_parameters_input_from_file.py \
  --questions-file python/random_questions.txt
```

### Vision / image description

These use the Chat Completions API and send images inline as base64 data URLs
(`.jpg`, `.jpeg`, `.png`).

| Script | Purpose |
| --- | --- |
| `llm_query_describing_picture.py` | Describes one image. Path and all settings are hardcoded (`IMAGE_FILE_PATH`, defaults to `photo/tree.png`). |
| `llm_query_describing_picture_from_folder.py` | Walks every image in `FILES_BASE_PATH` (defaults to `photo/`) and describes each one, printing the filename as a header. Still hardcoded configuration. |
| `llm_query_describing_picture_from_file_or_folder_all_parameters.py` | The parameterized version: `--file` or `--folder` (mutually exclusive, one required), plus `--ogx-url`, `--model-name`, `--token`, and `--msg` to change the question asked about each image. |

Examples:

```bash
python python/llm_query_describing_picture_from_file_or_folder_all_parameters.py --folder python/photo
python python/llm_query_describing_picture_from_file_or_folder_all_parameters.py \
  --file python/photo/cat.jpg --msg "What breed is this?"
```

Note: the hardcoded vision scripts resolve `photo/` relative to the current
directory, so run them from inside `python/`.

### Data files

| Path | Purpose |
| --- | --- |
| `python/random_questions.txt` | 5,000 plain questions, one per line — the input for `llm_query_parameters_input_from_file.py`. |
| `python/photo/` | Sample images (`car.jpg`, `cat.jpg`, `dog.jpg`, `tree.png`) for the vision scripts. |

## Notes

- Model names and URLs throughout default to a specific lab environment
  (`*.apps.ocp35.king.lab`); override them with the flags or edit the constants.
- Token defaults are placeholders (`"something"`, `"unused"`) that work against
  endpoints which do not enforce authentication.
- TLS verification is disabled in every script. Do not point these at anything
  you do not control without changing that.

## License

See [LICENSE](LICENSE).


Feel free to share feedback, ideas, new scripts. Go on under issues, and submit a new request, or just email me at waldirio@gmail.com

Thank you!<br>
Waldirio