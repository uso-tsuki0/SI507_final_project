# Billboard Influence Network

## Overview

The **Billboard Influence Network** is a Python script that interacts with an interface to query and analyze Billboard chart data, artist information, and graph-based metrics.

**CAUTION:** API queries may take more than 6 hours if cache is not used.

## Features

- Retrieve Billboard chart data.
- Get detailed information about a specific artist.
- Find the shortest path between two artists.
- Generate and visualize the influence network graph.
- Rank artists based on score, number of songs, and influence activity.

## Usage

1. Run the script using the following command:

    ```bash
    python final_project.py
    ```

2. You will be prompted to choose whether to use cache and save cache. Be cautious, as API queries without cache may take a significant amount of time.

3. Wikipedia private key should be provided because the query amount exceed the none-authentication limit.
    Wikipedia api can be applied here: https://api.wikimedia.org/wiki/Special:AppManagement

4. The script will load the required content. Once loaded, you will be presented with a menu of options:

    - **1. Get billboard chart**
    - **2. Get artist information**
    - **3. Get shortest path between two artists**
    - **4. Get graph**
    - **5. Get rank by score**
    - **6. Get rank by number of songs**
    - **7. Get rank by influence activity**
    - **8. Exit**

5. Choose an option by entering the corresponding number (1-8).

6. Follow the prompts to perform the selected operation.

7. After each operation, you will be asked if you want to continue. Enter 'y' to continue or 'n' to exit.

## Requirements

- Python 3.x
- requests, json, re, ast, pandas, bs4, time, numpy, networkx, matplotlib, pandas, seaborn

