# Source files
SRCS = ./index.py
SRCS_POETRY = ./poetry.lock ./poetry.toml ./pyproject.toml

# Name of generate file: 生成ファイル名
TARGET = deployment-package.zip

BUILD_DIR = tmp_build
TEST_DIR = tmp_test



$(TARGET): $(SRCS)
	@echo "\n============================================================\n"
	@echo "SRCS: \n$(SRCS)\n"
	@echo "\n============================================================\n"

	mkdir -p $(BUILD_DIR)
	cp -pR ./deployment_package_build_env/* ./$(BUILD_DIR)
	cp -r ./docker_sh ./$(BUILD_DIR)
	cp $(SRCS) ./$(BUILD_DIR)
	cp $(SRCS_POETRY) ./$(BUILD_DIR)

#	cd ./$(BUILD_DIR); ./build_dockerfile_by_DinD.sh
	cd ./$(BUILD_DIR); ./build_dockerfile_by_DooD.sh

	mv ./$(BUILD_DIR)/$(TARGET) ./
	@echo ""

.PHONY: test
build:
	mkdir -p $(TEST_DIR)
	cd test_env;


.PHONY: clean
clean:
	./$(BUILD_DIR)/clean_docker.sh
	rm -rf $(BUILD_DIR)
	rm -rf $(TARGET)
