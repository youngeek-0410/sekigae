from fastapi import Form


class PaswordLoginSchema:
    def __init__(
        self,
        username: str = Form(...),
        password: str = Form(...),
    ):
        self.email = username
        self.password = password


class FirebaseLoginSchema:
    def __init__(
        self,
        idtoken: str = Form(...),
    ):
        self.idtoken = idtoken
