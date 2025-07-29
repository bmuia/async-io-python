import asyncio
from collections import deque

# === FIBER CLASS ===
class Fiber:
    def __init__(self, name):
        self.name = name
        self.mailbox = asyncio.Queue()
        self.task = None  # Holds the asyncio task running the fiber

    async def send(self, message):
        await self.mailbox.put(message)

    async def run(self, on_idle_callback):
        print(f"[{self.name}] started and waiting for tasks...")
        while True:
            msg = await self.mailbox.get()
            if msg == "stop":
                print(f"[{self.name}] stopping.")
                break

            task_name, delay = msg
            print(f"[{self.name}] doing task: {task_name} (takes {delay}s)")
            await asyncio.sleep(delay)  # Simulate the work
            print(f"[{self.name}] finished task: {task_name}")

            # Tell scheduler this fiber is idle again
            await on_idle_callback(self)

# === SCHEDULER CLASS ===
class Scheduler:
    def __init__(self, max_fibers=3):
        self.max_fibers = max_fibers
        self.idle_fibers = deque()  # Available fibers
        self.all_fibers = []

    async def start(self):
        # Create and start all fibers
        for i in range(self.max_fibers):
            fiber = Fiber(f"fiber-{i}")
            self.idle_fibers.append(fiber)
            task = asyncio.create_task(fiber.run(self.fiber_became_idle))
            fiber.task = task
            self.all_fibers.append(fiber)

    async def fiber_became_idle(self, fiber):
        self.idle_fibers.append(fiber)

    async def schedule(self, task_name, delay):
        while not self.idle_fibers:
            await asyncio.sleep(0.1)  # Wait for any fiber to free up

        fiber = self.idle_fibers.popleft()
        await fiber.send((task_name, delay))

    async def shutdown(self):
        for fiber in self.all_fibers:
            await fiber.send("stop")
        for fiber in self.all_fibers:
            await fiber.task

# === RUN IT ALL ===
async def main():
    scheduler = Scheduler(max_fibers=3)
    await scheduler.start()

    await scheduler.schedule("Cook Pizza", 5)
    await scheduler.schedule("Make Burger", 2)
    await scheduler.schedule("Fry Chicken", 3)
    await scheduler.schedule("Bake Cake", 4)
    await scheduler.schedule("Mix Salad", 1)

    await asyncio.sleep(8)  # Let everything finish
    await scheduler.shutdown()

asyncio.run(main())
