venv:
	test -d venv || virtualenv venv
	venv/bin/pip3 install -r requirements.txt

run:
	venv/bin/python src/bot.py
