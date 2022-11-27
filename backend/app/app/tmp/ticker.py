from pedesis.components.pubsub.maker import create_redis_pubsub

async def listen():
    import json
    client = create_redis_pubsub()
    await client.subscribe('1_future::BTC-USDT-SWAP:ticker')

    count = 10
    async for msg in client.listen():
        print(msg)
        # if msg['data'] != 1:
        #     print(json.loads(msg['data'])['data'][0]['last'])
        # count -= 1
        # if count == 0:
        #     break


if __name__ == '__main__':
    import asyncio
    asyncio.run(listen())
