import os
from typing import Any

import dotenv
from asyncache import cached
from fast_bitrix24 import BitrixAsync

dotenv.load_dotenv()
_bitrix_webhook: str = os.getenv("BITRIX_WEBHOOK")
bx: BitrixAsync = BitrixAsync(_bitrix_webhook)


async def get_contact(contact_id: int) -> dict[str, Any]:
    return (await bx.get_by_ID(
        "crm.contact.get",
        (contact_id,),
    ))[str(contact_id)]


async def get_contact_fields() -> dict[str, Any]:
    return await bx.get_all(
        "crm.contact.fields",
    )


async def create_contact_gender_field() -> dict[str, Any]:
    return await bx.call(
        "crm.contact.userfield.add",
        {
            "fields": {
                "FIELD_NAME": "GENDER",
                "EDIT_FORM_LABEL": "Пол",
                "LIST_COLUMN_LABEL": "Пол",
                "USER_TYPE_ID": "string",
                "XML_ID": "GENDER",
            }
        },
    )


@cached({})
async def get_gender_field_id() -> str:
    for key, value in (await get_contact_fields()).items():
        if "listLabel" in value and str(value["listLabel"]).lower() == "пол":
            return key

    await create_contact_gender_field()
    return await get_gender_field_id()


async def set_contact_gender(contact_id: int, gender: str):
    gender_field_id: str = await get_gender_field_id()

    await bx.call(
        "crm.contact.update",
        {
            "id": contact_id,
            "fields": {
                gender_field_id: gender,
            }
        }
    )
