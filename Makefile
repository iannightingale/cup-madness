.PHONY: init
init:
	rm -rf venv
	python3 -m venv venv
	. venv/bin/activate; pip install -r requirements.txt

.PHONY: run
run:
	. venv/bin/activate; python src/bracket.py