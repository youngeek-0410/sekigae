from fastapi import Form


class PaswordLoginSchema:
    def __init__(
        self,
        username: str = Form(...),
        password: str = Form(...),
    ):
        self.email = username
        self.password = password
