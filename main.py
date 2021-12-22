import os


if __name__ == '__main__':
    try:
        os.environ['server_url'] = "http://localhost:8000/"
        os.system("uvicorn server:app --reload")
    except KeyboardInterrupt:
        exit(0)
