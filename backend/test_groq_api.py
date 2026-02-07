import os
import aiohttp
import asyncio

async def test_groq_api():
    api_key = os.getenv("GROQ_API_KEY", "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")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.1-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'Hello, API is working!' if you can read this."}
        ],
        "temperature": 0.1,
        "max_tokens": 50
    }
    
    print("Testing Groq API...")
    print(f"API Key: {api_key[:20]}...{api_key[-10:]}")
    print(f"Model: {payload['model']}")
    
    try:
        async with aiohttp.ClientSession() as session:
            timeout = aiohttp.ClientTimeout(total=30)
            async with session.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=timeout
            ) as response:
                print(f"\nStatus Code: {response.status}")
                
                if response.status == 200:
                    data = await response.json()
                    answer = data["choices"][0]["message"]["content"]
                    print(f"✅ SUCCESS!")
                    print(f"Response: {answer}")
                    return True
                else:
                    text = await response.text()
                    print(f"❌ FAILED!")
                    print(f"Response: {text}")
                    return False
                    
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

asyncio.run(test_groq_api())
