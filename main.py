import time
from web3 import AsyncWeb3, AsyncHTTPProvider
import asyncio

import aiohttp
from asgiref import sync


w3 = AsyncWeb3(AsyncHTTPProvider("https://polygon-rpc.com"))

headers = {"Content-Type": "application/json", 
           "Accept": "application/json", 
           "X-Api-Key":"8923f924-1f00-4a6a-b484-088e6ffed7f3", 
           "X-Kvv":"2", "X-Nonce":str(time.time()*1000), 
           "X-Sig":"c9e19286a2f159884f777947e6ab726827701fe8cd7ad8c0ef178d504d175af0",
           "Authorization":"ac449d50-133b-440f-bbdd-0acacc7a73a7",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
send_url = "https://api.dew.gg/uniapi/domains/dew/records/sign_mint_order"


# private_key = "dbddd9b01d20309f5f63bab37298fd8ab73078bf4c5e9bb901b4e4861b2d6a01"

wallets = ["dbddd9b01d20309f5f63bab37298fd8ab73078bf4c5e9bb901b4e4861b2d6a01","4028fe89d7e91d7f6457bd5442760d9c7bf19c506686548f054a208068272a9a"]


contract_address = '0xc9ae29bb6df1545fd14f282fc756c2cc8217ed59'
value = 0

names = ["ih","5j","6j"]

start = time.time()

mint_start_time = 1689900180

async def mint(data,private_key):

    transaction = {
        "to": w3.to_checksum_address(contract_address),
        "value": w3.to_wei(value, "ether"),
        "gas": 300000,  # Adjust gas according to your requirements
        "gasPrice": w3.to_wei("130", "gwei"),  # Adjust gas price according to your requirements
        "nonce": (await w3.eth.get_transaction_count(w3.to_checksum_address(w3.eth.account.from_key(private_key).address))),
        "chainId": 137,
        "data": data,
    }

    signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)

    # Send the transaction
    tx_hash = await w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    print(time.time()-start)
    tx_receipt = await w3.eth.wait_for_transaction_receipt(tx_hash)

    return tx_receipt



def request_sender():

    async def get_all():
        async with aiohttp.ClientSession() as session:

            async def fetch(name,private_key):
                json = {"name":str(name)}
                async with session.post(send_url, json = json,headers=headers) as response:
                    data = (await response.json())["data"]["mint_call_data"]
                    print(f"{name} - {data}")
                    return await mint(data,private_key)
                    
            return await asyncio.gather(*[
                fetch(name,wallet) for name, wallet in zip(names, wallets)
            ])
        

    return sync.async_to_sync(get_all)()


if __name__ == '__main__':

    while mint_start_time > time.time():
        print(f"wait - {mint_start_time - time.time()}")
        time.sleep(1)

    print("Minting")

    um = request_sender()
    print(um)