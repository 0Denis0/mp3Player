from youtube_search import YoutubeSearch

searchTerms = 'Closer by Big Baby Tape, Aarne lyrics'
results = YoutubeSearch(search_terms=searchTerms, max_results=1).to_dict()[0]['id']

ytPrefix = 'https://www.youtube.com/watch?v='

link = f'{ytPrefix}{results}'
print(link)