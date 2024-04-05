from pytest import main
from iu_carrige.api import app
from os import putenv, environ


def start_test():
	import iu_datamodels
	main(['tests'])


def start_dev():
	from subprocess import run
	putenv('DEBUG', "YES")
	run(["uvicorn", "main:app", "--host=0.0.0.0",  "--port=8000", "--reload"], env=environ)
