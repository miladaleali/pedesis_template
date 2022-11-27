import asyncio

def load_okx_account(demo=False):
    from ccxt.async_support import okx
    import backend.app.app.apis as apis
    if demo:
        br = okx({
            'apiKey': apis.DemoApiKey,
            'secret': apis.DemoApiSecret,
            'password': apis.DemoPassphrase,
        })
        br.set_sandbox_mode(True)
        return br
    return okx(config={
        'apiKey': apis.ApiKey,
        'secret': apis.ApiSecret,
        'password': apis.Passphrase,
    })


okx = load_okx_account(True)
okx.aiohttp_proxy = "http://Zm0ExKmqUR:SCl64J5AUX@185.173.107.66:26737"
# okx.proxies = {'http': "http://Zm0ExKmqUR:SCl64J5AUX@185.173.107.66:26737"}
# okx.proxies = {'http': "http://127.0.0.1:20172"}

print(
    asyncio.run(okx.privateGetAccountPositions(dict(
        instType='SWAP',
        instId='BTC-USDT-SWAP'
    ))
    )
)

print(asyncio.run(okx.fetch_accounts()))

# print(asyncio.run(okx.publicGetSystemStatus()))