# TikTok Scraper

A Python scraper to extract TikTok video data from search results and export them to CSV format.

## Features

- 🔍 Search TikTok videos by keyword
- 📊 Extract comprehensive video metadata (stats, author info, music, hashtags)
- 📄 Export to CSV with UTF-8 encoding
- 🔄 Automatic pagination support
- 🍪 Optional cookie support for better access
- ⏱️ Built-in rate limiting

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
python scraper.py [keyword] [max_results]
```

### Examples
```bash
# Scrape with default keyword "BPC-157" and 50 results
python scraper.py

# Scrape with custom keyword
python scraper.py "fitness"

# Scrape with custom keyword and result count
python scraper.py "fitness" 100
```

### Using the Scraper Class
```python
from scraper import TikTokScraper

scraper = TikTokScraper()
videos = scraper.scrape("keyword", max_results=50)
scraper.export_to_csv(videos, "output.csv")
```

## Output

The script generates a CSV file named `tiktok_scrape_YYYYMMDD_HHMMSS.csv` containing:

- **Video Information**: ID, Description, Create Time, Video URL, Play URL, Download URL, Cover Image
- **Video Properties**: Duration, Width, Height, Video Quality, Format
- **Author Information**: ID, Username, Nickname, Verified Status, Followers, Following, Videos Count, Hearts
- **Statistics**: Likes, Shares, Comments, Views, Collects
- **Music Information**: ID, Title, Author, Original Status
- **Metadata**: Hashtags, Challenge Count, Original Item, Text Language

## API Response Example

The scraper uses TikTok's Web API. Here's an example of the API response structure:

```json
{
    "status_code": 0,
    "data": [
        {
            "type": 1,
            "item": {
                "id": "7525518078759800077",
                "desc": "What's your experience with BPC-157? #bpc157peptides #joerogan",
                "createTime": 1752171233,
                "video": {
                    "id": "7525518078759800077",
                    "height": 1024,
                    "width": 576,
                    "duration": 94,
                    "ratio": "540p",
                    "cover": "https://p19-sign.tiktokcdn-us.com/...",
                    "playAddr": "https://v16-webapp-prime.tiktok.com/video/...",
                    "bitrate": 509414,
                    "format": "mp4",
                    "videoQuality": "normal"
                },
                "author": {
                    "id": "7128007246440858670",
                    "uniqueId": "growthovereverything",
                    "nickname": "Growth Over Everything",
                    "verified": false,
                    "followerCount": 2418,
                    "followingCount": 19,
                    "videoCount": 151,
                    "heartCount": 41700
                },
                "stats": {
                    "diggCount": 57,
                    "shareCount": 79,
                    "commentCount": 1,
                    "playCount": 4606,
                    "collectCount": 19
                },
                "music": {
                    "id": "7031101555747080194",
                    "title": "Storytelling",
                    "authorName": "Adriel",
                    "original": false
                },
                "textExtra": [
                    {
                        "hashtagName": "bpc157peptides",
                        "hashtagId": "7341124986960085034",
                        "type": 1
                    }
                ],
                "challenges": [
                    {
                        "id": "7341124986960085034",
                        "title": "bpc157peptides"
                    }
                ],
                "textLanguage": "en"
            }
        }
    ]
}
```

## CSV Output Example

The exported CSV file contains flattened data from the API response:

```csv
Video ID,Description,Create Time,Video URL,Play URL,Download URL,Cover Image,Duration (seconds),Width,Height,Video Quality,Format,Author ID,Author Username,Author Nickname,Author Verified,Author Followers,Author Following,Author Videos,Author Hearts,Likes,Shares,Comments,Views,Collects,Music ID,Music Title,Music Author,Music Original,Hashtags,Challenge Count,Original Item,Text Language
7525518078759800077,"What's your experience with BPC-157? #bpc157peptides #joerogan",2025-07-11 01:13:53,https://www.tiktok.com/@growthovereverything/video/7525518078759800077,https://v16-webapp-prime.tiktok.com/video/...,...,https://p19-sign.tiktokcdn-us.com/...,94,576,1024,normal,mp4,7128007246440858670,growthovereverything,Growth Over Everything,False,2418,19,151,41700,57,79,1,4606,19,7031101555747080194,Storytelling,Adriel,False,"bpc157peptides, joerogan, growthovereverything, growth, personalgrowth",5,False,en
```

## Pagination

The scraper automatically handles pagination:
- **First page**: `offset=0`, `focus_state=false`
- **Next pages**: `offset` increments by 16, `focus_state=true`
- Continues until `max_results` is reached or no more data is available

## Configuration

### Rate Limiting
Default delay between requests is 1 second. You can modify it in the `scrape()` method:

```python
videos = scraper.scrape(keyword, max_results=50, delay=2)  # 2 seconds delay
```

### Cookies
The scraper can automatically load cookies from `docs/damn.md` file. Cookies help with:
- Better access to TikTok API
- Reduced rate limiting
- Access to more results

To use cookies, place them in `docs/damn.md`:
```
cookie
your_cookie_string_here
```

## Notes

- The script uses TikTok's Web API (not official API)
- Rate limiting: 1 second delay between requests (configurable)
- Cookies are optional but recommended for better access
- Results are exported to CSV with UTF-8 encoding (compatible with Excel)
- The API may change without notice - the scraper may need updates

## Troubleshooting

### Common Issues

1. **No results returned**
   - Check your internet connection
   - TikTok may be blocking requests - try adding cookies
   - The keyword might not have any results

2. **Rate limiting errors**
   - Increase the delay between requests
   - Add cookies for better access
   - Reduce `max_results` per run

3. **Import errors**
   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version (3.7+ required)

4. **CSV encoding issues**
   - The CSV uses UTF-8 encoding with BOM (`utf-8-sig`)
   - Should open correctly in Excel, Google Sheets, and most text editors

## License

This project is for educational purposes only. Please respect TikTok's Terms of Service and use responsibly.
