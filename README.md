# Whatsappy

This is an open sourse package to interact with WhatsApp Business Cloud API using Python.

We are looking for colaborators.

## How to Install

`pip install whatsappy`

or in virtual env

`python -m pip install whatsappy`

## Usage

### Text message

```py
    from whatsappy.client import Client

    client = Client(whatsapp_token, phone_number_id)
    response = client.text_message(
        phone_number="56999999999",
        body="my first message"
    )
```

### Interactive button message

```py
    from whatsappy.client import Client

    client = Client(whatsapp_token, phone_number_id)
    response = client.interactive_button_message(
        phone_number="56999999999",
        titles=["button-1", "button-2"]
        body_text="my first button message"
    )
```
