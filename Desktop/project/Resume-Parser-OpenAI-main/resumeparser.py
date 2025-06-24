# -------- resumeparser.py --------
import yaml
from openai import OpenAI          # ← use OpenAI client, point it at OpenRouter

# ------------------------------------------------------------------#
# Load your key from config.yaml (same as before)
with open("config.yaml", "r") as f:
    api_key = yaml.safe_load(f)["OPENAI_API_KEY"]

# Configure the client **once**
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",   # OpenRouter endpoint
    api_key=api_key,
    # Optional but nice: these let your app show up on openrouter.ai leaderboards
    default_headers={
        "HTTP-Referer": "http://localhost:8000",
        "X-Title":       "Resume-Parser-App",
    },
)

# ------------------------------------------------------------------#


def ats_extractor(resume_text: str) -> str:
    """
    Parse a resume (plain text) and return the extracted info as a JSON string.
    """
    system_prompt = (
        "You are an AI resume-parsing expert.\n"
        "Given a resume, extract ONLY the following and output pure JSON:\n"
        "1. full name\n2. email id\n3. github portfolio\n4. linkedin id\n"
        "5. employment details\n6. technical skills\n7. soft skills"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user",   "content": resume_text},
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # ✅ Free tier supported model

        messages=messages,
        temperature=0.0,
        max_tokens=1500,
    )
    return response.choices[0].message.content
