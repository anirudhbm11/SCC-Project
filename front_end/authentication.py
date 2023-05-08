

class Authentication:
    def __init__(self) -> None:
        pass

    def authentication_type(self, type):
        if type == "bearer":
            return self.bearer_token()
        else:
            raise NotImplementedError

    def bearer_token(self):
        bearer_token = "AAAAAAAAAAAAAAAAAAAAAGAkigEAAAAAwmk6%2Fe7Eh3iWZe%2FZLSbm7kQNMgs%3D5wrC7pnyYUoCaqgRDIfUtnXPunkdny4js1kLfr6uSrxCsud45K"
        return {"Authorization":"Bearer " + bearer_token}