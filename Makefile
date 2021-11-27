# Source files
SRCS = ./bin/infra.ts

INFRA_STACK_FILES = $(wildcard ./lib/*.ts)

# Name of generate file
TARGET = ""

$(TARGET): $(SRCS) $(INFRA_STACK_FILES) lambda_fn
	@echo "\n============================================================\n"
	@echo "SRCS: \n$(SRCS)\n"
	@echo "\n============================================================\n"
	npx cdk deploy
	@echo ""

lambda_fn:
	cd ./lib/lambda/cnvFile/; make


.PHONY: clean
clean:
	cd ./lib/lambda/cnvFile/; make clean

