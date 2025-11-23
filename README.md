# Hotel Booking — LLaMA training + Streamlit tester


This repo contains scripts to:
- generate a synthetic Thai dataset of ~200 booking sentences (`dataset/generate_dataset.py`)
- train / fine-tune a causal LLM using LoRA (placeholder model path — replace with your LLaMA 3.1 8B checkpoint or other local model)
- run a Streamlit app to test the trained model (`app.py`) which shows the predicted JSON and inference time


> **Important**: This repo does *not* include model weights. Provide `MODEL_PATH` as an env var or HF repo name. If you plan to fine-tune LLaMA 3.1 you must ensure licensing and access.


## Quick start (developer machine without Docker)


1. Create virtualenv


```bash
python -m venv .venv
source .venv/bin/activate # Windows: .venv\Scripts\activate
pip install -r requirements.txt

2. Generate dataset (200 samples):
python dataset/generate_dataset.py --n 200 --out dataset/dataset.jsonl

3.(Optional) Train / fine-tune model using LoRA
export MODEL_PATH="/path/to/your/llama-3.1-8b-or-local"
python train.py --data dataset/dataset.jsonl --output_dir outputs/lora_checkpoint

4.Run Streamlit tester
export MODEL_PATH="/path/to/your/llama-3.1-8b-or-local"
streamlit run app.py

Notes

The trainer uses transformers + peft LoRA to avoid heavy full fine-tuning. Replace MODEL_NAME_OR_PATH with the actual path or HF repo.

app.py uses the same model via from_pretrained and applies simple post-processing to force a JSON schema.

Preprocessing uses Thai tokenization (pythainlp), dateparser to parse Thai/relative dates, and RapidFuzz for fuzzy fixes.