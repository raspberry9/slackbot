init:
	virtualenv -p python3 venv
	. venv/bin/activate && pip install -r requirements.txt

test:
	. venv/bin/activate && SLACK_API_TOKEN=xoxb-**** python -m pyslackbot

libtest:
	. venv/bin/activate && SLACK_API_TOKEN=xoxb-**** python pyslackbot/core.py

.PHONY: init test
