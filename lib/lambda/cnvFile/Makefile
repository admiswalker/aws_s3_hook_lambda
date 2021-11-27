SRCS = ./index.py
SRCS_POETRY = ./poetry.lock ./poetry.toml ./pyproject.toml

TARGET = deployment-package.zip

TMP_DIR = .venv __pycache__

$(TARGET): $(SRCS) $(SRCS_POETRY)
	@echo "\n============================================================\n"
	@echo "SRCS: \n$(SRCS)\n"
	@echo "\n============================================================\n"

#	./build_dockerfile_by_DinD.sh
	./build_dockerfile_by_DooD.sh


.PHONY: test
test:
	poetry install
	poetry run python test.py


.PHONY: clean
clean:
	./clean_docker.sh
	rm -rf $(TARGET)
	rm -rf $(TMP_DIR)
