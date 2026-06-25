import os

DOCS_DIR = "documents"

def load_documents(docs_dir):
    documents = {}
    for filename in os.listdir(docs_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(docs_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                documents[filename] = f.read()
    return documents

if __name__ == "__main__":
    docs = load_documents(DOCS_DIR)
    print(f"Loaded {len(docs)} documents:")
    for name in docs:
        print(f" - {name}")

    # Print one full document so we can inspect it
    first_doc_name = list(docs.keys())[0]
    print(f"\n--- Contents of {first_doc_name} ---\n")
    print(docs[first_doc_name])