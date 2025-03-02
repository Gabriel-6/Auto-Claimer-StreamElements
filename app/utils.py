import aiohttp
import json
from time import sleep
from app.config import Config

def select_item_by_id(items):
    for index, item in enumerate(items, start=1):
        print(f"ID: {index} - ITEM: {item['name']}")

    try:
        item_id = int(input("Enter the item ID: "))

        return items[item_id - 1]
    except Exception:
        print("The ID is not valid")

async def get_account_name():
    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"Bearer {Config.JWTTOKEN}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
        }
        async with session.get("https://api.streamelements.com/kappa/v2/users/current", headers=headers) as request:
            response = json.loads(await request.text())
            return response['username']

async def get_channel_id():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.streamelements.com/kappa/v2/channels/{Config.CHANNEL}") as request:
            response = json.loads(await request.text())
            return response['_id']
        
async def get_items(id):
    async with aiohttp.ClientSession() as session:
        async with session.get(F"https://api.streamelements.com/kappa/v2/store/{id}/items?source=website") as request:
            itens = json.loads(await request.text())
            return [item for item in itens if item['enabled'] == True]
        
async def claim_item(item, channel_id):
    async with aiohttp.ClientSession() as session:
        data_c = {"input":[]}
        data_p = {"input":[], "message":f"{Config.MESSAGE}"}

        headers = {
            "Authorization": f"Bearer {Config.JWTTOKEN}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
        }
        username = await get_account_name()

        while True:
            async with session.get(f"https://api.streamelements.com/kappa/v2/points/{channel_id}/{username}", headers=headers) as request:
                response = json.loads(await request.text())
                total_points = response['points']

            if total_points >= item["cost"] and item["quantity"]["current"] > 0:
                if item["type"] == "code":
                    async with session.post(f"https://api.streamelements.com/kappa/v2/store/{channel_id}/redemptions/{item["_id"]}", headers=headers, json=data_c) as claim_item:
                        response = json.loads(await claim_item.text())
                        code = response["accessCode"]
                        await trigger_discord_webhook(code, Config.DISCORDWEBHOOK)
                        return
                if item["type"] == "perk":
                    async with session.post(f"https://api.streamelements.com/kappa/v2/store/{channel_id}/redemptions/{item["_id"]}", headers=headers, json=data_p) as claim_item:
                        response = json.loads(await claim_item.text())
                        sleep(item["cooldown"]["user"])
            else:
                print("Dont have enough points")

async def trigger_discord_webhook(code, webhook_url):
    async with aiohttp.ClientSession() as session:
        payload = {
                "content": "",
                "embeds": [{
                    "title": "Resgatado com Sucesso",
                    "description": f"{code}",
                    "color": 32768 
                }],
        }

        async with session.post(webhook_url, json=payload) as request:
            if request.status == 204:
                print("Mensagem enviada com sucesso!")
            else:
                print(f"Falha ao enviar a mensagem. Status: {request.status}")

        
