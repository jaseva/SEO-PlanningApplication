# SEO-PlanningApplication
# main.py
# MIT License
# Created Date: 2024-10-30
# Created By: Jason Evans
# Modified Date: 2024-10-30
# Modified By: Jason Evans
# Version 0.1

import requests
import pandas as pd
import os
from pytrends.request import TrendReq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up API keys (replace with actual API key variables from .env)
AHREFS_API_KEY = os.getenv("AHREFS_API_KEY")
SEMRUSH_API_KEY = os.getenv("SEMRUSH_API_KEY")

# Initialize Google Trends
pytrends = TrendReq(hl='en-US', tz=360)

# Function to fetch keyword metrics from Ahrefs
def get_keyword_metrics_ahrefs(keyword):
    url = f"https://apiv2.ahrefs.com?from=keywords_info&target={keyword}&token={AHREFS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "keyword": keyword,
            "volume": data.get('volume', 'N/A'),
            "difficulty": data.get('difficulty', 'N/A'),
            "clicks": data.get('clicks', 'N/A')
        }
    else:
        print(f"Error fetching data from Ahrefs: {response.status_code}")
        return None

# Function to fetch keyword trends from Google Trends
def get_trends_data(keyword):
    pytrends.build_payload([keyword], timeframe='today 12-m')
    trends_data = pytrends.interest_over_time()
    if not trends_data.empty:
        trends_data = trends_data.drop(columns=['isPartial'])
        return trends_data
    else:
        print(f"No trends data available for {keyword}.")
        return None

# Function to analyze competitors from SEMrush (simplified example)
def get_competitor_data_semrush(keyword):
    url = f"https://api.semrush.com/?type=phrase_this&key={SEMRUSH_API_KEY}&phrase={keyword}&export_columns=Ph,Nq,Db"
    response = requests.get(url)
    if response.status_code == 200:
        competitors = pd.read_csv(response.text)
        return competitors
    else:
        print(f"Error fetching data from SEMrush: {response.status_code}")
        return None

# Function to plan SEO strategy
def seo_strategy(keyword):
    # Get Ahrefs metrics
    ahrefs_data = get_keyword_metrics_ahrefs(keyword)
    if ahrefs_data:
        print("\n--- Keyword Metrics from Ahrefs ---")
        print(pd.DataFrame([ahrefs_data]))

    # Get Google Trends data
    trends_data = get_trends_data(keyword)
    if trends_data is not None:
        print("\n--- Google Trends Data ---")
        print(trends_data)

    # Get SEMrush competitor analysis
    competitor_data = get_competitor_data_semrush(keyword)
    if competitor_data is not None:
        print("\n--- Competitor Data from SEMrush ---")
        print(competitor_data.head())  # Display the top few rows

    # Plan summary
    print("\n--- SEO Strategy Summary ---")
    if ahrefs_data:
        print(f"Keyword Volume: {ahrefs_data['volume']}")
        print(f"Keyword Difficulty: {ahrefs_data['difficulty']}")
    if not trends_data.empty:
        print(f"Trend Insights: Check seasonal peaks for '{keyword}'")
    if competitor_data is not None:
        print(f"Top Competitors Analyzed: {competitor_data['Ph'].values[:5]}")

# Run SEO strategy function for a sample keyword
keyword = input("Enter a keyword for SEO analysis: ")
seo_strategy(keyword)
