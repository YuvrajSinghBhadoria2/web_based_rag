import os
import aiohttp
import asyncio

async def test_all_models():
    api_key = "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"
    
    models = [
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768",
        "llama-3.3-70b-versatile",
        "llama3-8b-8192",
        "gemma-7b-it"
    ]
    
    for model in models:
        print(f"\n{'='*60}")
        print(f"Testing model: {model}")
        print('='*60)
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": "Say 'OK' if you can read this."}
            ],
            "temperature": 0.1,
            "max_tokens": 10
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                timeout = aiohttp.ClientTimeout(total=10)
                async with session.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=timeout
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        answer = data["choices"][0]["message"]["content"]
                        print(f"✅ SUCCESS: {answer}")
                    else:
                        text = await response.text()
                        print(f"❌ FAILED ({response.status}): {text[:200]}")
                        
        except Exception as e:
            print(f"❌ ERROR: {e}")

asyncio.run(test_all_models())
