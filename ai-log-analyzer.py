import subprocess
import requests
import os


# HuggingFace API settings
API_URL = "https://router.huggingface.co/hf-inference/models/mistralai/Mistral-7B-Instruct-v0.2"

HF_TOKEN = os.getenv("HF_TOKEN")

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

# Container name (change if needed)
CONTAINER_NAME = "affectionate_hermann"

try:
    # Get last 50 logs from Docker container
    logs = subprocess.check_output(
        ["docker", "logs", "--tail", "50", CONTAINER_NAME],
        stderr=subprocess.STDOUT
    ).decode()

    print("\n===== DOCKER LOGS =====\n")
    print(logs)

    prompt = f"""
Analyze these server logs and explain any errors.
Also suggest possible fixes.

Logs:
{logs}
"""

    response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": prompt}
    )

    result = response.json()

    print("\n===== AI ANALYSIS =====\n")

    if isinstance(result, list):
        print(result[0]["generated_text"])
    else:
        print(result)

except subprocess.CalledProcessError as e:
    print("Error fetching docker logs:", e.output.decode())