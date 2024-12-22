import asyncio
import random

from web3 import AsyncWeb3  # web3.py 6.14.0


class Client:
    def __init__(self, rpc: str, private_key: str | None = None):
        self.rpc = rpc

        self.w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc))
        if private_key:
            self.account = self.w3.eth.account.from_key(private_key=private_key)
        else:
            self.account = self.w3.eth.account.create(
                extra_entropy=str(random.randint(1, 999_999_999))
            )

    async def get_balance(self, address: str | None = None):
        if not address:
            address = self.account.address
        return await self.w3.eth.get_balance(account=address)

    async def check_account(self):
        return {
            "key_hex": self.account.key.hex(),
            "address": self.account.address,
            "balance": await self.w3.eth.get_balance(account=self.account.address),
        }


async def main():
    is_balance = False
    queue_counts = 5

    while not is_balance:
        # client = Client(rpc="https://arbitrum.llamarpc.com")
        # Создаем нужное количество клиентов для дальнейших действий с ними
        clients = [
            Client(rpc="https://rpc.ankr.com/arbitrum") for _ in range(queue_counts)
        ]
        tasks = [asyncio.create_task(client.check_account()) for client in clients]

        await asyncio.wait(tasks)

        print("**********************************")
        print("**********************************")
        for task in tasks:
            result = task.result()
            print(result)

            if result["balance"]:
                is_balance = True
                print("Баланс найден")


if __name__ == "__main__":
    asyncio.run(main())
