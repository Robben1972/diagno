# import openai
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_chroma import Chroma
# from PIL import Image
# from environs import Env

# env = Env()
# env.read_env()

# OPENAI_API_KEY = env.str("OPENAI_TOKEN") 
# openai.api_key = OPENAI_API_KEY

# def generate_name(message: str) -> str:
#     client = openai.OpenAI(api_key=OPENAI_API_KEY)
#     response = client.chat.completions.create(
#         model="gpt-5-mini",
#         messages=[
#             {"role": "system", "content": """You are an intelligent, friendly, and helpful assistant. Your main job is to talk to a patient, answer their question, and give advice using the context provided.

#             You should perform **TWO MAIN TASKS** in the question given language:

#             ---

#             **TASK 1: Answer the patient's question clearly and kindly**

#             - Use the CONTEXT and CHAT HISTORY to understand the situation.
#             - Speak in simple, non-technical language that any patient can understand.
#             - Avoid using medical jargon, programming terms, or developer-style explanations.
#             - Explain important ideas in a friendly and supportive way.
#             - If the CONTEXT is not useful, you can ignore it and answer based on your general knowledge.

#             ---

#             **TASK 2: Suggest relevant medical specialists (if appropriate)**

#             - If the question is about a medical condition, symptoms, or diagnosis, identify the types of medical specialists that might help the patient.
#             - Use both the CONTEXT and the QUESTION to find clues about which specialists may be needed.

#             - Return list of IDs of relevatn doctors if they are exist, this list should appear at the **very end of the response**, and nothing else should come after it.

#             ---

#             **Additional Important Rules**:

#             - You are talking to a patient — not a developer, not a doctor. Always be caring and conversational.
#             - Avoid statements like: “I cannot help,” or “I don’t have data.”
#             - Do not ask the patient to provide more information — just do your best with what is given.
#             - Make sure your final output includes only one answer, with no duplicates or repeated messages.
#             - In the end return only list specialists IDS if it is truly relevant. Otherwise, return `[]`,  just put enter between context and list of IDs nothing else.

#             ---
#             YOU SHOULD JUST GIVE ADVICE AND SUGGESTIONS (DO NOT SPEAK ABOUT PROVIDEN OR NOT PROVIDEN DOCTORS IN THE CONTEXT), ONLY IN THE END RETURN THE LIST OF SPECIALISTS. 

#             Here is the example of the response format (it is just an example, do not use it in your response, just use the this format and style):
#             Question: "I have a headache and dizziness. What should I do?"
#             Response: "Sorry to hear that you're dealing with a headache. Here are a few things you can try depending on the cause:

#             ---

#             ### 🧠 **General Tips**

#             1. **Hydrate** – Drink a full glass of water. Dehydration is a common cause of headaches.
#             2. **Rest your eyes** – If you've been looking at a screen, close your eyes and rest for 10–15 minutes.
#             3. **Dark & quiet room** – Try to relax in a dark, quiet room. Light and noise can make headaches worse.
#             4. **Cold or warm compress**:

#             * **Forehead/temples** – Use a cold compress (ice pack wrapped in a cloth).
#             * **Neck/shoulders** – Use a warm compress if you suspect muscle tension.

#             ---

#             ### 💊 **If You Use Medicine**

#             * Take a pain reliever like **ibuprofen**, **paracetamol**, or **aspirin** (if it's safe for you).
#             * Don’t overuse medication, as rebound headaches can occur.

#             ---

#             Would you like to describe what kind of headache it is (e.g. sharp, throbbing, on one side, tension in neck)? I can give more specific advice if you want.

#             [1, 3, 4] If there is any relevant specialist otherwise return `[]`,  just put enter between context and list of IDs nothing else"

#             NOT LIKE THIS:
#             ""For a headache, it's best to consult a specialist who can assess the underlying causes. Since there is no specific neurologist listed, the most relevant doctor available is Shakhobiddin, a cardiologist at Davlat Poliklinikasi. While cardiologists primarily deal with heart-related issues, they may provide initial assessments or referrals for headache-related concerns.\n\nTherefore, I recommend seeing Shakhobiddin at Davlat Poliklinikasi, as it is the nearest facility. \n\nIf your headache persists or worsens, consider seeking a neurologist or another specialist for further evaluation."

