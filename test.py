from langchain.schema.document import Document
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter

doc1 = Document(page_content="Just a test document to assess splitting/chunking")
doc2 = Document(page_content="Short doc")
docs = [doc1, doc2]

text_splitter_c = CharacterTextSplitter(chunk_size=30, chunk_overlap=10)
text_splitter_rc = RecursiveCharacterTextSplitter(chunk_size=30, chunk_overlap=10)

texts_c = text_splitter_c.split_documents(docs)
texts_rc = text_splitter_rc.split_documents(docs)

max_chunk_c = max([ len(x.to_json()['kwargs']['page_content']) for x in texts_c])
max_chunk_rc = max([ len(x.to_json()['kwargs']['page_content']) for x in texts_rc])

print(f"Max chunk in CharacterTextSplitter output is of length {max_chunk_c}")
print(f"Max chunk in RecursiveCharacterTextSplitter output is of length {max_chunk_rc}")



