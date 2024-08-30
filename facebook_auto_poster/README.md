# Facebook Auto Poster

## Description

Facebook Auto Poster is a Python script that automates the process of logging into Facebook and posting a status update. It uses Selenium WebDriver to interact with the Facebook website, simulating user actions to log in and create a post.

## Features

-   Automated login to Facebook
-   Automated status posting
-   Configurable email, password, and status message
-   Utilizes explicit waits for improved reliability

## Prerequisites

Before you begin, ensure you have met the following requirements:

-   Python 3.6 or higher installed
-   Firefox browser installed (the script uses Firefox WebDriver)
-   Selenium library installed
-   Geckodriver (Firefox WebDriver) installed and in your system PATH

## Installation

1. Clone this repository.

2. Navigate to the project directory:

    ```
    cd facebook_auto_poster
    ```

3. Install the required Python packages:

    ```
    pip install selenium
    ```

4. Download the appropriate version of geckodriver for your system from the [official release page](https://github.com/mozilla/geckodriver/releases) and add it to your system PATH.

## Usage

1. Open the `facebook.py` file in a text editor.

2. Replace the placeholder values in the `main()` function with your actual Facebook credentials and desired status message:

    ```python
    email = "your_email@example.com"
    password = "your_password"
    status_message = "Hello, World!"
    ```

3. Run the script:
    ```
    python facebook.py
    ```

The script will open a Firefox browser, log into Facebook with the provided credentials, and post the specified status message.

## Configuration

You can modify the following variables in the `main()` function to customize the behavior:

-   `email`: Your Facebook account email
-   `password`: Your Facebook account password
-   `status_message`: The message you want to post as your status
