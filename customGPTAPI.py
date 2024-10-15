#!/usr/bin/env python3
import string
from fastapi import FastAPI
from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
import chromadb
import os
import argparse
import time

app = FastAPI()

model_name = 'mistral'
model = os.environ.get("MODEL", model_name)
target_chunk = 100

# For embeddings model, the example uses a sentence-transformers model
# https://www.sbert.net/docs/pretrained_models.html 
# "The all-mpnet-base-v2 model provides the best quality, while all-MiniLM-L6-v2 is 5 times faster and still offers good quality."
embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME", "all-MiniLM-L6-v2")
persist_directory = os.environ.get("PERSIST_DIRECTORY", "db")
# edit this variable to determined how much chunks you want the ai for taking the context
target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS',target_chunk))

def parse_arguments():
    parser = argparse.ArgumentParser(description='privateGPT: Ask questions to your documents without an internet connection, '
                                                 'using the power of LLMs.')
    parser.add_argument("--hide-source", "-S", action='store_true',
                        help='Use this flag to disable printing of source documents used for answers.')

    parser.add_argument("--mute-stream", "-M",
                        action='store_true',
                        help='Use this flag to disable the streaming StdOut callback for LLMs.')

    return parser.parse_args()


@app.post("/")
def process_query(query: str):
    # Parse the command line arguments
    args = parse_arguments()
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)

    db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

    retriever = db.as_retriever(search_kwargs={"k": target_source_chunks})
    # activate/deactivate the streaming StdOut callback for LLMs
    callbacks = [] if args.mute_stream else [StreamingStdOutCallbackHandler()]

    llm = Ollama(model=model, callbacks=callbacks)

    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents= not args.hide_source)
    # Interactive questions and answers
    
    
    # Get the answer from the chain
    start = time.time()
    res = qa(query)
    answer, docs = res['result'], [] if args.hide_source else res['source_documents']
    end = time.time()
    elapsed_time = end-start
    
    references = []
    # Print the relevant sources used for the answer
    for document in docs:
        
        source = document.metadata["source"] + " : " + document.page_content
        references.append(source)
    
    return {"success" : True, "answer": answer, "references": references, "processed time" : elapsed_time}




