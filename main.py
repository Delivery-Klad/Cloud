from os import environ, system


if __name__ == '__main__':
    try:
        environ['DATABASE_URL'] = "postgres://oztfqoifymridq:e98f174d929fc8109736c5013c7ca2981caf42d8f89a4a4609a53" \
                                     "4ea5f27279f@ec2-34-250-92-138.eu-west-1.compute.amazonaws.com:5432/d677ns4imct7mh"
        environ['server_url'] = "http://localhost:8000/"
        environ['dbx_token'] = "EOhAkm3Q_zQAAAAAAAAAAaEO_4EwwBq8QDFzIu4uIxDOwY3O_weedvtu0LURQnfp"
        environ['gh_token'] = "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"
        environ['secret'] = "d8daf4995572b8fb6dd6"
        system("uvicorn server:app --reload")
    except KeyboardInterrupt:
        exit(0)
