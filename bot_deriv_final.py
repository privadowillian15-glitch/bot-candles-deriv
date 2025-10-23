import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import websocket, json, threading, time, webbrowser

TOKEN = "COLE_SEU_TOKEN_AQUI"
SYMBOLS = {
    "EUR/USD": "frxEURUSD",
    "USD/JPY": "frxUSDJPY",
    "GBP/USD": "frxGBPUSD",
    "AUD/USD": "frxAUDUSD"
}

candles = {pair: [] for pair in SYMBOLS.values()}

def subscribe(symbol, granularity):
    ws = websocket.WebSocket()
    ws.connect("wss://ws.derivws.com/websockets/v3?app_id=1089")
    msg = {
        "ticks_history": symbol,
        "count": 100,
        "end": "latest",
        "granularity": granularity,
        "style": "candles"
    }
    ws.send(json.dumps(msg))
    response = json.loads(ws.recv())
    if "candles" in response:
        candles[symbol] = response["candles"]
    ws.close()

def update_data_loop(symbol, granularity):
    while True:
        subscribe(symbol, granularity)
        time.sleep(3)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("📈 Bot Deriv - Analisador de Candles em Tempo Real"),
    html.Div([
        html.Label("Escolha o par:"),
        dcc.Dropdown(
            id="pair",
            options=[{"label": k, "value": v} for k, v in SYMBOLS.items()],
            value="frxEURUSD"
        ),
        html.Label("Escolha o Timeframe:"),
        dcc.RadioItems(
            id="tf",
            options=[
                {"label": "1 Minuto", "value": 60},
                {"label": "5 Minutos", "value": 300},
                {"label": "15 Minutos", "value": 900}
            ],
            value=60,
            inline=True
        )
    ]),
    dcc.Graph(id="chart"),
    dcc.Interval(id="update", interval=5000, n_intervals=0)
])

@app.callback(Output("chart", "figure"),
              [Input("pair", "value"), Input("tf", "value"), Input("update", "n_intervals")])
def update_chart(pair, tf, _):
    if not candles[pair]:
        threading.Thread(target=update_data_loop, args=(pair, tf), daemon=True).start()
        return go.Figure()
    df = pd.DataFrame(candles[pair])
    fig = go.Figure(data=[go.Candlestick(
        x=df["epoch"],
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"]
    )])
    fig.update_layout(xaxis_rangeslider_visible=False, template="plotly_dark")
    return fig

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:8050")
    app.run(debug=False)
