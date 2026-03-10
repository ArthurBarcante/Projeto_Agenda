from fastapi import FastAPI

from app.core.config.uuid7 import generate_uuid7

app = FastAPI()


@app.get("/")
def root():
    return {"status": "AIGENDA Phase 1 pronta", "request_id": str(generate_uuid7())}


@app.get("/uuid7")
def uuid7_sample():
    value = generate_uuid7()
    return {"uuid": str(value), "version": value.version}
