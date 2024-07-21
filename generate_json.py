import pandas as pd
import json

def create_json_object(custom_id, prompt, model):
    return {
        "custom_id": custom_id,
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1000
        }
    }

def generate_jsonl(df, model, custom_id_column, prompt_column, output_file='input_file.jsonl'):
    """Generate JSON objects for each row in the DataFrame"""
    json_objects = []
    for idx, row in df.iterrows():
        custom_id = row[custom_id_column]
        prompt = row[prompt_column]
        json_object = create_json_object(custom_id, prompt, model)
        json_objects.append(json_object)

    # Write the JSON objects to a .jsonl file
    with open(output_file, 'w') as f:
        for json_object in json_objects:
            f.write(json.dumps(json_object) + '\n')

    print(f"Data has been written to {output_file}")
