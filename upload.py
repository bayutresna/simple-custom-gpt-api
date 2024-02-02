from fastapi import FastAPI, UploadFile, File
from typing import List
import os
import shutil
app = FastAPI() 

db_directory = "./db/"
cache_directory = "./__pycache__/"
document_directory = "./files/"

@app.post("/")
async def upload(files:List[UploadFile] = File(...)):
    if not os.path.exists('files'):
        os.mkdir('files')
    for file in files:
        file_path = f"files/{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
    return{"success":True, "message":"files has uploaded successfully"}

@app.get("/reset-db")
async def resetdb():
    
    for name in os.listdir(db_directory):
        file = db_directory + name
        if(os.path.isfile(file)):
            os.remove(file)
            
        if(os.path.isdir(file)):
            shutil.rmtree(file)
            
    for cache in os.listdir(cache_directory):
        file = cache_directory + cache
        if(os.path.isfile(file)):
            os.remove(file)
            
        if(os.path.isdir(file)):
            shutil.rmtree(file)

        for doc in os.listdir(document_directory):
            file = document_directory + doc
            if(os.path.isfile(file)):
                os.remove(file)

            if(os.path.isdir(file)):
                shutil.rmtree(file)
        if(os.path.exists('./db')):
            shutil.rmtree('./db')
            
    return {"success": True, "message":"document and cache has been cleared"}

@app.get("remove-all-files")
async def removefiles():
    for doc in os.listdir(document_directory):
        file = document_directory + doc
        if(os.path.isfile(file)):
            os.remove(file)

        if(os.path.isdir(file)):
            shutil.rmtree(file)

# @app.post("remove-file")
# async def removefile()

    