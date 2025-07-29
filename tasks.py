import asyncio

async def kitchen_task(id, task_name, delay):
    print(f"Task {id}: {task_name} started")
    await asyncio.sleep(delay)
    print(f"Task {id}: {task_name} done")
    return f"{task_name} finished"

async def main():
    make_pizza = asyncio.create_task(kitchen_task(1, "cooking pizza", 8))
    make_burger = asyncio.create_task(kitchen_task(2, "cooking burger", 5))

    print("Both tasks started...")

    result1 = await make_pizza
    result2 = await make_burger

    print(result1, result2)
    print("All cooking done!")

asyncio.run(main())
