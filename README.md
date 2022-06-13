# Whatsappy

This is an open sourse package to interact with WhatsApp Business Cloud API using Python.

We are looking for colaborators.

# How to Install

```pip install whatsappy```

or in virtual env

```python -m pip install whatsappy```

# Usage

## Text message

```from whatsappy.client import Client```

```client = Client(whatsapp_token, phone_number_id)```

```response = client.text_message("56999999999", "my first message")```
