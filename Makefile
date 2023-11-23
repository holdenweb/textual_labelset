.PHONY:	clean demo1

clean:
	find . -name __pycache__ -exec rm -r {} \; -prune

demo1:
	PYTHONPATH=$$(pwd)/src poetry run textual run --dev textual_tagset.demo.demo_tagset

demo2:
	PYTHONPATH=$$(pwd)/src poetry run textual run --dev textual_tagset.demo.demo_tagset_selector

demo3:
	PYTHONPATH=$$(pwd)/src poetry run textual run --dev textual_tagset.demo.demo_filtered_tagset

demo4:
	PYTHONPATH=$$(pwd)/src poetry run textual run --dev textual_tagset.demo.demo_filtered_tagset_selector

rich-demo:
	poetry run rich-demo

demo:
	make demo1 && make demo2 && make demo3 && make demo4

test:
	poetry run pytest -v

