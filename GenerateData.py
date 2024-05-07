import pandas as pd
from prompt import SYSTEM_PROMPT
import json
from tqdm import tqdm

def read_data(DocList):
    for doc in DocList:
        df = pd.read_csv(f'./data/download_data/{doc}.csv', encoding='utf_8_sig')
        columns_to_check = df.columns[3:]

        # check each column for -2 and replace with 0
        for column in columns_to_check:
            df.loc[df[column] == -2, column] = 0

        df.to_csv(f'./data/modified_{doc}.csv', index=False,encoding='utf_8_sig')



def map_dataset(data_path, output_path, is_test = None):
    df = pd.read_csv(data_path, encoding='utf_8_sig')
    results = []
    for index, row in tqdm(df.iterrows(), total=len(df)):
        label_dict = {}
        for col in df.columns[3:-1]:
            label_dict[col] = row[col]
        
        labels_str = ', '.join([f"{col}: {val}" for col, val in label_dict.items()])
        
        if is_test:
            results.append(
                {
                    "conversation": [
                        {
                            "system": "",
                            "input": SYSTEM_PROMPT.format(question=row['review']),
                            "output": labels_str,
                            "PredOutput": ""
                        }
                    ]
                }
            )
        else:
            results.append(
                {
                    "conversation": [
                        {
                            "system": "",
                            "input": SYSTEM_PROMPT.format(question=row['review']),
                            "output": labels_str
                        }
                    ]
                }
            )
    with open(output_path, "w", encoding="utf-8") as f:
        for result in results:
            json.dump(result, f)
            f.write('\n')  
            
if __name__ == "__main__":
    DocList = ['train','dev','test']
    read_data(DocList)
    map_dataset("./data/modified_dev.csv", "./data/train.jsonl")
    map_dataset("./data/modified_test.csv", "./data/test.jsonl",is_test=True)
