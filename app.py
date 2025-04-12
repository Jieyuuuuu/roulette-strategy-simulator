"""
MIT License

Copyright (c) 2025 Jieyu
https://github.com/Jieyuuuuu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import random
from datetime import datetime
import time

# Language translation mapping
TRANSLATIONS = {
    "zh": {
        "title": "🎲 輪盤策略模擬器",
        "settings": "參數設置",
        "author": "作者",
        "github": "GitHub",
        "strategy": "選擇策略",
        "martingale": "馬丁賭法",
        "anti_martingale": "反馬丁賭法",
        "fibonacci": "斐波那契數列法",
        "martingale_desc": "輸局後下注翻倍，贏局後重置為初始下注金額。目的是通過翻倍來彌補之前的損失。",
        "anti_martingale_desc": "贏局後下注翻倍，輸局後重置為初始下注金額。目的是在好運時加大獲利。",
        "fibonacci_desc": "根據斐波那契數列調整下注金額，每次輸局增加至下一個數列值，贏局則退回兩個位置。",
        "bet_type": "選擇下注類型",
        "straight": "直注",
        "split": "分注",
        "corner": "角注",
        "red_black": "紅黑/奇偶",
        "straight_desc": "選擇單一數字（0至36），賠率 1:35",
        "split_desc": "選擇相鄰的兩個數字，賠率 1:17",
        "corner_desc": "選擇四個交叉點上的數字，賠率 1:8",
        "red_black_desc": "選擇紅色或黑色，賠率 1:1",
        "bet_mode": "選擇下注方式",
        "random_bet": "隨機下注",
        "fixed_bet": "固定下注",
        "random_bet_desc": "每次下注的數字/顏色都隨機選擇",
        "fixed_bet_desc": "每次下注都使用固定的數字/顏色",
        "initial_capital": "初始本金",
        "initial_bet": "初始下注金額",
        "max_rounds": "最大回合數",
        "start_simulation": "開始模擬",
        "slow": "慢速",
        "unlimited": "無限制",
        "speed_help": "開啟：無限制速度\n關閉：每回合 0.5 秒",
        "final_capital": "最終資金",
        "win_rate": "勝率",
        "profit_ratio": "盈虧比",
        "total_rounds": "總回合數",
        "total_profit": "總盈虧",
        "round": "回合",
        "current_capital": "當前資金",
        "current_bet": "當前下注",
        "detailed_data": "詳細數據",
        "download_data": "下載數據 (CSV)",
        "capital_curve": "資金變化曲線",
        "rounds": "回合數",
        "capital": "資金",
        "profit_ratio_help": "如果完成所有回合代表在設定回合內沒輸光，當前資金為最後持有的資金；如果在設定回合內結束則代表已輸光。",
        "initial_funds": "初始資金",
        "bet_number_prefix": "下注數字: ",
        "bet_color_prefix": "下注顏色: ",
        "win": "贏",
        "lose": "輸",
        "red": "紅",
        "black": "黑"
    },
    "en": {
        "title": "🎲 Roulette Strategy Simulator",
        "settings": "Settings",
        "author": "Author",
        "github": "GitHub",
        "strategy": "Select Strategy",
        "martingale": "Martingale",
        "anti_martingale": "Anti-Martingale",
        "fibonacci": "Fibonacci",
        "martingale_desc": "Double bet after loss, reset to initial bet after win. Aims to recover losses through doubling.",
        "anti_martingale_desc": "Double bet after win, reset to initial bet after loss. Aims to maximize profits during winning streaks.",
        "fibonacci_desc": "Adjust bet amount according to Fibonacci sequence, increase to next value after loss, go back two positions after win.",
        "bet_type": "Select Bet Type",
        "straight": "Straight",
        "split": "Split",
        "corner": "Corner",
        "red_black": "Red/Black",
        "straight_desc": "Choose a single number (0-36), payout 35:1",
        "split_desc": "Choose two adjacent numbers, payout 17:1",
        "corner_desc": "Choose four numbers at intersection, payout 8:1",
        "red_black_desc": "Choose red or black, payout 1:1",
        "bet_mode": "Select Bet Mode",
        "random_bet": "Random Bet",
        "fixed_bet": "Fixed Bet",
        "random_bet_desc": "Randomly select number/color for each bet",
        "fixed_bet_desc": "Use the same number/color for all bets",
        "initial_capital": "Initial Capital",
        "initial_bet": "Initial Bet",
        "max_rounds": "Max Rounds",
        "start_simulation": "Start Simulation",
        "slow": "Slow",
        "unlimited": "Unlimited",
        "speed_help": "On: Unlimited speed\nOff: 0.5s per round",
        "final_capital": "Final Capital",
        "win_rate": "Win Rate",
        "profit_ratio": "Profit Ratio",
        "total_rounds": "Total Rounds",
        "total_profit": "Total Profit",
        "round": "Round",
        "current_capital": "Current Capital",
        "current_bet": "Current Bet",
        "detailed_data": "Detailed Data",
        "download_data": "Download Data (CSV)",
        "capital_curve": "Capital Curve",
        "rounds": "Rounds",
        "capital": "Capital",
        "profit_ratio_help": "If all rounds are completed, it means you haven't lost all money within the set rounds. If it ends before max rounds, it means you've lost all money.",
        "initial_funds": "Initial Funds",
        "bet_number_prefix": "Bet Number: ",
        "bet_color_prefix": "Bet Color: ",
        "win": "Win",
        "lose": "Lose",
        "red": "Red",
        "black": "Black"
    }
}

# Initialize session state
if 'simulation_data' not in st.session_state:
    st.session_state.simulation_data = None
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'language' not in st.session_state:
    st.session_state.language = "en"

# Get current language translation
def t(key):
    return TRANSLATIONS[st.session_state.language][key]

# Page configuration
st.set_page_config(
    page_title=t("title"),
    page_icon="🎲",
    layout="wide"
)

# Reduce top padding
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
        }
    </style>
""", unsafe_allow_html=True)

