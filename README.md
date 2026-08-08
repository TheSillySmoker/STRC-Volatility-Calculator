# STRC-Volatility-Calculator
Calculates the volatility of STRC compared to MSTR and BTC. It also shows how much the asset has remained within a trading range.  

Vibe Coded with ChatGPT

A Python script for analysing the historical closing-price behaviour of **Strategy Variable Rate Series A Perpetual Stretch Preferred Stock (STRC)**.

The script analyses how effectively STRC has traded around its $100 target price and compares its volatility with **Strategy (MSTR)** and **Bitcoin (BTC)**.

## Features

* Downloads all available STRC daily closing-price history
* Default target range of **$100–$95**
* Lower bound can be changed when the script starts
* Prices above $100 are treated as within the target range
* Calculates:

  * Days within and outside the target range
  * Highest and lowest closing prices
  * Average closing price
  * Average distance from $100
  * Number of excursions below the lower bound
  * Longest consecutive period below the lower bound
  * Recovery time for each excursion
* Produces a chart comparing:

  * STRC
  * MSTR
  * Bitcoin
* Includes normalised price performance and 20-day rolling volatility from the date STRC began trading

## Requirements

* Python 3
* Internet connection

Install the required Python packages:

```bash
pip install yfinance pandas numpy matplotlib
```

## Usage

Download or clone the repository, then run:

```bash
python3 strc_analysis.py
```

The script will ask:

```text
Enter lower bound [press Enter for $95.00]:
```

Press **Enter** to use the default $95 lower bound, or enter another value such as:

```text
97
```

This will change the analysis to the **$100–$97 target range**.

The script prints the STRC analysis directly in the terminal and generates:

```text
STRC_MSTR_BTC_volatility.png
```

containing the STRC, MSTR and Bitcoin volatility comparison.

## Data

Market data is retrieved using the `yfinance` Python package.

This project does not distribute historical market data. Users should review Yahoo Finance and yfinance terms before using or redistributing downloaded market data.

## Disclaimer

This project is for informational, research and educational purposes only. It is not financial advice.

## Licence

This project is licensed under the MIT Licence.

