.PHONY:	clean demo1

clean:
	find . -name __pycache__ -exec rm -r {} \; -prune

demo_tagset:
	PYTHONPATH=$$(pwd)/src poetry run textual run --dev textual_tagset.demo.demo_tagset

demo_tagset_selector:
	PYTHONPATH=$$(pwd)/src poetry run textual run --dev textual_tagset.demo.demo_tagset_selector

demo_filtered_tagset:
	PYTHONPATH=$$(pwd)/src poetry run textual run --dev textual_tagset.demo.demo_filtered_tagset

demo_filtered_tagset_selector:
	PYTHONPATH=$$(pwd)/src poetry run textual run --dev textual_tagset.demo.demo_filtered_tagset_selector

rich-demo:
	poetry run rich-demo

demo:
	make demo_tagset && make demo_tagset_selector && make demo_filtered_tagset && make demo_filtered_tagset_selector

test:
	poetry run pytest -v

