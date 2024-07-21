import time
import json
from openai import OpenAI

# This code to implement batch method is adjusted from https://www.echohive.live/. 

SECRET_FILE = 'secrets.txt'

def get_openai_key(secret_file):
    try:
        with open(secret_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.split(',')[0].strip() == "openai_key":
                    return line.split(',')[1].strip()
    except FileNotFoundError:
        raise Exception(f"Secret file '{secret_file}' not found.")
    except Exception as e:
        raise Exception(f"An error occurred while reading the secret file: {e}")


class OpenAIBatchProcessor:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def process_batch(self, input_file_path, endpoint, completion_window, result_file_name):
        try:
            # Upload the input file
            with open(input_file_path, "rb") as file:
                uploaded_file = self.client.files.create(
                    file=file,
                    purpose="batch"
                )
            # Create the batch job
            batch_job = self.client.batches.create(
                input_file_id=uploaded_file.id,
                endpoint=endpoint,
                completion_window=completion_window
            )
            # Monitor the batch job status
            while batch_job.status not in ["completed", "failed", "cancelled"]:
                time.sleep(1)  # Batch API has a rate limite of 100/minute
                #print(f"Batch job status: {batch_job.status}...")
                batch_job = self.client.batches.retrieve(batch_job.id)

            # Download and save the results
            if batch_job.status == "completed":
                result_file_id = batch_job.output_file_id
                result = self.client.files.retrieve_content(result_file_id)
                with open(result_file_name, "wb") as file:
                    file.write(result.encode())

                # Load data from the saved file
                results = []
                with open(result_file_name, "r") as file:
                    for line in file:
                        json_object = json.loads(line.strip())
                        results.append(json_object)
                return results
            else:
                print(f"Batch job failed with status: {batch_job.status}")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


if __name__ == '__main__':
    openai_key = get_openai_key(SECRET_FILE)
    processor = OpenAIBatchProcessor(openai_key)
    input_file_path = 'input_file.jsonl'
    endpoint = 'v1/chat/completions'
    completion_window = "24h"
    result_file_name = 'batch_job_results.jsonl'
    results = processor.process_batch(input_file_path, endpoint, completion_window, result_file_name)