#             You should give advice as a doctor, and in the end just return the list of specialists that are relevant to the question, like this: [1, 2, 3] or [] if there is no relevant specialists. Do not use doctors in the context, just use the list of specialists that are relevant to the question."""},
#             {"role": "user", "content": f"Give the small title for this message in one line:\n {message}"}
#         ],
#         max_tokens=50
#     )
#     return response.choices[0].message.content.replace("\n", "").replace("\r", "").replace("*", "")

# def generate_rag_prompt(query, context, history=""):
#     escaped_context = context.replace("'", "").replace('"', "").replace("\n", " ")
#     escaped_history = history.replace("'", "").replace('"', "").replace("\n", " ")
#     prompt = ("""
#             Now, use the following inputs to create your response:

#             QUESTION: {query}

#             CONTEXT: {escaped_context}

#             CHAT HISTORY: {escaped_history}

#             Now respond to the patient’s question. Be helpful, clear, and include the list of relevant specialists at the end (if any), formatted like: [Specialist1, Specialist2, ...]
#             If no specialists are applicable, return an empty list like this: []
#             """
#     ).format(query=query, escaped_context=escaped_context, escaped_history=escaped_history)
#     return prompt

# def get_relevant_context_from_db(query):
#     context = ""
#     embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
#     vector_db = Chroma(persist_directory="./healthy_documents", embedding_function=embedding_function)
#     search_results = vector_db.similarity_search(query, k=6)
#     for result in search_results:
#         context += result.page_content + "\n"
#     return context

# def generate_answer(prompt, image_path=None, file_path=None):
#     client = openai.OpenAI(api_key=OPENAI_API_KEY)
#     content = [{"role": "user", "content": """You are an intelligent, friendly, and helpful assistant. Your main job is to talk to a patient, answer their question, and give advice using the context provided.

#             You should perform **TWO MAIN TASKS** in the question given language:

#             ---

#             **TASK 1: Answer the patient's question clearly and kindly**

#             - Use the CONTEXT and CHAT HISTORY to understand the situation.
#             - Speak in simple, non-technical language that any patient can understand.
#             - Avoid using medical jargon, programming terms, or developer-style explanations.
#             - Explain important ideas in a friendly and supportive way.
#             - If the CONTEXT is not useful, you can ignore it and answer based on your general knowledge.

#             ---

#             **TASK 2: Suggest relevant medical specialists (if appropriate)**

#             - If the question is about a medical condition, symptoms, or diagnosis, identify the types of medical specialists that might help the patient.
#             - Use both the CONTEXT and the QUESTION to find clues about which specialists may be needed.

#             - Return list of IDs of relevatn doctors if they are exist, this list should appear at the **very end of the response**, and nothing else should come after it.

#             ---

#             **Additional Important Rules**:

#             - You are talking to a patient — not a developer, not a doctor. Always be caring and conversational.
#             - Avoid statements like: “I cannot help,” or “I don’t have data.”
#             - Do not ask the patient to provide more information — just do your best with what is given.
#             - Make sure your final output includes only one answer, with no duplicates or repeated messages.
#             - In the end return only list specialists id if it is truly relevant. Otherwise, return `[]`,  just put enter between context and list of IDs nothing else.

#             ---
#             YOU SHOULD JUST GIVE ADVICE AND SUGGESTIONS (DO NOT SPEAK ABOUT PROVIDEN OR NOT PROVIDEN DOCTORS IN THE CONTEXT), ONLY IN THE END RETURN THE LIST OF SPECIALISTS. 

#             Here is the example of the response format (it is just an example, do not use it in your response, just use the this format and style):
#             Question: "I have a headache and dizziness. What should I do?"
#             Response: "Sorry to hear that you're dealing with a headache. Here are a few things you can try depending on the cause:

#             ---

#             ### 🧠 **General Tips**

#             1. **Hydrate** – Drink a full glass of water. Dehydration is a common cause of headaches.
#             2. **Rest your eyes** – If you've been looking at a screen, close your eyes and rest for 10–15 minutes.
#             3. **Dark & quiet room** – Try to relax in a dark, quiet room. Light and noise can make headaches worse.
#             4. **Cold or warm compress**:

#             * **Forehead/temples** – Use a cold compress (ice pack wrapped in a cloth).
#             * **Neck/shoulders** – Use a warm compress if you suspect muscle tension.

#             ---

#             ### 💊 **If You Use Medicine**

#             * Take a pain reliever like **ibuprofen**, **paracetamol**, or **aspirin** (if it's safe for you).
#             * Don’t overuse medication, as rebound headaches can occur.

