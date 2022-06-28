import websocket
import numpy as np
import json5 as json
import beepy
import pandas as pd

money=100
pf=100
q=0
cp=0
bought=False

def buy(m,cp) :
    global q
    q=m/cp
    be=str(q)
    curprice=str(cp)
    print("EHEREUM BOUGHT  : "+be +"@"+curprice)


def update(q,cp):
    global  pf
    pf=q*cp
    portfolio=str(pf)
    print("Current PORTFOLIO value "+portfolio)

def sell(q,cp):
    global  pf,money
    pf=q*cp
    money=pf
    be=str(q)
    curprice=str(cp)
    print("SOLD " + be + " of ethereum @ " + curprice)




socket = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

def on_open(ws) :
    handle={ 'money' : money , 'pf' : pf , 'q' : q  }
    print(handle)


def on_close(ws):
    print("CLOSED")


def on_message(ws, message):
    global  pf,q,money
    json_mes = json.loads(message)
    candle = json_mes['k']
    cp = candle['c']
    cclosed = candle['x']
    lastprice=float(cp)
    print(lastprice)
    global bought


    if bought==False:
        buy(money,lastprice)
        beepy.beep(3)
        bought=True

    update(q,lastprice)

    if pf > money + 0.05 :
        sell(q,lastprice)
        beepy.beep(4)
        bought=False





ws = websocket.WebSocketApp(socket, on_open=on_open,on_message=on_message, on_close=on_close)


ws.run_forever()




