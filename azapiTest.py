# Test

import azapi
from duckduckgo_search import DDGS

api = azapi.AZlyrics('duckduckgo')

api.artist = "Glass Animals"
api.title = "Agnes"

results = DDGS().text(f'{api.title} by {api.artist} lyrics site:azlyrics.com', max_results=1)[0]['href']

api.getLyrics(url=results, save=True, path='Lyrics/', sleep=5)







