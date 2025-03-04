# Fintual Stocks Portfolio Simulator

## Overview
Fintual Stocks Portfolio is a Python-based project designed to simulate a portfolio of stocks and calculate profit and annualized return between specified dates.

## Features
- **Portfolio Management:**
  Manage a collection of stocks with daily price histories.
- **Transaction Recording:**
  Record sequential buy/sell transactions for each stock.
- **Financial Calculations:**
  Compute portfolio value, profit over a period, and annualized return.

## Architecture
The project is built around the following components:
- **PriceHistory:**
  A dataclass that stores daily prices for a stock.
- **TransactionHistory:**
  A dataclass that stores transactions and maintains a cumulative total (daily_accumulated) using a simple cumulative total mechanism.
- **Stock:**
  Represents a single stock; ties together a PriceHistory and a TransactionHistory. Provides methods for obtaining the stock’s price, effective shares, and value.
- **Portfolio:**
  Manages a collection of Stock objects. Calculates overall portfolio value, profit, and annualized return.

## Installation & Running

### Prerequisites
- Python 3.12 (or Python ≥ 3.7)
- Docker (optional, for containerized development)

### Running Locally
1. **Clone the repository.**
2. **Run tests:**
   ```bash
   python -m unittest
   ```
   Or docker can be used as well:
   ```bash
   docker-compose run -T app python -m unittest
   ```


## Understanding the Implementation Through Tests

Review the tests in the `tests/` directory to gain insight into the design and behavior of the system. The tests are organized as follows:

- **Unit Tests:**
  Each module has dedicated tests that cover individual components:
  - **PriceHistory Tests:** Verify that historical prices are correctly retrieved and that the list of available dates is accurate.
  - **TransactionHistory Tests:** Confirm that transactions are recorded sequentially and that the cumulative (effective) shares are computed properly.
  - **Stock Tests:** Ensure that a stock returns the correct price, effective shares, and overall value based on its price and transaction histories.

- **Integration Tests:**
  The integration tests demonstrate how the components work together in realistic scenarios:
  - **Portfolio Tests:** Validate that the Portfolio class correctly aggregates multiple stocks, calculates overall portfolio value, profit between two dates, and annualized return over specified periods.

By reading these tests, you'll gain a deeper understanding of the implementation details and the design decisions behind the application.
