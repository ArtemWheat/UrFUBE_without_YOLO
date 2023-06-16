import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=9001,  log_level="info", use_colors=True, reload=True)
