.PHONY:	clean demo1

clean:
	find . -name __pycache__ -exec rm -r {} \; -prune

demo1:
	PYTHONPATH=$$(pwd)/src poetry run textual run textual_tagset.demo.tagset

demo2:
	PYTHONPATH=$$(pwd)/src poetry run textual run textual_tagset.demo.tagset_selector

demo3:
	PYTHONPATH=$$(pwd)/src poetry run textual run textual_tagset.demo.filtered_tagset

demo4:
	PYTHONPATH=$$(pwd)/src poetry run textual run textual_tagset.demo.filtered_tagset_selector

rich-demo:
	poetry run rich-demo