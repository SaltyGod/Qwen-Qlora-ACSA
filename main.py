import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import pandas as pd
from tqdm import tqdm
from transformers import GenerationConfig
from prompt import SYSTEM_PROMPT
import json
from xtuner.utils import PROMPT_TEMPLATE
import os
from sklearn.metrics import precision_recall_fscore_support

from GenerateData import read_data,map_dataset
from model import load_model,predict
from Evaluate import evaluate_performance,save_results_to_txt

if __name__=='__main__':
    # generate data
    DocList = ['train','dev','test']
    read_data(DocList)
    map_dataset("./data/modified_dev.csv", "./data/train.jsonl")
    map_dataset("./data/modified_test.csv", "./data/test.jsonl",is_test=True)

    # load the model
    MODEL_DIR = "Qwen-1.5-1.8B-ASCA" # qloar qwen
    TEST_PATH = "data/test.jsonl"
    PREDICT_TEST_PATH = 'data/PredTest.jsonl'
    model, tokenizer = load_model()
    model.eval()

    # calcute the num of test data
    data = pd.read_csv('./data/modified_test.csv')
    MAX_JSON_OBJECTS = len(data)

    # start LLM inference and Use tqdm to track progress
    with tqdm(total=MAX_JSON_OBJECTS, desc='Processing') as pbar, \
        open(TEST_PATH, 'r', encoding='utf-8') as read_file, \
        open(PREDICT_TEST_PATH, 'w', encoding='utf-8') as write_file:
        for line in read_file:
            json_object = json.loads(line)
            
            input_text = json_object['conversation'][0]['input']
            PredOutput = predict(input_text)
            json_object['conversation'][0]['PredOutput'] = PredOutput
            
            # Writes the modified JSON object to the output file, adding newlines
            write_file.write(json.dumps(json_object) + '\n')
            
            # Update the progress bar of tqdm
            pbar.update(1)
            
            if pbar.n >= MAX_JSON_OBJECTS:
                break
    
    # Evaluation model and save results to a new text file
    file_path = 'data/PredTest.jsonl'
    output_file = 'result/performance_results.txt'
    results = evaluate_performance(file_path)
    save_results_to_txt(results, output_file)
