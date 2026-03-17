#importing langchain
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_text(text: str, chunk_size: int =300, chunk_overlap: int = 75) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(chunk_size = chunk_size, chunk_overlap= chunk_overlap) #splitting the text based of fixed size
    chunks = splitter.split_text(text) #chunks hold the list of chunks
    return chunks










