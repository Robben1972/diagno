# import fitz  # pymupdf
# import tiktoken
# from openai import OpenAI
# from leann import LEANNIndex
# import os
# from pathlib import Path

# # ====== CONFIG ======
# PDF_FOLDER = "pdf_books"  # folder with your PDF files
# INDEX_PATH = "leann_index"
# EMBEDDING_MODEL = "text-embedding-3-large"
# CHUNK_SIZE = 500  # tokens per chunk
# CHUNK_OVERLAP = 50  # tokens overlap between chunks

# # ====== INIT ======
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# tokenizer = tiktoken.get_encoding("cl100k_base")
# index = LEANNIndex(dim=3072)  # dimension of "text-embedding-3-large"

# def extract_text_from_pdf(pdf_path):
#     """Extracts text from a PDF file."""
#     doc = fitz.open(pdf_path)
#     text = ""
#     for page in doc:
#         text += page.get_text()
#     return text.strip()

# def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
#     """Splits text into overlapping chunks based on tokens."""
#     tokens = tokenizer.encode(text)
#     chunks = []
#     for i in range(0, len(tokens), chunk_size - overlap):
#         chunk_tokens = tokens[i:i + chunk_size]
#         chunk_text = tokenizer.decode(chunk_tokens)
#         chunks.append(chunk_text)
#     return chunks

# def embed_text(texts):
#     """Gets embeddings from OpenAI API."""
#     response = client.embeddings.create(
#         model=EMBEDDING_MODEL,
#         input=texts
#     )
#     return [item.embedding for item in response.data]

# def build_index():
#     pdf_files = Path(PDF_FOLDER).glob("*.pdf")
#     for pdf_file in pdf_files:
#         print(f"Processing: {pdf_file}")
#         text = extract_text_from_pdf(pdf_file)
#         chunks = chunk_text(text)
#         embeddings = embed_text(chunks)

#         for chunk, vector in zip(chunks, embeddings):
#             index.add_item(vector, {"text": chunk, "source": str(pdf_file)})

#     index.save(INDEX_PATH)
#     print(f"Index saved to {INDEX_PATH}")

# if __name__ == "__main__":
#     build_index()

