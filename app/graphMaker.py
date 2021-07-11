import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from app import worker as w
from datetime import timedelta
from app import config


def make():
    formatter = DateFormatter('%m/%d/%y')
    print('making graphs')

    plt.style.use('dark_background')

    for periodName in config.periods:
        a = w.getByLastTime(config.periods[periodName])
        fig, ax = plt.subplots()
        plt.plot(a[2], a[0], label='t (C)')
        plt.plot(a[2], a[1], label='h (%)')
        plt.gcf().autofmt_xdate()
        plt.grid(color=[0.47]*3 + [1])
        ax.legend()
        plt.savefig(f'./app/static/images/{periodName}.png', dpi=300)
        plt.close()
    for periodName in config.periods:
        a = w.getByLastTime(config.periods[periodName])
        fig, ax = plt.subplots()
        plt.plot(a[2], a[0], label='t (C)')
        plt.gcf().autofmt_xdate()
        plt.grid(color=[0.47]*3 + [1])
        ax.legend()
        plt.savefig(f'./app/static/images/temp-{periodName}.png', dpi=300)
        plt.close()
    for periodName in config.periods:
        a = w.getByLastTime(config.periods[periodName])
        fig, ax = plt.subplots()
        plt.plot(a[2], a[1], label='h (%)')
        plt.gcf().autofmt_xdate()
        plt.grid(color=[0.47]*3 + [1])
        plt.savefig(f'./app/static/images/hum-{periodName}.png', dpi=300)
        ax.legend()
        plt.close()
