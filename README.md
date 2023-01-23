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
> 
```
- Alix_et_Mika_Paris_Ile_de_France.csv: 26
- Bayleaf_Restaurant_London_England.csv: 195
- Bistrot_Instinct_Paris_Ile_de_France.csv: 96
- Bleecker_Street_Pizza_New_York_City.csv: 267
- Bonoo_Indian_Tapas_London_England.csv: 225
- Boucherie_Union_Square_New_York_City.csv: 225
- Boucherie_West_Village_New_York_City.csv: 227
- Cavale_Paris_Ile_de_France.csv: 7
- Club_A_Steakhouse_New_York_City.csv: 250
- David_Burke_Tavern_New_York_City.csv: 114
- Da_Andrea_Ristorante_New_York_City.csv: 225
- Da_Giuseppe_Paris_Ile_de_France.csv: 120
- Devine_Restaurant_Coffee_Bar_London_England.csv: 213
- Devran_London_England.csv: 225
- Frog_XVI_Paris_Ile_de_France.csv: 225
- Il_Etait_Un_Square_Paris_Ile_de_France.csv: 225
- Indian_Room_London_England.csv: 227
- Little_Alley_New_York_City.csv: 70
- Nell_Arte_Paris_Ile_de_France.csv: 4
- Nora_Cafe_London_England.csv: 225
- Olio_e_Piu_New_York_City.csv: 238
- Petite_Boucherie_New_York_City.csv: 227
- Piccola_Cucina_Estiatorio_New_York_City.csv: 219
- Pur_Jean_Francois_Rouquette_Paris_Ile_de_France.csv: 225
- Scarlett_Green_London_England.csv: 225
- Sheba_London_England.csv: 227
- STK_Steakhouse_Strand_London_England.csv: 225
- The_Consulate_New_York_City.csv: 221
- The_India_2_Best_of_the_City_London_England.csv: 127
- The_London_Cabaret_Club_England.csv: 225
- Verse_Toujours_Paris_Ile_de_France.csv: 70
- Zincou_Vins_Tapas_Paris_Ile_de_France.csv: 1
```

### analysis_img folder
> It collects the plots for each restaurant with the relative features analysis

### demo folder
> Here it is stored the demo of the website

### notebooks_ipynb folder
> The copies of the scripts.py in notebook.ipynb format