# Main layout
col1, col2 = st.columns([6, 4])
with col1:
    st.title(t("title"))
with col2:
    st.write("")  # Add spacing
    st.write("")  # Add extra spacing for language toggle
    # Language toggle
    lang_col1, lang_col2, lang_col3 = st.columns([0.5, 0.5, 0.5])
    with lang_col1:
        st.write("中文 ")
    with lang_col2:
        is_english = st.toggle("", value=True, label_visibility="collapsed")
        st.session_state.language = "en" if is_english else "zh"
    with lang_col3:
        st.write(" EN")
    
    # Speed toggle
    speed_col1, speed_col2, speed_col3 = st.columns([0.5, 0.5, 0.5])
    with speed_col1:
        st.write(f"{t('slow')} ")
    with speed_col2:
        unlimited_speed = st.toggle("", value=True, help=t("speed_help"), label_visibility="collapsed")
    with speed_col3:
        st.write(f" {t('unlimited')}")

# Author information
st.sidebar.markdown("""
<style>
    .creator-box {
        border: 2px solid #ffffff;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
        background-color: transparent;
    }
    .creator-title {
        color: #ffffff;
        font-size: 1em;
        font-weight: 600;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
    }
    .github-link {
        color: #ffffff;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        font-size: 0.9em;
        gap: 4px;
    }
    .github-link:hover {
        text-decoration: underline;
        opacity: 0.8;
    }
    .github-icon {
        margin-right: 4px;
    }
</style>
<div class="creator-box">
    <div class="creator-title">
        Creator: Jieyu
    </div>
    <a href="https://github.com/Jieyuuuuu" class="github-link" target="_blank">
        <svg class="github-icon" height="16" width="16" viewBox="0 0 16 16">
            <path fill="currentColor" d="M8 0a8 8 0 00-2.53 15.59c.4.07.55-.17.55-.38l-.01-1.49c-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82a7.42 7.42 0 014 0c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48l-.01 2.2c0 .21.15.46.55.38A8 8 0 008 0z"/>
        </svg>
        GitHub Profile
    </a>
</div>
""", unsafe_allow_html=True)

st.sidebar.title(t("settings"))

# Strategy descriptions
strategy_descriptions = {
    t("martingale"): t("martingale_desc"),
    t("anti_martingale"): t("anti_martingale_desc"),
    t("fibonacci"): t("fibonacci_desc")
}

strategy = st.sidebar.selectbox(
    t("strategy"),
    [t("martingale"), t("anti_martingale"), t("fibonacci")]
)
st.sidebar.caption(f"💡 {strategy_descriptions[strategy]}")

# Bet type descriptions
bet_type_descriptions = {
    t("straight"): t("straight_desc"),
    t("split"): t("split_desc"),
    t("corner"): t("corner_desc"),
    t("red_black"): t("red_black_desc")
}

bet_type = st.sidebar.selectbox(
    t("bet_type"),
    [t("straight"), t("split"), t("corner"), t("red_black")]
)
st.sidebar.caption(f"💡 {bet_type_descriptions[bet_type]}")

# Bet mode descriptions
bet_mode_descriptions = {
    t("random_bet"): t("random_bet_desc"),
    t("fixed_bet"): t("fixed_bet_desc")
}

# Bet mode selection
bet_mode = st.sidebar.radio(
    t("bet_mode"),
    [t("random_bet"), t("fixed_bet")],
    index=0
)
st.sidebar.caption(f"💡 {bet_mode_descriptions[bet_mode]}")

# Parameter inputs
initial_capital = st.sidebar.number_input(
    t("initial_capital"),
    min_value=100,
    max_value=10000,
    value=1000,
    step=100
)

