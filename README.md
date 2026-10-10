# movie-recommender
HI !!   I made this movie recommender system , as currently i'm learning Ml and wanted to make some cool projcts.
so the idea is , suppose You liked a movie , say batman and you want to see more movies like that , of the same series , or of the same actoor/director , so you can just search and get the results . 

## features 
- the csv has 5000 movie data ! , so im sure your fav one is on the list
- posters integration: fetches movies poster from Movie database( TMDB)

## tech stack

python 
pandas
sciket-learn
NLTK
streamlit 

## RUN LOCALLY 

- Clone the repository
```
git clone https://github.com/nAItiklearn/movie-recommender.git
cd movie-recommender  
```

- Create a virtual environment

```
python -m venv .venv
```

-Activate it on Windows:
```
.venv\Scripts\Activate.ps1
```
- Install dependencies
```
pip install -r requirements.txt
```

- Configure the TMDB API key
```
Create .streamlit/secrets.toml and add your TMDB API key:
```
TMDB_API_KEY = ```"your_tmdb_api_key"```

Update``` app.py``` to read the key using ```st.secrets["TMDB_API_KEY"]```.

5. Start the application
```
streamlit run app.py
```
The application will open in your browser, usually at http://localhost:8501.

