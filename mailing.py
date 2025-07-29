import asyncio

chef_mailbox = asyncio.Queue()

async def waiter():
    print("Waiter: Got the order 1 pizza")
    await chef_mailbox.put("Make i izaa for table 4")
    print("Send order the chief")

async def chef():
    print("chef: waiting for orders")
    order = await chef_mailbox.get()
    print(f"chef: Got order: {order}")
    await asyncio.sleep(10)
    print("chef: done cooking")

async def main():
    task1 = asyncio.create_task(waiter())
    task2 = asyncio.create_task(chef())
    await task1
    await task2


asyncio.run(main())