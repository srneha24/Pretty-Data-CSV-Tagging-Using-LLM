# PRETTY DATA CSV TAGGING WITH LLM

## Running The Project

Use the following command to use the Makefile to run the project

```
make
```

The Makefile will handle creating the virtual environment, the .env and installing the dependencies. You will be asked to enter the host and the API key you want to use for the LLM. To use the default OpenRouter host, just press enter when prompted.

You can adjust the following values to your liking on the .env file that will be created

- CSV_FILE: Name of the CSV file to be read
- TAGGED_CSV_FILE: Name of the file to be created after the data have been tagged
- LLM: The LLM to use
- LLM_HOST: The host of the LLM
- LLM_API_KEY: The API key required to access the LLM host

## Sample Output

The sample output file is added to this repository - [services_tagged.csv](services_tagged.csv)

## Loom

[Here](https://www.loom.com/share/9400cc2f45fe467b88844ab4d449663e?sid=e69c5564-1f90-4577-ae72-1d9a5243d737) is the Loom video.