import requests

url = "http://localhost:11434/api/generate"

payload = {
    "model": "qwen2.5:3b",
    "prompt": "Explique en deux phrases la différence entre la VaR et la CVaR.",
    "stream": False
}

response = requests.post(url, json=payload, timeout=180)

print(response.json()["response"])
