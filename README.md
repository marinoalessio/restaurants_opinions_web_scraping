# Restaurants Opinions Web Scraping - Features Analysis through Social Networks

This project aims to scrape people's opinions through social networks, related to a specific topic: in our case, about restaurants.

### Which platforms to get people's opinions?

**Twitter** and **TripAdvisor**. 

This choice is because:
- Having a second source is great for having more accurate data
- Twitter may not have much data available, sometimes it can be infrequent to leave a thought on Twitter about a restaurant
- Not all tweets may be relevant or a restaurant name is not unique and there may be more than one with the same name

### Why Features?

We are interested in offering businesses a careful analysis of the advantages and disadvantages of their business, furthermore, to orient the clients' choice.
So seeing which features are the most satisfactory and which ones are less.

## Project Structure

### main.py
> It is the main function containing the gist of the project. It collects several functions found in other .py files. 
> The strength of having several files is the modular structure that serves to keep everything tidier. 
>> However, it was also decided to copy all the functions in a file so as to avoid dependencies through imports and make it clearer. 
> Anyways, it is possible to use each function in isolation via 
> `from file_name import function_name`

### tripadvisor_search.py
> It contains the function `get_top_from_query(query, max_elements=10)` that gets name and link of the most influential `n` restaurants

### twitter_scraper.py
> It contains the function `twitter_scraper(query, Stop_num, kw_start_point=0, start_date=None, end_date=None)` to get a `Stop_num` tweets from a `query` as a keyword.
> It returns a dataframe with date and tweet content

### tripadvisor_reviews_scraper.py
> The function `get_reviews_from_url(url)` retrieves all the TripAdvisor reviews from url. It returns a dataframe with title, date, rating and review content.

### get_analysis.py
> `clean_text(text, name)` removes all the useless and misleading elements.
> `get_sentiment(x)` gets the sentiment score from -1 (negative) to +1 (positive) given a text.
> `get_analysis_from_opinions(opinions, name)` plots the analysis on features (most common words)

### data folder
> It collects the opinion data relative to each restaurant for each city, as a "backup"
> Here is half of the files stored in the folder and their opinion count. It is important to have enough data to obtain more precise analyses.
```
Alix_et_Mika_Paris_Ile_de_France.csv: 26
Bayleaf_Restaurant_London_England.csv: 195
Bistrot_Instinct_Paris_Ile_de_France.csv: 96
Bleecker_Street_Pizza_New_York_City.csv: 267
Boucherie_West_Village_New_York_City.csv: 227
Club_A_Steakhouse_New_York_City.csv: 250
David_Burke_Tavern_New_York_City.csv: 114
Frog_XVI_Paris_Ile_de_France.csv: 225
Nora_Cafe_London_England.csv: 225
Olio_e_Piu_New_York_City.csv: 238
Petite_Boucherie_New_York_City.csv: 227
The_India_2_Best_of_the_City_London_England.csv: 127
The_London_Cabaret_Club_England.csv: 225
Verse_Toujours_Paris_Ile_de_France.csv: 70
```
### analysis_img folder
> It collects the plots for each restaurant with the relative features analysis

### demo folder
> Here it is stored the demo of the website

### notebooks_ipynb folder
> The copies of the scripts.py in notebook.ipynb format

## Code
```python
print(d)
```
