from amocrm.v2 import Lead, tokens
from config import *

tokens.default_token_manager(
        client_id=client_id,
        client_secret=client_secret,
        subdomain=subdomain,
        redirect_url="https://ya.ru/",
        storage=tokens.FileTokensStorage(),
    )

leads = Lead.objects.all()
for i in leads:
    print(i)
