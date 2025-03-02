import asyncio
from app.utils import *

async def main():
    channel_id = await get_channel_id()
    list_items = await get_items(channel_id)
    selected_item = select_item_by_id(list_items)
    claim = await claim_item(selected_item, channel_id)

if __name__ == "__main__":
    asyncio.run(main())