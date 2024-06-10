# GitHub Activity Tracker

## Overview
This application tracks activities on up to five configurable GitHub repositories using the GitHub Events API. It generates statistics based on a rolling window of either 7 days or 500 events, whichever is less. These statistics are available via a REST API.

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/timok19/github_activity_tracker.git
    cd github_activity_tracker
    ```

2. Create a virtual environment and install dependencies:
    ```sh
    pip3 install poetry
    poetry shell
    poetry install
    ```
    To install with development dependencies use `--with dev`
    ```sh
    poetry install --with dev
    ```

3. Set up `.env` file:
    ```sh
    touch .env
    ```
    Add necessary environment variables. Use `.env.example` as a reference:
    ```sh
    cp .env.example .env
    ```
    
4. Run the application:
    ```sh
    python3 main.py
    ```

## API Endpoints

### Fetch Events
- **URL:** `/api/github/fetch-events`
- **Method:** `GET`
- **Description:** Fetches the latest events from the configured GitHub repositories and stores them in the database if newer.

### Get Statistics
- **URL:** `/api/github/get-repo-stats`
- **Method:** `GET`
- **Parameters:**
  - `repo_name` (required): The name of the repository (e.g., `owner/repo1`).
  - `event_type` (required): The type of event (e.g., `PushEvent`).
- **Description:** Returns the average time between consecutive events for the specified repository and event type within the rolling window.

## Assumptions
- The GitHub token provided has the necessary permissions to access the events of the specified repositories.
- The application handles up to five repositories as per the given requirement. Number of repositories can be changed through the `.env` file

## Documentation
The code is documented to help understand the functionality and purpose of each part. Test cases are provided to ensure the application works as expected.

## Testing

### Run tests
1. Add `.env.test` file into `tests/` folder and fill necessary data for testing:
```sh
cp .env.example tests/.env.test
```

2. Run using `pytest` command:
```sh
pytest
```