initial_bet = st.sidebar.slider(
    t("initial_bet"),
    min_value=1,
    max_value=500,
    value=10,
    step=1
)

max_rounds = st.sidebar.number_input(
    t("max_rounds"),
    min_value=10,
    max_value=1000,
    value=100,
    step=10
)

# Generate Fibonacci sequence
def generate_fibonacci(n):
    fib = [1, 1]
    while len(fib) < n:
        fib.append(fib[-1] + fib[-2])
    return fib

# Roulette simulator class
class RouletteSimulator:
    def __init__(self, initial_capital, initial_bet, max_rounds, strategy, bet_type, bet_mode):
        self.initial_capital = initial_capital
        self.initial_bet = initial_bet
        self.max_rounds = max_rounds
        self.strategy = strategy
        self.bet_type = bet_type
        self.bet_mode = bet_mode
        self.current_capital = initial_capital
        self.current_bet = initial_bet
        self.rounds_played = 0
        self.wins = 0
        self.fibonacci_sequence = generate_fibonacci(100)
        self.fibonacci_index = 0
        self.history = [
            {
                'round': 0,
                'capital': initial_capital,
                'bet': 0,
                'bet_content': t("initial_funds"),
                'result': '-',
                'number': '-',
                'payout': 0
            }
        ]
        
        # Set payout odds based on bet type
        self.odds = {
            "直注": 35,
            "分注": 17,
            "角注": 8,
            "紅黑/奇偶": 1
        }
        
        # Initialize bet settings
        self.setup_bet()
        # Save initial bet content for fixed bet mode
        if self.bet_mode == "固定下注":
            self.fixed_bet_number = getattr(self, 'bet_number', None)
            self.fixed_bet_numbers = getattr(self, 'bet_numbers', None)
            self.fixed_bet_color = getattr(self, 'bet_color', None)
            self.fixed_bet_description = self.bet_description
    
    def setup_bet(self):
        """Set up betting content"""
        if self.bet_mode == "固定下注" and self.rounds_played > 0:
            # Use saved bet content for fixed bet mode after first round
            if self.bet_type == "直注":
                self.bet_number = self.fixed_bet_number
            elif self.bet_type in ["分注", "角注"]:
                self.bet_numbers = self.fixed_bet_numbers
            elif self.bet_type == "紅黑/奇偶":
                self.bet_color = self.fixed_bet_color
            self.bet_description = self.fixed_bet_description
            return

        # Random bet or first round of fixed bet
        if self.bet_type == "直注":
            self.bet_number = random.randint(0, 36)
            self.bet_description = f"{t('bet_number_prefix')}{self.bet_number}"
        elif self.bet_type == "分注":
            # Select two adjacent numbers
            base_number = random.randint(1, 35)
            if random.choice([True, False]):  # Randomly choose horizontal or vertical
                self.bet_numbers = [base_number, base_number + 1]
            else:
                self.bet_numbers = [base_number, base_number + 3]
            self.bet_description = f"{t('bet_number_prefix')}{self.bet_numbers[0]},{self.bet_numbers[1]}"
        elif self.bet_type == "角注":
            # Select four intersecting numbers
            base_number = random.randint(1, 33)
            if base_number % 3 != 0:  # Ensure not rightmost number
                self.bet_numbers = [base_number, base_number + 1, 
                                  base_number + 3, base_number + 4]
                self.bet_description = f"{t('bet_number_prefix')}{self.bet_numbers[0]},{self.bet_numbers[1]},{self.bet_numbers[2]},{self.bet_numbers[3]}"
            else:
                self.setup_bet()  # Retry selection
        elif self.bet_type == "紅黑/奇偶":
            self.bet_color = t("red") if random.choice([True, False]) else t("black")
            self.bet_description = f"{t('bet_color_prefix')}{self.bet_color}"
    
    def spin(self):
        """Simulate roulette wheel spin"""
        return random.randint(0, 36)
    
    def is_win(self, number):
        """Check if bet wins based on the spun number"""
        if self.bet_type == "直注":
            return number == self.bet_number
        elif self.bet_type == "分注":
            return number in self.bet_numbers
        elif self.bet_type == "角注":
            return number in self.bet_numbers
        elif self.bet_type == "紅黑/奇偶":
            # Red numbers: 1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36
            red_numbers = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
            if self.bet_color == "紅":
                return number in red_numbers
            else:
                return number not in red_numbers and number != 0
    
    def calculate_payout(self, won):
        """Calculate payout based on bet result"""
        if won:
            # Net win (payout multiplier)
            return self.current_bet * self.odds[self.bet_type]
        else:
            # Loss of bet amount
            return -self.current_bet
    
    def update_bet(self, won):
        """Update bet amount based on strategy and result"""
        if self.strategy == "馬丁賭法":
            if won:
                self.current_bet = self.initial_bet
            else:
                self.current_bet *= 2
        elif self.strategy == "反馬丁賭法":
            if won:
                self.current_bet *= 2
            else:
                self.current_bet = self.initial_bet
        elif self.strategy == "斐波那契數列法":
            if won:
                self.fibonacci_index = max(0, self.fibonacci_index - 2)
            else:
                self.fibonacci_index += 1
            self.current_bet = self.initial_bet * self.fibonacci_sequence[self.fibonacci_index]
        
        # Reset bet content
        self.setup_bet()
    
    def play_round(self):
        """Play one round of roulette"""
        if self.current_capital <= 0 or self.rounds_played >= self.max_rounds:
            return False
        
        # Check if enough capital for bet
        if self.current_bet > self.current_capital:
            self.current_bet = self.current_capital
        
        # Record current capital before bet
        current_capital = self.current_capital
        
        number = self.spin()
        won = self.is_win(number)
        payout = self.calculate_payout(won)
        
        # Update capital after round
        self.current_capital += payout
        if won:
            self.wins += 1
        
        self.history.append({
            'round': self.rounds_played + 1,
            'capital': current_capital,
            'bet': self.current_bet,
            'bet_content': self.bet_description,
            'result': t("win") if won else t("lose"),
            'number': number,
            'payout': payout,
            'final_capital': self.current_capital
        })
        
        self.update_bet(won)
        self.rounds_played += 1
        
        return True

