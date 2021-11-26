# Source files
SRCS = ./index.py

# Name of generate file: 生成ファイル名
TARGET = deployment-package.zip

$(TARGET): $(SRCS)
	@echo "\n============================================================\n"
	@echo "SRCS: \n$(SRCS)\n"
	@echo "CFLAGS: \n$(CFLAGS)"
	@echo "\n============================================================\n"
#	./build_dockerfile_by_DinD.sh
	./build_dockerfile_by_DooD.sh
	@echo ""

.PHONY: clean
clean:
	./clean.sh

