from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = 'postgresql://svhvncepmsdzli:d7a6ac16728a7568b72a22ae3c55d90c5b875f83f09d4a857819e52d498a0365@ec2-63-34-153-52.eu-west-1.compute.amazonaws.com:5432/d3h814l24glv60'
    server_url: str = 'http://localhost/'
    dbx_token: str = 'fQdmKcU5PgsAAAAAAAAAAaGmxRMqV3tkdY5z2XS3coDiKDFzxEUo15jhnte6tcWM'
    gh_token: str = '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'
    secret: str = '32dcfe51aa8be2890f6ea05bb4'
    keys: str = '9c8eca4f-a030-448b-bdcf-b968267fa5ee, 8d9431cf-b91b-41f1-afe9-dd2c8161dd75, 2387f710-7cad-4409-a3cd-18e0d7e24220, e6586431-6ae2-4bdb-adf2-d06c826cf4ca, 957c19cc-7f9b-4226-9430-4d6ba74ab9e0, 584783b6-3fcf-4090-9cb0-f65a593129ed, 5cc07fa5-c7a4-4766-9704-2fea07237213, 437213f7-9568-438e-9746-7a6480ecad8c, 84d5b345-d1b2-4f90-a13a-ad144c946fda, f7db22d7-a908-42e1-8db4-afb1432d7bfa'
    debug: bool = True
    root_path: str = ''

    class Config:
        env_file = ".env"
