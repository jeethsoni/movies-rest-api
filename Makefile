all: install black lint print-lint run
install:
	pip3 install -r requirements.txt
run:
	python3 app.py