import pandas as pd
import numpy as np 
import streamlit as st
import requests
data = pd.read_csv("Goodreads 2023 Data.csv")

st.title("2023 Goodreads Reading Challenge")

st.divider()

with st.container():
    
    st.markdown("<h2 style='text-align: center;'>Overall Stats</h2>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: grey'>Total Pages Read : 5702</h5>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: grey'>Total Book Read : 18</h5>", unsafe_allow_html=True)
    
st.divider()

with st.expander("All Data"):
    st.write(data)

st.divider()

st.subheader("Books Read Each Month")
monthly_counts = data['Month Read'].value_counts().sort_index()

st.bar_chart(monthly_counts)

st.divider()
st.header("Select The Book for specific details")
selected_book = st.selectbox('Select a book:', data['title'])

selected_book_info = data[data['title'] == selected_book].squeeze()

# Display book details
st.subheader(f'{selected_book}')
st.write(f"**Author:** {selected_book_info['author']}")
st.write(f"**Goodreads Rating:** {selected_book_info['avg goodreads rating']}")
st.write(f"**My Rating:** {selected_book_info['my rating']}")

google_books_api_url = 'https://www.googleapis.com/books/v1/volumes'
params = {'q': f'intitle:{selected_book}'}
response = requests.get(google_books_api_url, params=params)

if response.ok:
    book_data = response.json()
    if 'items' in book_data:
        first_book = book_data['items'][0]['volumeInfo']
        image_url = first_book['imageLinks']['thumbnail'] if 'imageLinks' in first_book else None
        st.image(image_url, caption=f"Cover of {selected_book}", use_column_width=False, width=200)

    else:
        st.warning(f"No information found for {selected_book}")
else:
    st.error(f"Failed to fetch data from Google Books API. Status code: {response.status_code}")
