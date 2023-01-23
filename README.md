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
