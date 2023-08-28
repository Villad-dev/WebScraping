# WebScraping(Flight Crash Statistics Dashboard)

Welcome to the Flight Crash Statistics Dashboard project! This application is designed to scrape flight crash data from [Aviation Safety Network](https://aviation-safety.net/database/) using Selenium in Python and present the statistics on your own website using Dash and Plotly graphs. The data covers flight crashes from 1919 to 2023.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## Features

- Web scraping flight crash data from [Aviation Safety Network](https://aviation-safety.net/database/) using Selenium.
- Displaying statistics and visualizations of flight crashes using Dash and Plotly.
- Data covers the period from 1919 to 2023, providing a comprehensive overview of historical flight incidents.
- Predicting by trained data future catastrophies with losses in crew and passengers.

## Installation

Follow these steps to set up and run the Flight Crash Statistics Dashboard on your local machine:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Villad-dev/WebScraping.git
   cd WebScraping

## Usage

To use this application, follow these steps:

### Step 1: Web Scraping

1. Import the necessary modules for web scraping:

import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException

### Step 2:

1. Process and format the scraped data as needed using the Pandas library.

import pandas as pd
from dateutil import parser


### Step 3:

Dash Dashboard
1. Import the necessary modules for creating the Dash dashboard:

import dash
import base64
import requests
import pandas as pd
import plotly.express as px
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output

2. Launch the Dash application by running the app.py script:

python app.py

3. Open your web browser and navigate to http://localhost:8050 to interact with the dashboard.

4. Remember to customize the code as needed to fit your specific use case and data processing requirements.

## Screenshots

![image](https://github.com/Villad-dev/WebScraping/assets/83395350/48ab0a30-e8f9-4d7e-baf8-2a140892f917)

![image](https://github.com/Villad-dev/WebScraping/assets/83395350/5155cf74-032d-4915-a2d1-a2bfbde436d9)

![image](https://github.com/Villad-dev/WebScraping/assets/83395350/764c82e3-20d1-4bad-b160-f5984ec2d612)

![image](https://github.com/Villad-dev/WebScraping/assets/83395350/79d0870f-8e02-4b71-b463-bfb83214341b)

![image](https://github.com/Villad-dev/WebScraping/assets/83395350/3631cace-21ec-4edb-9f6d-401204a616b2)




## License

This project is licensed under the MIT License.


For applying all visual features beter to use Visual Studio code or whatever.


