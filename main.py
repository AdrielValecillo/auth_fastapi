from fastapi import FastAPI, HTTPException, Depends


app = FastAPI()

@app.get("/")

def main():
    return {"Hello": "World"}

