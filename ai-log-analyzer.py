import subprocess
import requests
import os

# HuggingFace API
API_URL = "https://router.huggingface.co/hf-inference/models/mistralai/Mistral-7B-Instruct-v0.3"
HF_TOKEN = os.getenv("HF_TOKEN")

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

CONTAINER_NAME = "affectionate_hermann"

try:
    # Get docker logs
    logs = subprocess.check_output(
        ["docker", "logs", "--tail", "50", CONTAINER_NAME],
        stderr=subprocess.STDOUT
    ).decode()

    print("\n===== DOCKER LOGS =====\n")
    print(logs)

    prompt = f"""
You are a DevOps security assistant.

Analyze the following nginx/docker logs and produce a HUMAN READABLE report.

Return output in this format:

1. Summary of traffic
2. Suspicious activities detected
3. Possible attacks
4. Suggested fixes for the server

Logs:
{logs}
"""

    response = requests.post(
        API_URL,
        headers=headers,
        json={
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 300
            }
        }
    )

    print("\n===== AI ANALYSIS =====\n")

    if response.status_code != 200:
        print("API ERROR:", response.status_code)
        print(response.text)
        exit()

    result = response.json()

    if isinstance(result, list):
        text = result[0]["generated_text"]
    else:
        text = str(result)

    # Clean output
    text = text.replace(prompt, "")

    print(text.strip())

except subprocess.CalledProcessError as e:
    print("Error fetching docker logs:", e.output.decode())