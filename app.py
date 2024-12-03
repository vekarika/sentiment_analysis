import streamlit as st
from textblob import TextBlob
import pandas as pd
import plotly.express as px
import requests
from bs4 import BeautifulSoup


# Set up the page configuration with a title and a custom icon
st.set_page_config(page_title="Group 2 Sentiment Analysis", layout="centered")


# Add custom CSS for styling for a vibrant and colorful UI/UX
st.markdown(
   """
   <style>
   .main {
       background: linear-gradient(to right, #FF8C00, #FF6347); /* Orange to Tomato gradient */
       color: white;
       padding: 30px;
   }
   .stTextInput, .stButton button {
       background-color: #FFB6C1; /* Soft Pink */
       color: white;
   }
   .stTextInput input, .stTextArea textarea {
       background-color: #FFFFFF;
       color: #333;
   }
   .stButton button:hover {
       background-color: #FF69B4; /* Hot Pink */
   }
   .sidebar .sidebar-content {
       background-color: #2C3E50; /* Dark Blue-Grey */
       color: white;
       padding: 20px;
   }
   .sidebar .sidebar-title {
       color: #FFB6C1; /* Soft Pink */
   }
   h1, h2, h3 {
       font-family: 'Arial', sans-serif;
       color: #34495e; /* Darker text for headers */
   }
   .stMarkdown {
       color: #333;
   }
   .stTextInput, .stButton {
       border-radius: 8px;
   }
   .stTextArea textarea {
       border-radius: 8px;
   }
   .stFileUploader input {
       background-color: #f0f0f0;
       color: #333;
   }
   .stFileUploader button {
       background-color: #FFB6C1;
   }
   </style>
   """,
   unsafe_allow_html=True
)


# Sidebar for project introduction and group details
st.sidebar.title("AI/ML Class Project by CLUTAE: Sentiment Analysis on Product Reviews")
st.sidebar.write(
   """
   This application uses Natural Language Processing (NLP) to analyze the sentiment of customer reviews.
   The sentiment is classified as Positive, Neutral, or Negative.
   We provide two options for users:
   1. **Upload a CSV file** - Analyze sentiment for multiple reviews from your product's CSV file.
   2. **Fetch real-time reviews** - Get live reviews from a product page and analyze them.


   **Group Members:**
   - Utibe OwoAbasi Obot (ID: FE/23/62017159)
   - Clement Nduonyi (ID: FE/23/15378565)
   - Aniekan Ananga (ID: FE/23/34048660)
   - Emmanuel Thompson (ID: FE/23/75959998)
   """
)




# Remove the footnote on the main bar
# Function to analyze sentiment
def analyze_sentiment(text):
   blob = TextBlob(text)
   sentiment_score = blob.sentiment.polarity
   if sentiment_score > 0:
       return "Positive 😊", sentiment_score, "#27ae60"  # Green for positive
   elif sentiment_score < 0:
       return "Negative 😞", sentiment_score, "#e74c3c"  # Red for negative
   else:
       return "Neutral 😐", sentiment_score, "#bdc3c7"  # Gray for neutral




# Main content area
st.title("Sentiment Analysis for Customer Reviews")
option = st.selectbox("Choose an option", ["Upload CSV File", "Check Live Real-time Reviews"])


# Option 1: Upload CSV File
if option == "Upload CSV File":
   st.subheader("Upload CSV for Product Reviews")


   uploaded_file = st.file_uploader("Choose a CSV file", type="csv")


   if uploaded_file is not None:
       df = pd.read_csv(uploaded_file)
       if 'review_text' in df.columns:  # Check if the file has 'review_text' column
           st.write("### Analyzing Reviews:")
           sentiment_results = []


           for review in df['review_text']:
               sentiment, sentiment_score, color = analyze_sentiment(review)
               sentiment_results.append([review, sentiment, sentiment_score])


           sentiment_df = pd.DataFrame(sentiment_results, columns=["Review", "Sentiment", "Sentiment Score"])
           st.write(sentiment_df)


           # Pie chart for sentiment distribution
           sentiment_counts = sentiment_df['Sentiment'].value_counts()
           fig = px.pie(names=sentiment_counts.index, values=sentiment_counts.values, title="Sentiment Distribution")
           fig.update_traces(textinfo="percent+label", pull=[0.1, 0.1, 0.1])  # Add pull effect for engagement
           fig.update_layout(
               plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
               paper_bgcolor='#F0F4F8',
               title_font=dict(family="Arial", size=24, color='#2E3B4E'),
               margin=dict(t=50, b=50)
           )
           st.plotly_chart(fig)


           # Save sentiment analysis results to new CSV
           output_csv = sentiment_df.to_csv(index=False)
           st.download_button(label="Download Sentiment Analysis Results", data=output_csv,
                              file_name="sentiment_analysis_results.csv", mime="text/csv")
       else:
           st.error("The uploaded CSV file doesn't contain 'review_text' column.")


# Option 2: Check Live Real-time Reviews
elif option == "Check Live Real-time Reviews":
   st.subheader("Check Live Real-time Reviews for Product")


   product_url = st.text_input("Enter product URL (e.g., AliExpress, Amazon, etc.)")


   if product_url:
       # For demo purposes, let's fetch reviews from AliExpress (adjust as needed)
       try:
           headers = {'User-Agent': 'Mozilla/5.0'}
           response = requests.get(product_url, headers=headers)
           soup = BeautifulSoup(response.text, 'html.parser')


           # This is just an example, you would need to inspect the HTML structure for your actual case
           reviews = soup.find_all('div', class_='feedback-item')
           review_texts = [review.find('div', class_='feedback-text').get_text(strip=True) for review in reviews]


           if review_texts:
               sentiment_results = []


               for review in review_texts:
                   sentiment, sentiment_score, color = analyze_sentiment(review)
                   sentiment_results.append([review, sentiment, sentiment_score])


               sentiment_df = pd.DataFrame(sentiment_results, columns=["Review", "Sentiment", "Sentiment Score"])
               st.write(sentiment_df)


               # Pie chart for sentiment distribution
               sentiment_counts = sentiment_df['Sentiment'].value_counts()
               fig = px.pie(names=sentiment_counts.index, values=sentiment_counts.values,
                            title="Sentiment Distribution")
               fig.update_traces(textinfo="percent+label", pull=[0.1, 0.1, 0.1])  # Add pull effect for engagement
               fig.update_layout(
                   plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
                   paper_bgcolor='#F0F4F8',
                   title_font=dict(family="Arial", size=24, color='#2E3B4E'),
                   margin=dict(t=50, b=50)
               )
               st.plotly_chart(fig)
           else:
               st.warning("No reviews found on the page.")


       except Exception as e:
           st.error(f"An error occurred: {e}")

