.PHONY: all forms zip clean format check install
all: zip

forms: src/form_qt5.py src/form_qt6.py

PACKAGE_NAME := wrap_related_content

zip: forms $(PACKAGE_NAME).ankiaddon

src/form_qt5.py: designer/form.ui
	pyuic5 $^ > $@

src/form_qt6.py: designer/form.ui
	pyuic6 $^ > $@

$(PACKAGE_NAME).ankiaddon: src/*
	rm -f $@
	rm -rf src/__pycache__
	( cd src/; zip -r ../$@ * )

# Install in test profile
install: forms
	rm -rf src/__pycache__
	cp -r src/. ankiprofile/addons21/$(PACKAGE_NAME)

format:
	python -m black src/ --exclude="form_qt(5|6)\.py"

check:
	python -m mypy src/

clean:
	rm -f $(PACKAGE_NAME).ankiaddon