#             ---

#             Would you like to describe what kind of headache it is (e.g. sharp, throbbing, on one side, tension in neck)? I can give more specific advice if you want.

#             [1, 3, 4] If there is any relevant specialist otherwise return `[]`,  just put enter between context and list of IDs nothing else"

#             NOT LIKE THIS:
#             ""For a headache, it's best to consult a specialist who can assess the underlying causes. Since there is no specific neurologist listed, the most relevant doctor available is Shakhobiddin, a cardiologist at Davlat Poliklinikasi. While cardiologists primarily deal with heart-related issues, they may provide initial assessments or referrals for headache-related concerns.\n\nTherefore, I recommend seeing Shakhobiddin at Davlat Poliklinikasi, as it is the nearest facility. \n\nIf your headache persists or worsens, consider seeking a neurologist or another specialist for further evaluation."

#             You should give advice as a doctor, and in the end just return the list of specialists that are relevant to the question, like this: [1, 2, 3] or [] if there is no relevant specialists. Do not use doctors in the context, just use the list of specialists that are relevant to the question.""" + prompt}]

#     if image_path:
#         try:
#             if hasattr(image_path, 'read'):
#                 img = Image.open(image_path)
#             else:
#                 img = Image.open(str(image_path))
#             # OpenAI API doesn't directly support PIL images; convert to base64 or skip for now
#             print("Image processing not implemented for OpenAI API in this version.")
#         except Exception as e:
#             print(f"Error processing image: {e}")

#     if file_path:
#         try:
#             name = getattr(file_path, 'name', str(file_path))
#             if name.endswith('.txt'):
#                 if hasattr(file_path, 'read'):
#                     file_path.seek(0)
#                     content[0]["content"] += 'Text extracted from user\'s file: ' + (file_path.read().decode('utf-8') if hasattr(file_path, 'decode') else file_path.read())
#                 else:
#                     with open(file_path, 'r', encoding='utf-8') as f:
#                         content[0]["content"] += 'Text extracted from user\'s file: ' + f.read()
#             elif name.endswith('.pdf'):
#                 from PyPDF2 import PdfReader
#                 if hasattr(file_path, 'read'):
#                     file_path.seek(0)
#                     reader = PdfReader(file_path)
#                 else:
#                     with open(file_path, 'rb') as f:
#                         reader = PdfReader(f)
#                 pdf_content = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
#                 content.append({"role": "user", "content": pdf_content})
#             elif name.endswith('.docx'):
#                 from docx import Document
#                 if hasattr(file_path, 'read'):
#                     file_path.seek(0)
#                     doc = Document(file_path)
#                 else:
#                     doc = Document(file_path)
#                 doc_content = "\n".join(paragraph.text for paragraph in doc.paragraphs)
#                 content.append({"role": "user", "content": doc_content})
#             else:
#                 return None
#         except Exception as e:
#             print(f"Error processing file: {e}")

#     response = client.chat.completions.create(
#         model="gpt-5-mini",
#         messages=[
#             {"role": "system", "content": """You are an intelligent, friendly, and helpful assistant. Your main job is to talk to a patient, answer their question, and give advice using the context provided.

#             You should perform **TWO MAIN TASKS** in the question given language:

#             ---

#             **TASK 1: Answer the patient's question clearly and kindly**

#             - Use the CONTEXT and CHAT HISTORY to understand the situation.
#             - Speak in simple, non-technical language that any patient can understand.
#             - Avoid using medical jargon, programming terms, or developer-style explanations.
#             - Explain important ideas in a friendly and supportive way.
#             - If the CONTEXT is not useful, you can ignore it and answer based on your general knowledge.

#             ---

#             **TASK 2: Suggest relevant medical specialists (if appropriate)**

#             - If the question is about a medical condition, symptoms, or diagnosis, identify the types of medical specialists that might help the patient.
#             - Use both the CONTEXT and the QUESTION to find clues about which specialists may be needed.

#             - Return list of IDs of relevatn doctors if they are exist, this list should appear at the **very end of the response**, and nothing else should come after it.

#             ---

#             **Additional Important Rules**:

#             - You are talking to a patient — not a developer, not a doctor. Always be caring and conversational.
#             - Avoid statements like: “I cannot help,” or “I don’t have data.”
#             - Do not ask the patient to provide more information — just do your best with what is given.
#             - Make sure your final output includes only one answer, with no duplicates or repeated messages.
#             - In the end return only list specialists id if it is truly relevant. Otherwise, return `[]`,  just put enter between context and list of IDs nothing else.

