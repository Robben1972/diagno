from typing import Optional, Union, Tuple
import base64
import re
from langdetect import detect
from django.core.files.uploadedfile import InMemoryUploadedFile
from openai import OpenAI
from environs import Env

env = Env()
env.read_env()

client = OpenAI(api_key=env.str("OPENAI_TOKEN"))

SYSTEM_PROMPT = """
You are a professional AI medical assistant working at a hospital. Your role is to help patients describe their symptoms and provide guidance on next steps. You are not a doctor, but you can:
- Offer medically reasonable, safe advice.
- Suggest which doctor(s) (by ID) the patient should contact.
- Respond natively in the language of the user's input. For example, if the user writes in Uzbek, respond in Uzbek; if in Russian, respond in Russian; if in English, respond in English, and so on.
- Be empathetic, polite, and clear.
- Provide clear, concise answers (300-500 words) with detailed explanations.

**Language Rules:**
- Detect the user's input language and respond natively in that language, ensuring the response is natural and idiomatic, not translated.
- If the input language is unclear, mixed, or unsupported, respond in English and politely note that the input language could not be determined, encouraging the user to clarify.
- Before finalizing the response, verify that the output language matches the detected input language.
- Never use phrases indicating translation (e.g., "translated from...").

Your response format must always follow this structure:
1️⃣ **Advice for the patient:** Give explanation of the possible issue in the given prompt language, steps to take, and when to see a doctor.
2️⃣ **Doctor recommendation IDs:** At the very bottom, return doctor IDs in brackets, for example:
[1, 2, 5]

**Rules:**
- Never include doctor IDs within the advice text.
- If unsure about the condition or next steps, advise consulting a doctor or visiting a nearby hospital.
- Avoid medical jargon unless explaining it clearly.
- Ensure responses are culturally sensitive and appropriate for the detected language.
"""

def parse_ai_response(answer: str) -> Tuple[str, list]:
    """
    Extracts the main response text and list of doctor IDs.
    """
    phrases_to_remove = [
        r'1️⃣\s*\*\*Advice for the patient:\*\*\s*',
        r'2️⃣\s*\*\*Doctor recommendation IDs:\*\*\s*'
    ]
    cleaned_answer = answer
    for phrase in phrases_to_remove:
        cleaned_answer = re.sub(phrase, '', cleaned_answer)
    
    # Extract doctor IDs
    match = re.search(r'\[([\d,\s]+)\]', cleaned_answer)
    if match:
        doctor_ids_str = match.group(1)
        doctor_ids = [int(x.strip()) for x in doctor_ids_str.split(',') if x.strip().isdigit()]
        # Remove the doctor IDs part from the main response
        main_response = re.sub(r'\n*\[[\d,\s]+\]\s*$', '', cleaned_answer).strip()
    else:
        doctor_ids = []
        main_response = cleaned_answer.strip()
    
    return main_response, doctor_ids


def generate_answer(
    prompt: str,
    image_path: Optional[Union[str, InMemoryUploadedFile]] = None,
    file_text: Optional[str] = None
) -> Tuple[str, list]:
    """
    Generates a structured medical response using OpenAI GPT model.
    Automatically detects user's language and ensures proper formatting.
    """
    # Detect language for better consistency
    try:
        lang = detect(prompt)
    except Exception:
        lang = "en"

    user_prompt = (
        f"User message language: {lang}\n"
        f"User message and context:\n{prompt}\n"
    )

    if file_text:
        user_prompt += f"\nAttached file content:\n{file_text}\n"

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ]

    # Add image support if provided
    if image_path:
        if isinstance(image_path, InMemoryUploadedFile):
            image_bytes = image_path.read()
        else:
            with open(image_path, "rb") as img:
                image_bytes = img.read()

        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": user_prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "data:image/jpeg;base64," + base64.b64encode(image_bytes).decode(),
                        "detail": "auto"
                    }
                }
            ]
        })

    model = "gpt-4o" if image_path else "gpt-4o-mini"

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    answer = response.choices[0].message.content
    return parse_ai_response(answer)
