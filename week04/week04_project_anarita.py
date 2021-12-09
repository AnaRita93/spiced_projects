"""
Week 04 Project:Text Classification

Goal: the program should run a model that predicts the artist based on a lyric 
Steps:
1.the program scraps lyrics from the internet and stores it in a file within a directory
2.the lyrics in each file are extracted and stored into a data frame. 
3.The data is cleaned up and split into train and validation sets
4.the data is vectorized using Bag of Words method
5.a logistic model is run over the training data and the scores are calculated 
6.predictions, scores and probabilities are calculated using a lyric from test data into the model and results between data sets are compared

"""
import requests
import re
import time
from bs4 import BeautifulSoup
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from nltk.tokenize import TreebankWordTokenizer
from nltk.stem import WordNetLemmatizer
import nltk   # only done once! we have to download the WordNet database locally
nltk.download("wordnet")
nltk.download('stopwords')
from nltk.corpus import stopwords


# Step1. Download a HTML page with links to songs. Extract hyperlinks of song pages
#Set a user agent:
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"}
timer = 1 #second

######Get Artists main web page 
florence = 'https://www.azlyrics.com/f/florencethemachine.html'
pearljam = 'https://www.azlyrics.com/p/pearljam.html'

######Create a directory for the artists 
florence_dir = '/home/rita/Documents/spiced/spiced-projects/convex_capers_student_code/week04/data/FlorenceAndTheMachine/'
pearljam_dir = '/home/rita/Documents/spiced/spiced-projects/convex_capers_student_code/week04/data/PearlJam/'

#####Store lyric files in the artists directories 
def get_lyric_files (artist_url):
    artist_response = requests.get(artist_url, headers=headers)
    all_artist_links = re.findall('\/lyrics\/florencethemachine\/.*html', artist_response.text)

    for url_suffix in all_artist_links:
        time.sleep(5) # sleeps for 5s to not get blocked
        song_html = requests.get('https://www.azlyrics.com' + url_suffix)
        text = song_html.text #grabs the html (including lyrics)
        file_name = url_suffix.split('/')[-1]
        with open(f'{file_name}.txt','w') as f: #and saves to disk
            f.write(text)
#        
get_lyrics_file(florence)
get_lyrics_file(pearljam)


# Step 2. Extract the lyrics from the files into a dataframe. Prepare the data for vectorization
def extract_lyrics (artists_dir): 
    artist = []
    song = []
    lyrics = []

    for fn in os.listdir(artist_dir):
        ly = open(artist_dir + fn).read()
        ly_soup = BeautifulSoup(ly, features="html.parser").text
        ly = re.findall('\\n...*',ly_soup)
        ly = [i.split('\n')[1] for i in ly]
        artist.append(ly[3])
        song.append(ly[4])
        lyrics.append(ly[3:ly.index(' Submit Corrections')])    
        
    all_lyrics_df = pd.DataFrame(lyrics)
#
extract_lyrics(florence_dir)
extract_lyrics(pearljam_dir)


#Put all things together and tidy the data 
def cleaning_df (all_lyrics_df): 
    all_lyrics_df.rename(columns={0:'Artist', 1:'Song_Title'}, inplace=True)

    tidy_lyrics = pd.melt(all_lyrics_df,                        # <==== untidy/wide dataframe
                        id_vars=['Artist','Song_Title'],           # <==== columns from the untidy/wide dataframe we want unchanged
                        var_name='previous_column'  ,           # <==== new column name for the variable column
                        value_name='lyrics' # <==== new column name for the value column
                        )

    tidy_lyrics = tidy_lyrics.dropna()
#
cleaning_df(all_lyrics_df)

#Train-Validation split data 
lyrics_train, lyrics_test = train_test_split(tidy_lyrics, test_size=0.2, random_state=42)

# Step 3. Vectorize the text using Bag of Words method

#Pre-processing, Tokenation and Lemmatization 

def pre_processing_data(df): 
    CORPUS = df['lyrics']
    CORPUS = [s.lower() for s in CORPUS] 
    
    CLEAN_CORPUS = []
    tokenizer = TreebankWordTokenizer()
    lemmatizer = WordNetLemmatizer()

    for doc in CORPUS:
        tokens = tokenizer.tokenize(text=doc)
        clean_doc = " ".join(lemmatizer.lemmatize(token) for token in tokens)
        CLEAN_CORPUS.append(clean_doc)

    LABELS_artist = df['Artist']
    
pre_processing_data(lyrics_train)
pre_processing_data(lyrics_test)

#Get stop words 
STOPWORDS = stopwords.words('english')

#Vectorize text 
vectorizer = CountVectorizer(stop_words=STOPWORDS)
vectors = vectorizer.fit_transform(CLEAN_CORPUS)
pd.DataFrame(vectors.todense(), columns=vectorizer.get_feature_names(), index=LABELS_artist).head()

#Normalize Data 
vectorizer = TfidfVectorizer(stop_words=STOPWORDS)
X = vectorizer.fit_transform(CLEAN_CORPUS)
