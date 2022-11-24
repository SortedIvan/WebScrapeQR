from fastapi import FastAPI

app = FastAPI()
# app.include_router(agreement_key.router)


@app.get("/")
async def root():
  return {"message": "Hello world!"}

