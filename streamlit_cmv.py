from bs4 import BeautifulSoup
import requests
import streamlit as st
import re
import spacy
import praw

# create reddit API
CLIENT_ID = 'UKVJpINrwNK3QtABQbS2eg'
SECRET_KEY = 'sOwDVEQ_KiGVDDb0l1kn-NELBMFQ7A'

auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

data = {
    'grant_type': 'password',
    'username': 'Mysterious-Slide-278',
    'password': 'K&Jr(D.$he94BTr'
}

headers = {'User-Agent': 'MyAPI/0.0.1'}

res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)


TOKEN = res.json()['access_token']

headers['Authorization'] = f'bearer {TOKEN}'

# create program

st.title('Reddit Comment viewer')
st.header('This app takes in a Reddit post URL and outputs the comments in a easy to view manner')

# take url from user input

url = st.text_input("To get started enter the Reddit URL below")

def get_reddit_comments(url):
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=SECRET_KEY,
        user_agent='streamlit by u/Mysterious-Slide-278'
    )

    submission = reddit.submission(url=url)
    submission.comments.replace_more(limit=None)
    
    return submission

def get_snippet(comment_body, length=50):
    return (comment_body[:length] + '...') if len(comment_body) > length else comment_body


# Recursive function to display comments and their replies
def display_comments(comment_dict, parent_id, level=0):
    if parent_id in comment_dict:
        for comment_id, (comment_body, replies) in comment_dict[parent_id].items():
            snippet = get_snippet(comment_body)
            st.markdown(f"{'&nbsp;' * 4 * level}**User:** {comment_id} - {snippet}")
            st.markdown(f"{'&nbsp;' * 4 * level}Comment: {comment_body}")
            display_comments(comment_dict, comment_id, level + 1)

# Comment tree using dictionary
comment_dict = {}

# Placeholder URL (replace with actual URL input handling)

if url:
    submission = get_reddit_comments(url)
    
    if submission:
        st.write('### Comments:')
        # Build the comment dictionary
        for comment in submission.comments.list():
            comment_id = comment.id
            comment_body = comment.body
            comment_author = comment.author
            parent_id = str(comment.parent()) if comment.parent() != submission.id else "root"
            
            if parent_id not in comment_dict:
                comment_dict[parent_id] = {}
            
            comment_dict[parent_id][comment_id] = (comment_body, {})
        
        # Display the comments
        display_comments(comment_dict, "root")
    else:
        st.write('No comments found or invalid URL.')
