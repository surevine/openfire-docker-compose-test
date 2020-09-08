# This will be based off the Python image
FROM python:3.8

RUN python3 -m pip install pytest aioxmpp pytest-asyncio --user
COPY test_connection.py .
COPY config.json .

