import os
import pdfplumber
from openai import OpenAI
from dotenv import load_dotenv

def table_to_markdown(table):
    if not table:
        return ""
    # Convert all None to empty string to avoid errors
    header = [str(cell) if cell is not None else "" for cell in table[0]]
    rows = [
        [str(cell) if cell is not None else "" for cell in row]
        for row in table[1:]
    ]
    md = "| " + " | ".join(header) + " |\n"
    md += "| " + " | ".join("---" for _ in header) + " |\n"
    for row in rows:
        md += "| " + " | ".join(row) + " |\n"
    return md


def extract_text_and_tables_from_pdf(pdf_path):
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text() or ""
            
            # Extract tables
            tables = page.extract_tables()
            tables_text = ""
            if tables:
                for idx, table in enumerate(tables):
                    md_table = table_to_markdown(table)
                    tables_text += f"\nTable {idx+1} on page {i+1}:\n{md_table}\n"
            
            full_text += f"Page {i+1} text:\n{page_text}\n"
            if tables_text:
                full_text += tables_text + "\n"
    
    return full_text.strip()

def main():
    load_dotenv()
    token = os.getenv("SECRET")
    endpoint = "https://models.github.ai/inference"
    model = "openai/gpt-4.1-nano"
    
    client = OpenAI(
        base_url=endpoint,
        api_key=token,
    )
    
    pdf_path = "sample-table.pdf"
    print(f"Extracting text and tables from {pdf_path}...")
    document_text = extract_text_and_tables_from_pdf(pdf_path)
    
    if not document_text:
        print("Failed to extract any text or tables from the PDF.")
        return
    
    print("PDF content loaded into memory.")
    print("You can now ask questions about the document. Type 'exit' to quit.")
    
    while True:
        user_question = input("\nYour question: ")
        if user_question.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        
        prompt = f"""You are an AI assistant. Use the following document to answer the question.

Document:
\"\"\"
{document_text}
\"\"\"

Question: {user_question}

Answer:"""
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based on a provided document."},
                {"role": "user", "content": prompt}
            ]
        )
        
        answer = response.choices[0].message.content.strip()
        print(f"\nAnswer: {answer}")

if __name__ == "__main__":
    main()
