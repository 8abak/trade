import json
from ctrader_open_api.client import Client

with open("../credentials/creds.json", "r") as f:
    creds=json.load(f)

client=Client(
    clientId=creds["clientId"],
    clientSecret=creds["clientSecret"],
    accessToken=creds["accessToken"]
)


def handle_tick_data(message):
    ticks=message.payload.tick
    for tick in ticks:
        print(f"Symbol ID {tick.symbolId} >> Bid: {tick.bidPrice}, Ask: {tick.askPrice}, Time: {tick.timestamp}")


client.on_tick_data = handle_tick_data

print("starting tick stream...")
client.start()

client.send_subscribe_spot_price_request(
    ctid_trader_account_id=creds["accountId"],
    symbol_ids=[1,2]
)