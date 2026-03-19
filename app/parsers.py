from pypdf import PdfReader

def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text_parts = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text_parts.append(page_text)

    return "\n".join(text_parts)


def extract_text_from_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def extract_text(file_path: str) -> str:
    lower = file_path.lower()

    if lower.endswith(".pdf"):
        return extract_text_from_pdf(file_path)

    if lower.endswith(".txt"):
        return extract_text_from_txt(file_path)

    raise ValueError(f"Unsupported file type: {file_path}. Only PDF and TXT are supported.")
