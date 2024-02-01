from fastapi import FastAPI, UploadFile, File
import os
import shutil
app = FastAPI() 

db_directory = "./db/"
cache_directory = "./__pycache__/"

@app.post("/")
async def upload(file:UploadFile = File(...)):
    file_path = f"files/{file.filename}"
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    return{"success":True, "file_path":file_path, "message":"file uploaded successfully"}

@app.get("/reset-db")
async def reset():
    
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
            
    return {"success": True, "message":"document and cache has been cleared"}



    