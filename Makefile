ifeq ($(OS),Windows_NT)
RM = rmdir /s /q
BIN_PATH = ./venv/Scripts
PYTHON = python
ifdef ComSpec
SHELL := $(ComSpec)
endif
ifdef COMSPEC
SHELL := $(COMSPEC)
endif
else
RM = rm -rf
BIN_PATH = ./venv/bin
PYTHON = python3
endif

# Make default behavior the installing development package option
.DEFAULT_GOAL := install-dev
# https://www.gnu.org/software/make/manual/html_node/Phony-Targets.html
.PHONY := clean

PROJECT_DIR = speaker_test_bench
PACKAGE_PATH = src/speaker_test_bench
TEST_PATH = tests

# 1. BUILD VIRTUAL ENVIRONMENT -----------------------------------------------------------------------------------------
venv: requirements.txt
	@echo 1-Creating Python virtual env at the ${PROJECT_DIR} root path
	@echo *-----*
	${PYTHON} -m venv venv
	@echo 2-Upgrading pip version
	@echo *-----*
	${BIN_PATH}/${PYTHON} -m pip install --upgrade pip
	@echo 3-Installing dependencies from requirements.txt
	@echo *-----*
	${BIN_PATH}/${PYTHON} -m pip install -r requirements.txt

venv-dev: venv dev-requirements.txt
	@echo 4-Installing dependencies for devel environment
	@echo *-----*
	${BIN_PATH}/${PYTHON} -m pip install -r dev-requirements.txt

# 2. INSTALL PACKAGE ---------------------------------------------------------------------------------------------------
# pip -e, --editable <path/url> to install a project in editable mode
# https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs
install-dev: venv-dev
	@echo 5-Installing package ${PROJECT_DIR} in dev mode
	@echo *-----*
	${BIN_PATH}/${PYTHON} -m pip install -e ./
	${BIN_PATH}/pre-commit install
	${BIN_PATH}/pre-commit autoupdate

# 3. BUILD PACKAGE FOR EXPORT ------------------------------------------------------------------------------------------
build: venv
	@echo 5-Build ${PROJECT_DIR} as pure Python wheel
	@echo *-----*
	${BIN_PATH}/${PYTHON} setup.py sdist bdist_wheel

# **WARNING**
# For now this rule only works in Windows environment
export-test: test
	@echo 2-Prepare coverage of ${PROJECT_DIR} for export
	@echo *-----*
	mkdir coverage\tmp
	move coverage\*.html coverage\tmp
	move coverage\tmp\index.html coverage
	${RM} coverage\tmp

# 4. TEST PACKAGE FOR DEV ----------------------------------------------------------------------------------------------
test: venv-dev install-dev
	@echo 1-Running test and coverage for ${PROJECT_DIR}
	@echo *-----*
	${BIN_PATH}/coverage run -m pytest tests
	${BIN_PATH}/coverage html --show-contexts

# 5. LINTER & FORMATTING CODE ------------------------------------------------------------------------------------------
linter: venv-dev
	@echo Formatting code
	@echo *-----*
	${BIN_PATH}/black ./${PACKAGE_PATH}
	${BIN_PATH}/black ./${TEST_PATH}
	${BIN_PATH}/pylint ./${PACKAGE_PATH} --load-plugins=perflint

# 6. CLEANING PACKAGE FOR DEV ------------------------------------------------------------------------------------------
clean:
	@echo Cleaning project
	${RM} venv
	${RM} build
	@echo Cleaning completed

# 7. RUN SEVERAL RULES
all_hook: install-dev
	@echo Run all hook
	${BIN_PATH}/pre-commit run --all-files
