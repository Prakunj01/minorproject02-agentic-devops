import subprocess
import boto3

CONTAINER_NAME = "phase-1"

# Bedrock client
client = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1"
)

try:
    # Get docker logs
    logs = subprocess.check_output(
        ["docker", "logs", "--since", "5m", CONTAINER_NAME],
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

    # Bedrock request
    response = client.converse(
        modelId="us.meta.llama3-1-8b-instruct-v1:0",
        messages=[
            {
                "role": "user",
                "content": [{"text": prompt}]
            }
        ],
    )

    result = response["output"]["message"]["content"][0]["text"]

    print("\n===== AI ANALYSIS =====\n")
    print(result)

except subprocess.CalledProcessError as e:
    print("Error fetching docker logs:", e.output.decode())