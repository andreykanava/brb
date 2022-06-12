import pandas as pd
from binance.client import Client
import info
import requests
client = Client(api_key=info.api, api_secret=info.secret_api, testnet=True)
from discord.ext import commands
DS = commands.Bot(command_prefix='+')
DS.remove_command("help")
data = []
def BalanceUSDT():
    try:
        b=client.futures_account_balance()
        b = pd.DataFrame.from_dict(b)
        b = b.loc[b['asset']=='USDT']
        balance_USDT = float(b['balance'].values)
    except:
        balance_USDT=0
    return balance_USDT

def get_price(symbol, prices):
    for price in prices:
        if symbol == price['symbol']:
            return price['price']
bal = BalanceUSDT()
tbal = bal / 2
@DS.event
async def on_message(ctx):
    global data
    if ctx.author != DS.user:
        await ctx.reply(":white_check_mark: сигнал принят!:white_check_mark: ")
        rawdata = ctx.content
        rawdata = rawdata.split()
        data = rawdata
        print(data)
        symbol = data[0]
        symbol = symbol+"USDT"
        side = data[1]
        prices = requests.get('https://api.binance.com/api/v3/ticker/price').json()
        price = float((symbol, prices))
        if side == "LONG" and client.futures_get_open_orders(symbol=symbol) == []:
            print(data)
            pos = "BUY"
            q = tbal / price
            q = round(q, 2)
            client.futures_change_leverage(symbol=symbol, leverage=info.laverage)
            buyorder = client.futures_create_order(symbol=symbol, side=pos, type="LIMIT", quantity=q, price=price, timeInForce="GTC")
            stop = client.futures_create_order(symbol=symbol, side="SELL", type="STOP_MARKET", stopPrice=round(price*info.stoplong), closePosition="true")
            take = client.futures_create_order(symbol=symbol, side="SELL", type="TAKE_PROFIT_MARKET", stopPrice=round(price * info.takelong), closePosition="true")
            print(buyorder)
            await ctx.reply(":money_with_wings:Сделка открыта!:money_with_wings:")
        if side == "SHORT" and client.futures_get_open_orders(symbol=symbol) == []:
            print(data)
            pos = "SELL"
            q = tbal / price
            q = round(q, 2)
            client.futures_change_leverage(symbol=symbol, leverage=info.laverage)
            buyorder = client.futures_create_order(symbol=symbol, side=pos, type="LIMIT", quantity=q, price=price, timeInForce="GTC")
            stop = client.futures_create_order(symbol=symbol, side="SELL", type="STOP_MARKET", stopPrice=round(price * info.stopshort), closePosition="true")
            take = client.futures_create_order(symbol=symbol, side="SELL", type="TAKE_PROFIT_MARKET", stopPrice=round(price * info.takeshort), closePosition="true")
            print(buyorder)
            await ctx.reply(":money_with_wings:Сделка открыта!:money_with_wings:")

DS.run('')
