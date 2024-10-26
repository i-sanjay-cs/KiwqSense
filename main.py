from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import requests
import base64
import hashlib
from cachetools import TTLCache, cached
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

invoke_url = "https://ai.api.nvidia.com/v1/gr/meta/llama-3.2-90b-vision-instruct/chat/completions"


API_KEY = os.getenv("API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Cache with TTL
cache = TTLCache(maxsize=100, ttl=600)

def generate_cache_key(image_b64: str) -> str:
    """Generate a cache key from the base64 image."""
    return hashlib.sha256(image_b64.encode()).hexdigest()

@cached(cache)
def get_threat_analysis(image_b64: str):
    """Analyze image for threats using NVIDIA API."""
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Accept": "application/json"
        }

        payload = {
            "model": 'meta/llama-3.2-90b-vision-instruct',
            "messages": [
                {
                    "role": "user",
                    "content": (
                        f"Analyze the image below for any potential threats to public safety. "
                        f"Please respond with 'dangerous' if a threat is detected, or 'not dangerous' otherwise. "
                        f"Include a description if a threat is present. "
                        f'<img src="data:image/png;base64,{image_b64}" />'
                    )
                }
            ],
            "max_tokens": 512,
            "temperature": 0,
            "top_p": 1.00
        }

        response = requests.post(invoke_url, headers=headers, json=payload)
        
        if response.status_code == 200:
            json_response = response.json()
            if "choices" in json_response and json_response["choices"]:
                return json_response["choices"][0]["message"]["content"]
        print(f"API Response: {response.text}")
        return None
    except Exception as e:
        print(f"Error in threat analysis: {str(e)}")
        return None

def send_telegram_alert(photo_b64: str, description: str):
    try:
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        photo_data = base64.b64decode(photo_b64)
        
        files = {
            "photo": ("alert.png", photo_data),
        }
        data = {
            "chat_id": CHANNEL_ID,
            "caption": f"🚨 Alert: Dangerous Situation Detected!\n\n{description}"
        }
        
        response = requests.post(telegram_url, data=data, files=files)
        print(f"Telegram API Response: {response.status_code}")
        print(f"Response content: {response.text}")
        
        if response.status_code != 200:
            print(f"Failed to send Telegram message: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending Telegram alert: {str(e)}")
        return False

def test_telegram_setup():
    try:
        test_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": CHANNEL_ID,
            "text": "🔧 Test message: System is online and working!"
        }
        response = requests.post(test_url, data=data)
        print(f"Test message response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Test failed: {str(e)}")
        return False

@app.post("/detect-threat/")
async def detect_threat(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image_b64 = base64.b64encode(contents).decode()
        
        assert len(image_b64) < 180_000, "To upload larger images, use the assets API (see docs)"
        
        cache_key = generate_cache_key(image_b64)
        result = get_threat_analysis(image_b64)

        if result is not None:
            if "dangerous" in result.lower():
                alert_sent = send_telegram_alert(image_b64, result)
                return JSONResponse(content={
                    "alert": "dangerous", 
                    "description": result,
                    "telegram_alert_sent": alert_sent
                })
            else:
                return JSONResponse(content={"alert": "not dangerous"})
        else:
            return JSONResponse(content={"error": "No valid response from model or request failed."})
    except Exception as e:
        print(f"Error in detect_threat: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    print("Testing Telegram connection...")
    if test_telegram_setup():
        print("✅ Telegram setup is working correctly")
    else:
        print("❌ Telegram setup failed")
    
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)