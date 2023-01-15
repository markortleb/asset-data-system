# Asset Data System

A configurable ETL and reporting system for stock and ETF data.


## About

Enjoy gambling on the stock market but don't have any technical analysis
charts? Well you have come to the right place! Pick any set of stock or
ETF ticker symbols, and with the click of a button get a set of technical
analysis charts for each symbol. Now you have peace of mind when buying 
your 0 DTE out-of-the-money SPY options!


## Requirements

You will need Docker installed. The following installation guide was tested
on Linux Mint.


## Getting Started

Take a look at the **selected_ticker_symbols.txt** and add or remove ticker
symbols as you see fit. Then, do one of the following.

### Run the interactive dev mode

```bash
sudo make start-dev-mode
```

### Run prod mode
```bash
sudo make start
```


## How it works

Assume we run the prod mode. Here is what happens:

- Two docker containers are spun up:
  - A container with a MongoDB database running.
  - A container running a Python docker image. This is the controller.
  
- The controller container does the following on startup:
  - Runs startup actions defined in **bootstrap.sh**.
  - Runs a Python script to define and schedule tasks defined in
**scripts/compiler/bundler/templates/** for all ticker symbols in the 
**selected_ticker_symbols.txt**. The tasks are scheduled on the container's
cron scheduler.

- The basic outline for each task is:
  - Download ticker data from yfinance, and load it to the mongo database.
  - Pull ticker data from each collection, and create a set of technical
analysis reports from that data.

- Two untracked directories will be created in this repo:
  - **tasks/** will hold YML files for tasks to help with debugging.
  - **reports/** will hold the generated technical analysis reports.