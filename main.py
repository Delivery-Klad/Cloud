import os


if __name__ == '__main__':
    try:
        os.environ['root_psw'] = "root"
        os.environ['viewer_key'] = "user"
        os.environ['server_url'] = "http://localhost:8000/"
        os.environ['last_folder'] = "7 сем"
        os.system("uvicorn server:app --reload")
    except KeyboardInterrupt:
        exit(0)
