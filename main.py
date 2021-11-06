import os


if __name__ == '__main__':
    try:
        os.environ['root_psw'] = "r00t"
        os.environ['viewer_key'] = "user"
        os.environ['server_url'] = "http://localhost:8000/"
        os.system("uvicorn server:app --reload")
    except KeyboardInterrupt:
        exit(0)
