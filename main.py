import os


if __name__ == '__main__':
    try:
        os.environ['root_psw'] = "root"
        os.environ['viewer_key'] = "user"
        os.system("uvicorn server:app --reload")
    except KeyboardInterrupt:
        exit(0)
