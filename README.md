## Introduction

This repository contains the code for the Sage Internal Data Catalog Streamlit application, designed to monitor and visualize project metrics stored in the Synapse service.

## Repository Structure

The repository is organized as follows:
```bash
.
├── .github/                 # GitHub-specific configurations
├── .streamlit/              # Streamlit configuration files
├── .vscode/                 # VS Code-specific configurations
├── tests/                   # Unit tests for the application
├── toolkit/                 # Helper modules used within the app
│   ├── queries.py           # Contains SQL queries used in the app
│   ├── widgets.py           # Custom widgets for Streamlit UI
│   ├── utils.py             # Utility functions used across the app
├── .gitignore               # Files and directories to ignore in Git
├── Dockerfile               # Dockerfile for containerizing the app
├── LICENSE                  # License for this project
├── README.md                # This README file
├── __init__.py              # Marks the app as a package
├── app.py                   # Main entry point for the Streamlit app
├── requirements.txt         # Python dependencies
└── style.css                # Custom CSS for styling the Streamlit app

```

## Main Components

* `app.py`: The core of the Streamlit application. It imports functionalities from the toolkit/ directory to build the app interface and logic.
* `toolkit/`:
   * `queries.py`: Contains all the SQL queries used to fetch data from the Snowflake database.
   * `widgets.py`: Includes custom widgets used in the Streamlit UI for a more interactive experience.
   * `utils.py`: Provides utility functions that assist in various data processing tasks within the app.
   * `style.css`: Custom CSS used to style the Streamlit application, ensuring a consistent and visually appealing user interface.
   * `Dockerfile`: Defines the Docker image for the application, making it easy to deploy in various environments.
   * `tests/`: Contains unit tests to ensure that the functions and features within the app work as expected.

## Running the Application

TBD

## Deployment

TBD

## Contributing

Contributions are welcome! Please follow these steps to contribute:

    Fork the repository.
    Create a new branch for your feature/bugfix.
    Make your changes and write tests if applicable.
    Test the application by running it locally and executing your tests.[*]
    Submit a pull request with a clear description of your changes.

[*] To run the application locally after you've cloned the repository:

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app.py
```

## License
