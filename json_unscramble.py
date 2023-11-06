# Import libraries
import sys
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel
import transformers
import json

# Include huggingface access token to load in llama model.
access_token = ''

# Load in Llama-2-7b model using BitsAndBytes
model_id = "meta-llama/Llama-2-7b-hf"
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=False,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

model = AutoModelForCausalLM.from_pretrained(
            model_id,
            token=access_token,
            quantization_config=bnb_config,
            device_map={"":0})

tokenizer = AutoTokenizer.from_pretrained(model_id)

# Load fine-tune
peft_model = PeftModel.from_pretrained(model, "jackhogan/llama_agemo_finetune")

scrambled_json = sys.argv[1]

prompt = """
Below is a JSON string containing a syntactic error. Return the corrected JSON string.\n\n### Broken JSON:\n{}\n\n### Repaired JSON:\n
""".format(scrambled_json)

inputs = tokenizer(prompt, return_tensors='pt').to('cuda')
prompt_len = inputs['input_ids'].shape[1]
output_tokens = peft_model.generate(**inputs)

print('{' + '{'.join(tokenizer.decode(output_tokens.squeeze()[prompt_len:-1]).split('{')[1:]))
