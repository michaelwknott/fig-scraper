# fig-scraper

## About the Project

A script to scrape Fédération Internationale de Gymnastique results. Currently the script only supports scraping results from the following [url](https://live.gymnastics.sport/live/17242/mensqual.php?app=fx).

## Built With

+ [Python](https://www.python.org/)

## Getting Started

### Prerequisites

+ Python 3.11 or higher

### Installation

To get a local copy up and running, follow these simple steps.

1. Clone the repo
    ```bash
    git clone git@github.com:michaelwknott/fig-scraper.git
    ```
2. Create a virtual environment
    ```bash
    python -m venv .venv --prompt .
    ```
3. Activate the virtual environment
    ```bash
    source .venv/bin/activate
    ```
4. Install dependencies
    ```bash
    python -m pip install -r requirements.txt
    ```
5. Run the script
    ```bash
    python script.py
    ```
6. The script has run successfully if the following message is displayed
    ```bash
    200 response from https://live.gymnastics.sport/live/17242/mensqual.php?app=fx
    ```

## License

Distributed under the MIT License. See LICENSE for more information.