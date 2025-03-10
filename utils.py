from amocrm.v2 import Contact as _Contact
from amocrm.v2 import Lead as _Lead
from amocrm.v2 import custom_field
from amocrm.v2 import tokens
from config import *


tokens.default_token_manager(
        client_id=client_id,
        client_secret=client_secret,
        subdomain=subdomain,
        redirect_url="https://meme.com/",
        storage=tokens.FileTokensStorage(),
    )




class Contact(_Contact):
    empl = custom_field.TextCustomField("рабочие")
    num_employees = custom_field.TextCustomField("num_emploeyes")
    turnover = custom_field.TextCustomField("оборот")
    role = custom_field.TextCustomField("роль")
    number = custom_field.ContactPhoneField(name="Телефон")


class Lead(_Lead):
    phone = custom_field.TextCustomField("phone")


def create_contact(name: str, number: str):
    contact = Contact.objects.create(
        name=name
    )
    contact.number = number
    contact.save()


def contact_save(num_emploeyes: str, turnover: str, role: str, number: str):
    contact = Contact.objects.get(query=number)
    contact.num_emploeyes = num_emploeyes
    contact.empl = num_emploeyes
    contact.turnover = turnover
    contact.role = role
    contact.save()


def lead_create_without_landing(phone_number, name):
    lead = Lead.objects.create(
        name=name,
        pipeline_id=int(voronka_id),
    )
    contact = Contact.objects.get(query=phone_number)
    lead.contacts.add(contact)
    lead.save()

# leads = Lead.objects.create(
#     name="Новая сделка 111",
#     price=500,
#     pipeline_id=voronka_id,
# )
# c = Contact.objects.get(query="+998999999990")
# leads.contacts.add(c)
# leads.save()




