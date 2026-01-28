from fastapi import FastAPI, HTTPException
from openai import OpenAI
import os

from dotenv import load_dotenv

load_dotenv() # This loads the variables from .env
api_key = os.getenv("OPENROUTER_API_KEY")

app = FastAPI()

# For local testing, we look for the key in your environment
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

@app.get("/ask")
async def ask(prompt: str):
    try:
        completion = client.chat.completions.create(
            model="meta-llama/llama-3.3-70b-instruct:free",
            messages=[{"role": "user", "content": prompt}]
        )
        return {"answer": completion.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
