# AI-Powered Cross-Market Arbitrage Platform

An AI-powered market intelligence project designed to identify potentially profitable second-hand electronics resale opportunities between France and Morocco.

## Overview

This project combines workflow automation, AI-assisted market research, and Python-based financial analysis to evaluate electronics listings from online marketplaces.

The objective is to reduce manual research and support more informed purchasing decisions.

## Key Features

- **Automated Listing Collection:** Scheduled Leboncoin monitoring using n8n and Apify.
- **AI-Powered Analysis:** Anthropic Claude evaluates device specifications, market prices, and potential risks.
- **Market Research:** Brave Search supports resale price estimation.
- **Profitability Engine:** Custom Python logic estimates acquisition costs and potential margins.
- **Risk Filtering:** Excludes suspicious, damaged, or potentially locked devices.
- **Notifications:** Telegram alerts for opportunities meeting predefined criteria.
- **Historical Tracking:** Google Sheets integration.

## Technology Stack

- Python
- JavaScript
- n8n
- Anthropic Claude
- Apify API
- Brave Search API
- Google Sheets
- Telegram Bot API
- pytest

## Python Profitability Engine

The `profitability.py` module calculates estimated resale margins for the French and Moroccan markets.

It supports configurable exchange rates, transport costs, minimum profit thresholds, and risk-based filtering.

Automated test cases are provided in `tests/test_profitability.py`.

### Run Tests

```bash
pip install pytest
python -m pytest -v
```

## Project Roadmap

- [x] Build the initial n8n automation
- [x] Implement the Python profitability module
- [x] Add unit test cases
- [ ] Refactor and improve the Python code using Claude Code
- [ ] Integrate the Python engine into n8n
- [ ] Build a market analytics dashboard
- [ ] Improve price estimation and risk scoring
- [ ] Add automated CI testing

## Disclaimer

Profit estimates are indicative and depend on market conditions, device condition, transaction costs, and applicable taxes. This system does not guarantee profitable transactions.

## Project Status

Active personal development project. The Python profitability module is available, while further integration and validation are ongoing.
