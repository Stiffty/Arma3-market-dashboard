import argparse
import datetime
import json
import time
from threading import Timer

import pandas as pd
import plotly.express as px
import requests
from dash import Dash, html, dcc, Output, Input

# Interval in which the dashboard is updated
interval_in_minutes = 2

app = Dash(__name__)


def make_request(cookie):
    try:
        cookies = dict(wsc_267ea4_cookieHash=cookie)
        x = requests.get('https://www.lyl.gg/lyl-api/arma-dashboard.php', cookies=cookies)

        request_text = x.text
        index_bracket = x.text.index('{')
        if index_bracket != 0:
            request_text = request_text[index_bracket:]
        return json.loads(request_text)

    except:
        print('Error! : You probably have to update your cookie.')
        exit(-1)


def fetch_data_loop(cookie, interval):
    while True:
        json_new_request = make_request(cookie)
        print('New data fetched')
        global json_market_now
        global json_market_history

        list_of_products = reformat_data([safe_data(json_new_request)])
        json_market_now = {'market': list_of_products}
        json_market_history['data'] = json_market_history['data'] + list_of_products

        time.sleep(interval * 60)


@app.callback(
    Output('history-graph', 'figure'),
    [Input('graph-update', 'n_intervals')])
def history_graph_callback(n):
    global json_market_history
    new_df = pd.DataFrame(json_market_history['data'])

    return px.line(new_df, x="updateTime", y="diff", color="name",
                   title='History of the difference in price')


@app.callback(
    Output('overview-graph', 'figure'),
    [Input('graph-update', 'n_intervals')])
def overview_graph_callback(n):
    global json_market_now
    new_df = pd.DataFrame(json_market_now['market'])

    return px.line(new_df, x="diff", y="price", color="name", markers=True,
                   title='Current market overview (depending on the position on the x-axis of a dot the more(left) or less(right) the product is farmed)')


def reformat_time(time_as_int):
    return datetime.datetime.fromtimestamp(time_as_int).strftime(
        "%H:%M:%S")


def reformat_data(data_as_list):
    json_history = []
    for line in data_as_list:
        json_line = json.loads(line)
        for product in json_line['market']:
            product['updateTime'] = json_line['updateTime']
            json_history.append(product)
    return json_history


def load_data():
    try:
        with open('data', 'r') as f:
            lines = [line.rstrip() for line in f]

        return {'data': reformat_data(lines)}
    except:
        print("Creating new file...")
        return None


def safe_data(json_request):
    json_for_safe = {'updateTime': reformat_time(json_request['updateTime']),
                     'market': json_request['market']}
    json_for_safe_as_string = json.dumps(json_for_safe)
    with open('data', 'a') as f:
        f.write(json_for_safe_as_string + '\n')

    return json_for_safe_as_string


# Handle passed arguments
parser = argparse.ArgumentParser(
    description='A visualisation of market data fetched from the website of the arma 3 server lyl. ')
parser.add_argument('cookie', type=str,
                    help='The value of the wsc_267ea4_cookieHash from the request to https://www.lyl.gg/lyl-api/arma-dashboard.php.')
parser.add_argument('-i', '--interval', type=int,
                    help='Sets the interval in minutes in which new data is fetched from the website. (default is 5)',
                    default=5)
args = parser.parse_args()

# Fetch first data
print('Fetching first data')
json_first_request = make_request(args.cookie)
safe_data(json_first_request)

json_market_now = json_first_request

print('Load old data if existing')
json_market_history = load_data()

# start update/fetch loop
print('Start loop to fetch new data')
Timer(5, fetch_data_loop, [args.cookie, args.interval]).start()

# init dataframes for graphs
df = pd.DataFrame(json_market_now['market'])
df2 = pd.DataFrame(json_market_history['data'])

# creating graphs
overview_graph = px.line(df, x="diff", y="price", color="name", markers=True,
                         title='Current market overview (depending on the position on the x-axis of a dot the more(left) or less(right) the product is farmed)')

history_graph = px.line(df2, x="updateTime", y="diff", color="name",
                        title='History of the difference in price')
pie_chart = px.pie(df, values="price", names="name", title='Most profit')
pie_chart.update_traces(textposition='inside', textinfo='value+label')

# setting up the dashboard layout
app.layout = html.Div(children=[
    html.H1(children='Market overview'),

    html.Div(children='''
        A visualisation of market data fetched from the website of the arma 3 server lyl. 
    '''),
    dcc.Interval('graph-update', interval=interval_in_minutes * 60 * 1000, n_intervals=0),
    dcc.Graph(
        id='overview-graph',
        figure=overview_graph
    ),
    dcc.Graph(
        id='pie-chart',
        figure=pie_chart
    ),
    dcc.Graph(
        id='history-graph',
        figure=history_graph
    ),
])

if __name__ == '__main__':
    app.run_server(debug=False)
