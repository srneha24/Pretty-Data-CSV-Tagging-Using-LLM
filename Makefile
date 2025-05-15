# Unix-only Makefile for Python project setup
# Works on Linux, macOS, and Windows Subsystem for Linux (WSL)

# Variables
VENV_NAME := env
PYTHON := python3
PIP := $(VENV_NAME)/bin/pip
PYTHON_VENV := $(VENV_NAME)/bin/python
ACTIVATE := $(VENV_NAME)/bin/activate
REQUIREMENTS := requirements.txt
ENV_EXAMPLE := .env.example
ENV_FILE := .env
MAIN_FILE := main.py

# Set the shell to bash
SHELL := /bin/bash

.PHONY: all setup venv deps env run clean activate

# Default target
all: run

# Setup everything
setup: venv deps env

# Check if venv exists, create if it doesn't
venv:
	@if [ ! -d "$(VENV_NAME)" ]; then \
		echo "Creating virtual environment..."; \
		$(PYTHON) -m venv $(VENV_NAME); \
	else \
		echo "Virtual environment already exists."; \
	fi

# Install dependencies (activates venv first)
deps: venv
	@echo "Installing dependencies..."
	@source $(ACTIVATE) && pip install -r $(REQUIREMENTS)

# Create .env file from .env.example if .env doesn't exist
# Prompts for host and API key and replaces placeholders
env:
	@if [ -f "$(ENV_EXAMPLE)" ] && [ ! -f "$(ENV_FILE)" ]; then \
		echo "Creating $(ENV_FILE) from $(ENV_EXAMPLE)..."; \
		cp $(ENV_EXAMPLE) $(ENV_FILE); \
		echo "Please enter the host (press Enter to use default 'https://openrouter.ai/api/v1'):";\
		read -r LLM_HOST; \
		LLM_HOST=$${LLM_HOST:-"https://openrouter.ai/api/v1"}; \
		echo "Using host: $$LLM_HOST"; \
		escaped_host=$$(echo "$$LLM_HOST" | sed 's/[\/&]/\\&/g');\
		sed -i "s|<LLM_HOST>|$$escaped_host|g" $(ENV_FILE);\
		echo "Please enter your API key:"; \
		read -r LLM_API_KEY; \
		escaped_key=$$(echo "$$LLM_API_KEY" | sed 's/[\/&]/\\&/g'); \
		sed -i "s/<LLM_API_KEY>/$$escaped_key/g" $(ENV_FILE); \
		echo "$(ENV_FILE) created with your host and API key.";\
	elif [ ! -f "$(ENV_EXAMPLE)" ]; then \
		echo "Warning: $(ENV_EXAMPLE) not found. Cannot create $(ENV_FILE)."; \
	else \
		echo "$(ENV_FILE) already exists."; \
	fi

# Run the main application in the virtual environment
run: setup
	@echo "Running application..."
	@source $(ACTIVATE) && $(PYTHON_VENV) $(MAIN_FILE)

# Clean up Python cache files
clean:
	@echo "Cleaning up..."
	@rm -rf __pycache__
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete