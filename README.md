# Roulette Strategy Simulator
https://jieyuuuuu-roulette-strategy-simulator-app-nz7d3m.streamlit.app/
[中文版](README_zh.md)

### Introduction
This is a roulette casino strategy simulator designed for testing and comparing different betting strategies. Users can select various strategies, bet types, and betting modes while observing real-time capital changes.

### Features
- **Multiple Strategies**:
  - Martingale: Double bet after loss, reset after win
  - Anti-Martingale: Double bet after win, reset after loss
  - Fibonacci: Adjust bet amount based on Fibonacci sequence

- **Various Bet Types**:
  - Straight: Choose a single number (35:1 payout)
  - Split: Choose two adjacent numbers (17:1 payout)
  - Corner: Choose four intersecting numbers (8:1 payout)
  - Red/Black: Choose red or black (1:1 payout)

- **Betting Modes**:
  - Random Bet: Randomly select number/color for each bet
  - Fixed Bet: Maintain the same bet content

- **Real-time Visualization**:
  - Capital change curve
  - Detailed round data
  - Live key metrics updates

- **Customizable Parameters**:
  - Initial capital
  - Initial bet amount
  - Maximum rounds

- **Additional Features**:
  - Chinese/English interface switch
  - Simulation speed adjustment
  - Data export (CSV format)

### Installation & Running
1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run app.py
```

### Usage Guide
1. Select strategy, bet type, and betting mode in the sidebar
2. Set initial capital, bet amount, and number of rounds
3. Click "Start Simulation" button
4. Monitor capital changes and statistics
5. Adjust simulation speed as needed
6. Download detailed data after simulation completes

### Note
- This simulator is for educational purposes only
- Actual casino roulette games may have different rules and payouts
- Please view simulation results rationally and do not use them as reference for actual gambling
