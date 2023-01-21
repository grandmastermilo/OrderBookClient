import asyncio



from order_book.client import BitfinexClient


async def main():
    client = BitfinexClient()

    print("starting client thread")
    client.start()

    print('subscribing to webscoket')
    await client.subscribe_OB()
    return 


if __name__ == '__main__':

    asyncio.get_event_loop().run_until_complete(main())