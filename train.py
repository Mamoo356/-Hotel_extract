"""train.py
Simple LoRA-based fine-tuning script using 🤗 Transformers + PEFT
Replace MODEL_NAME_OR_PATH with your model or path.
"""
import os
import argparse
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from datasets import load_dataset
from peft import get_peft_model, LoraConfig, TaskType
import torch




def main():
parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, default=os.environ.get('MODEL_PATH','/path/to/llama'))
parser.add_argument('--data', type=str, required=True)
parser.add_argument('--output_dir', type=str, default='outputs/lora')
parser.add_argument('--epochs', type=int, default=3)
args = parser.parse_args()


model_name = args.model
print('Loading model', model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map='auto', torch_dtype=torch.float16)


# prepare dataset
ds = load_dataset('json', data_files={'train': args.data})['train']


# format dataset: concatenate prompt and output in an instruction-style prompt
def map_fn(example):
prompt = f"แปลงเป็น JSON schema:\nInput: {example['input']}\nOutput:"
example['text'] = prompt + ' ' + json.dumps(example['output'], ensure_ascii=False)
return example


ds = ds.map(map_fn)


# tokenization
def tok(x):
return tokenizer(x['text'], truncation=True, max_length=512)
ds = ds.map(tok, batched=True)
ds.set_format(type='torch', columns=['input_ids','attention_mask'])


# LoRA config
peft_config = LoraConfig(
task_type=TaskType.CAUSAL_LM,
inference_mode=False,
r=8,