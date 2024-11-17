# Usage Instructions

## Overview

This document provides detailed instructions on how to use the Toast Exports Sanitizer project.

## Prerequisites

Before using the project, ensure you have the following installed:

- Python 3.x
- pip (Python package installer)

## Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/mattemmett/toast-exports-sanitizer.git
   cd toast-exports-sanitizer
   ```

2. Create and activate a virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add the necessary environment variables:
   ```sh
   LOCATION_REPLACEMENT="YourLocationReplacement"
   EMPLOYEE_MAPPING='{"OriginalName": "ReplacementName"}'
   ```

## Configuration

The `config/config.yaml` file contains configuration parameters for the project. You can modify the parameters as needed.

## Running the Sanitizer

To use the sanitization script, run the following command:
```sh
python src/main.py <input_directory>
```
Replace `<input_directory>` with the path to the directory containing the Toast PoS export files you want to sanitize.

## Output

The sanitized files will be saved in the `output` directory.

## Testing

To run the unit tests, use the following command:
```sh
python -m unittest discover tests
```

## Contribution Guidelines

We welcome contributions to this project! If you would like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them with descriptive messages.
4. Push your changes to your forked repository.
5. Create a pull request to the main repository.

Please ensure that your code follows the project's coding standards and includes appropriate tests.
