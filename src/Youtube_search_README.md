# Google Colab Youtube_search_based_on_Playlist

The Google Colab notebook contains 3 functions,`fetch_playlist(playlist_id)`, `data_retrieval()` and `retrieve_all_data()`, written for retrieving YouTube videos and shorts based on specific criteria. 

## Function: `fetch_playlist(playlist_id)`

This function fetches all videos from a specified YouTube playlist using the YouTube Data API. It retrieves video details, including the video ID, title, and channel.

### Usage Example:

```python
# Define playlist ID in the dictionary
playlist = {
    "NBC News": "PL0tDb4jw6kPwbfkRqaiNFdr0d_rl9vAXP",
    "CNN": "PL6XRrncXkMaU55GiCvv416NR2qBD_xbmf",
    "Fox News": "PLlTLHnxSVuIyMU4Q4I8NsLAVK1iNANGW9",
    "CBC News": "PLeyJPHbRnGaY2w91OBmfTL-d-a6MrO0gT"
}
df = build_csv(playlist)
```
The csv will be stored in 'Israel_Palestine_Conflict_videos.csv' and dataframe stored in df.

## Function: `data_retrieval(topic, API_KEY, channels, rows, search_type)`

This function scrapes YouTube videos and shorts based on the given `topic`. It filters videos from specified `channels` and ensures that the retrieved data matches the desired `search_type`. The function retrieves a maximum of `rows` videos/shorts.

### Parameters:

- `topic`: The topic/hashtag list to search for on YouTube.
- `API_KEY`: YouTube v3 API key.
- `channels`: A list of selected YouTube channels to filter the search results.
- `rows`: The total number of videos/shorts to retrieve.
- `search_type`: Specify either 'video' or 'short' to filter the search results accordingly.

### Output:

The function returns a DataFrame & save it as a csv with the following columns:
- `Channel`: The YouTube channel from which the video/short was retrieved.
- `Title`: The title of the video/short.
- `Video ID`: The unique ID of YouTube video/shorts.

## Function: `retrieve_all_data(topic, API_KEY, rows, search_type)`

This function retrieves all videos and shorts related to the given `topic` from the specified `channels`, using the provided `API_KEY`. 

### Parameters:

- `topic`: The topic/hashtag list to search for on YouTube.
- `API_KEY`: YouTube v3 API key.
- `rows`: The total number of videos/shorts to retrieve.
- `search_type`: Specify either 'video' or 'short' to filter the search results accordingly.

### Output:

The function returns a DataFrame & save it as a csv with the following columns:
- `Channel`: The YouTube channel from which the video/short was retrieved.
- `Title`: The title of the video/short.
- `Video ID`: The unique ID of the YouTube video/short.
- `Duration`: The duration of the video/short in seconds.
