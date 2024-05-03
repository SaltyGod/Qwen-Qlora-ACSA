import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import pandas as pd
from tqdm import tqdm
from transformers import GenerationConfig
from prompt import SYSTEM_PROMPT
import json
from xtuner.utils import PROMPT_TEMPLATE

def load_model():
    print("loading the model...")
    model = (
        AutoModelForCausalLM.from_pretrained(
            MODEL_DIR, low_cpu_mem_usage=True, trust_remote_code=True
        )
        .to(torch.bfloat16)
        .cuda()
    )
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR, trust_remote_code=True)
    print("Done!")
    return model, tokenizer

# inference
def predict(question):
    gen_config = GenerationConfig(
        do_sample=True,
        temperature=0.01,
        max_new_tokens=380,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=(
            tokenizer.pad_token_id
            if tokenizer.pad_token_id is not None
            else tokenizer.eos_token_id
        ),
    )
    query = SYSTEM_PROMPT.format(question=question)
    prompt = PROMPT_TEMPLATE.default.get("INSTRUCTION").format(input=query)
    inputs = tokenizer([prompt], return_tensors="pt")
    inputs = {k: v.cuda() for k, v in inputs.items()}
    generate_ids = model.generate(**inputs, generation_config=gen_config)
    response = tokenizer.batch_decode(
        generate_ids[:, inputs["input_ids"].shape[1] :], skip_special_tokens=True
    )[0]
    return response