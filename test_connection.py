import time
import json
import pytest
import aioxmpp
import aioxmpp.dispatcher

SERVER_UP = False

def config_parser():
    with open('config.json','r') as f:
        config = json.loads(f.read())
    return config

# TODO: this is currently all hard coded, ideally it'd be an unpacked dict.
config = config_parser()
SEND_JID = aioxmpp.JID.fromstr(config['sending_jid'])
SEND_PASS = config['sending_password']
REC_JID = aioxmpp.JID.fromstr(config['receiving_jid'])
REC_PASS = config['receiving_password']
SERVER_1 = config['xmpp_server_1']
SERVER_2 = config['xmpp_server_2']


def create_client(jid:str, password:str) -> object:
    # TODO: find a more elegant way to wait for the server to come up. Currently it loops forever!
    global SERVER_UP
    while not SERVER_UP:
        try:
            client = aioxmpp.PresenceManagedClient(jid, aioxmpp.make_security_layer(password, no_verify=True))
            SERVER_UP = True
            return client
        except aioxmpp.errors.MultiOSError as e:
            time.sleep(10)
            print(e)


def message_received(msg):
  if msg.body != "Sierra Golf One Niner":
      return True
  else:
      return False


@pytest.mark.asyncio
async def test_send_message():
    client = create_client(SEND_JID, SEND_PASS)
    # This unused variable is a consequence of how aioxmpp works. They can be used, but aren't. However we
    # like the context handler. The same holds true for other methods
    async with client.connected() as stream:
        msg = aioxmpp.Message(
                to=REC_JID,
                type_=aioxmpp.MessageType.CHAT,
                )
        msg.body[None] = "This is from the script"
        await client.send(msg)


@pytest.mark.asyncio
async def test_send_non_latin():
    client = create_client(SEND_JID, SEND_PASS)
    async with client.connected() as stream:
        msg = aioxmpp.Message(
            to=SEND_JID,
            type_=aioxmpp.MessageType.CHAT,
        )
        msg.body[None] = "你好。 我叫柯荣顺"
        await client.send(msg)


@pytest.mark.asyncio
async def test_rec_message():
    rec_client = create_client(REC_JID, REC_PASS)
    sending_client = create_client(SEND_JID, SEND_PASS)
    message_dispatcher = rec_client.summon(aioxmpp.dispatcher.SimpleMessageDispatcher)
    message_dispatcher.register_callback(
        aioxmpp.MessageType.CHAT,
        None,
        message_received,
    )
    async with sending_client.connected() as sender_stream:
        msg = aioxmpp.Message(
            to = REC_JID,
            type_=aioxmpp.MessageType.CHAT,
        )
        msg.body[None] = "Sierra Golf One Niner"
        await sending_client.send(msg)

