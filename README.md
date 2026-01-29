📊 Data-Driven Stock Analysis

An interactive dashboard to analyze NIFTY-50 stock market data using Python, Streamlit, and Power BI.

🔍 Overview

This project analyzes stock performance by:

Cleaning and processing market data

Calculating returns and volatility

Visualizing trends through interactive dashboards


📁 Project Structure
Data-Driven Stock Analysis/
│
├── app.py                    # Streamlit application
├── requirements.txt          # Required Python libraries
├── README.md                 # Project documentation
│
├── Data/
│   └── CLEANED_DATA/
│       ├── Cleaned_nifty_50.csv
│       └── all_stock_data.csv
│
├── YAML_FILES/               # Raw stock data in YAML format
├── YAML_TO_CSV/              # YAML to CSV conversion scripts
│
├── Notebook/
│   └── stock_analysis.ipynb  # Data analysis notebook
│
├── PowerBI/
│   └── visualisation.pbix    # Power BI 
│
├── Screen prints             # Screen prints of  Power BI and Stream Lit
│
└── .venv/                    # Virtual environment


✨ Features

📈 Cumulative Return Analysis

🔥 Volatility Analysis

🏭 Sector-wise Performance

🔗 Stock Correlation Heatmap

📅 Monthly Gainers & Losers

🖥️ Streamlit Interactive Dashboard


🧰 Tech Stack

Python

Pandas, NumPy

Matplotlib, Seaborn, Plotly

Streamlit

Power BI

SQLAlchemy, PostgreSQL

YAML

🚀 Run the App
pip install -r requirements.txt
streamlit run app.py



👤 Author

Sanjay Kannan
Built with ❤️ using Python & Streamlit