# Create metrics container
metrics_placeholder = st.empty()

if st.sidebar.button(t("start_simulation")):
    st.session_state.is_running = True
    
    # Map interface language to internal Chinese values
    strategy_map = {
        t("martingale"): "馬丁賭法",
        t("anti_martingale"): "反馬丁賭法",
        t("fibonacci"): "斐波那契數列法"
    }
    bet_type_map = {
        t("straight"): "直注",
        t("split"): "分注",
        t("corner"): "角注",
        t("red_black"): "紅黑/奇偶"
    }
    bet_mode_map = {
        t("random_bet"): "隨機下注",
        t("fixed_bet"): "固定下注"
    }
    
    simulator = RouletteSimulator(
        initial_capital, 
        initial_bet, 
        max_rounds, 
        strategy_map[strategy],
        bet_type_map[bet_type],
        bet_mode_map[bet_mode]
    )
    
    # Create progress indicators
    progress_bar = st.progress(0)
    status_text = st.empty()
    chart_placeholder = st.empty()
    
    # Set simulation speed
    delay = 0 if unlimited_speed else 0.5
    
    # Run simulation
    while simulator.play_round():
        # Add delay based on speed setting
        if delay > 0:
            time.sleep(delay)
            
        progress = simulator.rounds_played / max_rounds
        progress_bar.progress(progress)
        
        # Update status text
        status_text.text(f"{t('round')}: {simulator.rounds_played}/{max_rounds} | "
                        f"{t('current_capital')}: {simulator.current_capital:.0f} | "
                        f"{t('current_bet')}: {simulator.current_bet:.0f} | "
                        f"{t('win_rate')}: {(simulator.wins/simulator.rounds_played*100):.2f}%")
        
        # Update visualization
        df = pd.DataFrame(simulator.history)
        
        # Update metrics
        with metrics_placeholder.container():
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric(t("final_capital"), f"{simulator.current_capital:.0f}")
            with col2:
                win_rate = (simulator.wins/simulator.rounds_played*100)
                st.metric(t("win_rate"), f"{win_rate:.2f}%")
            with col3:
                profit_ratio = ((simulator.current_capital - initial_capital) / initial_capital) * 100
                st.metric(t("profit_ratio"), f"{profit_ratio:.2f}%", help=t("profit_ratio_help"))
            with col4:
                st.metric(t("total_rounds"), simulator.rounds_played)
            with col5:
                total_profit = simulator.current_capital - initial_capital
                st.metric(t("total_profit"), f"{total_profit:.0f}")
        
        # Update chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['round'],
            y=df['final_capital'],
            mode='lines',
            name=t('capital_curve')
        ))
        fig.update_layout(
            title=t('capital_curve'),
            xaxis_title=t('rounds'),
            yaxis_title=t('capital')
        )
        chart_placeholder.plotly_chart(fig, use_container_width=True)
    
    st.session_state.simulation_data = simulator.history
    st.session_state.is_running = False

# Display results after simulation
if st.session_state.simulation_data and not st.session_state.is_running:
    # Show detailed data
    st.subheader(t("detailed_data"))
    df = pd.DataFrame(st.session_state.simulation_data)
    st.dataframe(df)
    
    # Provide data download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=t("download_data"),
        data=csv,
        file_name=f"roulette_simulation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime='text/csv'
    )
    
    # Add bottom spacing
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
