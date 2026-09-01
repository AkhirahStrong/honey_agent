from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def root():
    return {
        "application": "PromptWatch Honey Agent",
        "status": "online"
    }