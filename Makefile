.PHONY:	clean demo1

clean:
	find . -name __pycache__ -exec rm -r {} \; -prune

rich-demo:
	poetry run rich-demo

demo:
	poetry run python -m textual_tagset.demo

test:
	poetry run pytest -v

