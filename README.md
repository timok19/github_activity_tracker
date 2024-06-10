# GitHub Activity Tracker

## Overview
This application tracks activities on up to five configurable GitHub repositories using the GitHub Events API. It generates statistics based on a rolling window of either 7 days or 500 events, whichever is less. These statistics are available via a REST API.

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/github_activity_tracker.git
    cd github_activity_tracker
    ```

2. Create a virtual environment and install dependencies:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. Set up environment variables:
    ```sh
    export GITHUB_TOKEN=your_github_token
    ```

4. Run the application:
    ```sh
    python run.py
    ```

## API Endpoints

### Update Events
- **URL:** `/update_events`
- **Method:** `POST`
- **Description:** Fetches the latest events from the configured GitHub repositories and stores them in the database.

### Get Statistics
- **URL:** `/stats`
- **Method:** `GET`
- **Parameters:**
  - `repo_name` (required): The name of the repository (e.g., `owner/repo1`).
  - `event_type` (required): The type of event (e.g., `PushEvent`).
- **Description:** Returns the average time between consecutive events for the specified repository and event type within the rolling window.

## Assumptions
- The GitHub token provided has the necessary permissions to access the events of the specified repositories.
- The application handles up to five repositories as per the given requirement.

## Documentation
The code is documented with comments to help understand the functionality and purpose of each part. Test cases are provided to ensure the application works as expected.
