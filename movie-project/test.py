import requests

# url = "https://api.themoviedb.org/3/search/movie"
# param = {
#     'api_key': "66f6975cdf45031ac423b530df397a61",
#     'query': "Spider-Man"
# }


movie_search = requests.get(f"https://api.themoviedb.org/3/movie/634649?api_key=66f6975cdf45031ac423b530df397a61")
data = movie_search.json()
# print(len(data["results"]))
# name = [data["results"][x]["original_title"] for x in range(len(data["results"]))]
# movie_id = [data["results"][y]["id"] for y in range(len(data["results"]))]
print(data)