from flask import Flask
from app import newDbWorker as dbWorker
from app import config
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
worker = dbWorker.worker()

from app import graphMaker

scheduler = BackgroundScheduler()

job = scheduler.add_job(graphMaker.make, 'interval', minutes=config.updateTime)
scheduler.start()

from app import views
