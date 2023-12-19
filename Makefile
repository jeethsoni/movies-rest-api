all: install black lint print-lint run
install:
	pip3 install -r requirements.txt
py3black:
	python3 -m black ./blueprints ./constants ./db app.py
pyblack:
	py -m black ./blueprints ./constants ./db app.py
lint:
	pylint ./constants/*.py ./blueprints ./db/*.py app.py > lint.log
print-lint:
	cat lint.log
run:
	python3 app.py
