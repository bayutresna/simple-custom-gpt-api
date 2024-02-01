from train import app as train_app
from upload import app as upload_app
from customGPTAPI import app as gpt_app
from fastapi import FastAPI
import uvicorn

app = FastAPI()

app.mount("/upload", upload_app)
app.mount("/train",train_app)
app.mount("/chatGPT",gpt_app)


@app.get("/")
def get():
    return("skadi here")


if __name__ == "__main__":
    uvicorn.run("router:app", host="localhost", port=8080, reload=True)