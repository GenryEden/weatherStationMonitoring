from app import app
from app import worker
from app import config

import requests
from flask import render_template, request
from random import randint


@app.route('/')
@app.route('/index')
def index():
    data = worker.getLast()
    dbUrl = '/static/csv/db.csv?r='+str(randint(1,9**9))
    if data is None:
        t = {'value':'??', 'name':'градусов', 'url':'/t'}
        h = {'value':'??%', 'name':'влажности', 'url':'/h'}
    else:
        t = {'value':f'{data["temp"]}', 'name':'градусов', 'url':'/t'}
        h = {'value':f'{data["hum"]}%', 'name':'влажности', 'url':'/h'}
    graphs = []
    for period in config.periods:
        graphs.append(
            {
                'name': config.periods[period].title,
                'location': f'/static/images/{period}.png?r={str(randint(1,9**9))}'
            }
        )
    return render_template('index.html',
                            left=t,
                            right=h,
                            graphs=graphs,
                            dbUrl=dbUrl,
                            fullDB= len(graphs)%2,
                            title="Главная")


@app.route('/t')
@app.route('/temp')
def tempSite():
    data = worker.getLast()
    dbUrl = '/static/csv/db.csv?r='+str(randint(1,9**9))
    if data is None:
        t = {'value':'??', 'name':'градусов', 'url':'/t'}
    else:
        t = {'value':f'{data["temp"]}', 'name':'градусов', 'url':'/t'}
    back = {'value': 'Назад','name':'на домашнюю', 'url':'/'}
    graphs = []
    for period in config.periods:
        graphs.append(
            {
                'name': config.periods[period].title,
                'location': f'/static/images/temp-{period}.png?r={str(randint(1,9**9))}'
            }
        )
    return render_template('index.html',
                            left=t,
                            right=back,
                            graphs=graphs,
                            dbUrl=dbUrl,
                            fullDB= len(graphs)%2,
                            title="Температура")

@app.route('/h')
@app.route('/hum')
def humSite():
    data = worker.getLast()
    dbUrl = '/static/csv/db.csv?r='+str(randint(1,9**9))
    if data is None:
        h = {'value':'??%', 'name':'влажности', 'url':'/h'}
    else:
        h = {'value':f'{data["hum"]}%', 'name':'влажности', 'url':'/t'}
    back = {'value': 'Назад','name':'на домашнюю', 'url':'/'}
    graphs = []
    for period in config.periods:
        graphs.append(
            {
                'name': config.periods[period].title,
                'location': f'/static/images/hum-{period}.png?r={str(randint(1,9**9))}'
            }
        )
    return render_template('index.html',
                            left=back,
                            right=h,
                            graphs=graphs,
                            dbUrl=dbUrl,
                            fullDB= len(graphs)%2,
                            title="Температура")


@app.route('/api')
def apiAppend():
    args = request.args
    if 't' in args and 'h' in args and args.get('auth') == config.apiPassword:
        worker.append(args['t'], args['h'])
        return 'Nice'
    else:
        return 'None'