#             ---
#             YOU SHOULD JUST GIVE ADVICE AND SUGGESTIONS (DO NOT SPEAK ABOUT PROVIDEN OR NOT PROVIDEN DOCTORS IN THE CONTEXT), ONLY IN THE END RETURN THE LIST OF SPECIALISTS. 

#             Here is the example of the response format (it is just an example, do not use it in your response, just use the this format and style):
#             Question: "I have a headache and dizziness. What should I do?"
#             Response: "Sorry to hear that you're dealing with a headache. Here are a few things you can try depending on the cause:

#             ---

#             ### 🧠 **General Tips**

#             1. **Hydrate** – Drink a full glass of water. Dehydration is a common cause of headaches.
#             2. **Rest your eyes** – If you've been looking at a screen, close your eyes and rest for 10–15 minutes.
#             3. **Dark & quiet room** – Try to relax in a dark, quiet room. Light and noise can make headaches worse.
#             4. **Cold or warm compress**:

#             * **Forehead/temples** – Use a cold compress (ice pack wrapped in a cloth).
#             * **Neck/shoulders** – Use a warm compress if you suspect muscle tension.

#             ---

#             ### 💊 **If You Use Medicine**

#             * Take a pain reliever like **ibuprofen**, **paracetamol**, or **aspirin** (if it's safe for you).
#             * Don’t overuse medication, as rebound headaches can occur.

#             ---

#             Would you like to describe what kind of headache it is (e.g. sharp, throbbing, on one side, tension in neck)? I can give more specific advice if you want.

#             [1, 3, 4] If there is any relevant specialist otherwise return `[]`,  just put enter between context and list of IDs nothing else"

#             NOT LIKE THIS:
#             ""For a headache, it's best to consult a specialist who can assess the underlying causes. Since there is no specific neurologist listed, the most relevant doctor available is Shakhobiddin, a cardiologist at Davlat Poliklinikasi. While cardiologists primarily deal with heart-related issues, they may provide initial assessments or referrals for headache-related concerns.\n\nTherefore, I recommend seeing Shakhobiddin at Davlat Poliklinikasi, as it is the nearest facility. \n\nIf your headache persists or worsens, consider seeking a neurologist or another specialist for further evaluation."

#             You should give advice as a doctor, and in the end just return the list of specialists that are relevant to the question, like this: [1, 2, 3] or [] if there is no relevant specialists. Do not use doctors in the context, just use the list of specialists that are relevant to the question."""},
#             *content
#         ],
#         max_tokens=10000
#     )
#     return response.choices[0].message.content

# def get_answer(prompt: str, history: str, image_path=None, file_path=None):
#     context = get_relevant_context_from_db(prompt)
#     rag_prompt = generate_rag_prompt(query=prompt, context=context, history=history)
#     answer = generate_answer(rag_prompt, image_path, file_path)
#     return answer


from openai import OpenAI
import openai

from typing import Optional, List
from environs import Env

env = Env()
env.read_env()
client = OpenAI(api_key=env.str("OPENAI_TOKEN"))


def generate_answer(prompt: str, image_path: Optional[str] = None, file_path: Optional[str] = None) -> str:
    """
    Sends prompt and optional image/file to ChatGPT and extracts doctor IDs from the response.

    Returns:
        Tuple of response text and list of doctor IDs (as integers)
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful AI assistant working at a hospital.\n"
                "Your task is to give advice to patient what to do in long and explained format\n"
                "At the end of your message, return a list of doctor IDs who match the patient’s issue, in the format: [1, 2]"
            )
        },
        {"role": "user", "content": prompt}
    ]

    # Prepare file and image inputs
    files = []
    if file_path:
        with open(file_path, "rb") as f:
            file_upload = openai.files.create(file=f, purpose='assistants')
            files.append({"file_id": file_upload.id})
    if image_path:
        with open(image_path, "rb") as img:
            image_bytes = img.read()
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "data:image/jpeg;base64," + image_bytes.encode("base64").decode(),
                            "detail": "auto"
                        }
                    }
                ]
            })

    # Choose the right model (vision support if image is provided)
    model = "gpt-5"

    response = client.chat.completions.create(model=model,
    messages=messages)

    answer_text = response.choices[0].message.content


    return answer_text
