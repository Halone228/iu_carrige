from pytest import main


def start_test():
	import iu_datamodels
	main(['tests'])


def start_dev():
	from uvicorn import run
	from iu_carrige.api import app
	run(app, host='0.0.0.0', port=8000)