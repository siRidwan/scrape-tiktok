#!/usr/bin/env python3
"""
TikTok Scraper - Scrapes TikTok search results and exports to CSV
"""

import requests
import pandas as pd
from urllib.parse import urlencode
from datetime import datetime
import time
import sys


class TikTokScraper:
    def __init__(self):
        self.base_url = "https://www.tiktok.com/api/search/general/full/"
        self.headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "id,en-US;q=0.9,en;q=0.8,zh-TW;q=0.7,zh;q=0.6",
            "dnt": "1",
            "priority": "u=1, i",
            "referer": "https://www.tiktok.com/search",
            "sec-ch-ua": '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
        }
        
    def build_search_url(self, keyword, offset=0, count=16, cookies=None):
        """Build search URL with parameters"""
        # focus_state is true if offset > 0, false if offset == 0
        focus_state = "true" if offset > 0 else "false"
        
        params = {
            "WebIdLastTime": str(int(time.time())),
            "aid": "1988",
            "app_language": "id-ID",
            "app_name": "tiktok_web",
            "browser_language": "id",
            "browser_name": "Mozilla",
            "browser_online": "true",
            "browser_platform": "MacIntel",
            "browser_version": "5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
            "channel": "tiktok_web",
            "cookie_enabled": "true",
            "count": str(count),
            "data_collection_enabled": "false",
            "device_id": "7540547403108861457",
            "device_platform": "web_pc",
            "device_type": "web_h265",
            "focus_state": focus_state,
            "from_page": "search",
            "history_len": "3",
            "is_fullscreen": "true",
            "is_page_visible": "true",
            "keyword": keyword,
            "odinId": "7540547149462799376",
            "offset": str(offset),
            "os": "mac",
            "priority_region": "",
            "referer": "",
            "region": "ID",
            "screen_height": "1050",
            "screen_width": "1680",
            "search_source": "normal_search",
            "tz_name": "Asia/Jakarta",
            "user_is_login": "false",
            "webcast_language": "id-ID"
        }
        
        # Add cookies to headers if provided
        if cookies:
            self.headers["cookie"] = cookies
            
        return self.base_url + "?" + urlencode(params)
    
    def search(self, keyword, offset=0, count=16, cookies=None):
        """Search TikTok videos"""
        url = self.build_search_url(keyword, offset, count, cookies)
        
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            return None
    
    def extract_video_data(self, item_data):
        """Extract relevant data from video item"""
        if not item_data or "item" not in item_data:
            return None
            
        item = item_data["item"]
        video = item.get("video", {})
        author = item.get("author", {})
        stats = item.get("stats", {})
        music = item.get("music", {})
        challenges = item.get("challenges", [])
        
        # Extract hashtags
        hashtags = []
        text_extra = item.get("textExtra", [])
        for extra in text_extra:
            if extra.get("type") == 1:  # Hashtag type
                hashtags.append(extra.get("hashtagName", ""))
        
        # Extract video URLs
        play_addr = video.get("playAddr", "")
        download_addr = video.get("downloadAddr", "")
        cover = video.get("cover", "")
        
        # Format create time
        create_time = item.get("createTime", 0)
        create_date = datetime.fromtimestamp(create_time).strftime("%Y-%m-%d %H:%M:%S") if create_time else ""
        
        return {
            "Video ID": item.get("id", ""),
            "Description": item.get("desc", ""),
            "Create Time": create_date,
            "Video URL": f"https://www.tiktok.com/@{(author.get('uniqueId', ''))}/video/{item.get('id', '')}",
            "Play URL": play_addr,
            "Download URL": download_addr,
            "Cover Image": cover,
            "Duration (seconds)": video.get("duration", 0),
            "Width": video.get("width", 0),
            "Height": video.get("height", 0),
            "Video Quality": video.get("videoQuality", ""),
            "Format": video.get("format", ""),
            "Author ID": author.get("id", ""),
            "Author Username": author.get("uniqueId", ""),
            "Author Nickname": author.get("nickname", ""),
            "Author Verified": author.get("verified", False),
            "Author Followers": author.get("followerCount", 0),
            "Author Following": author.get("followingCount", 0),
            "Author Videos": author.get("videoCount", 0),
            "Author Hearts": author.get("heartCount", 0),
            "Likes": stats.get("diggCount", 0),
            "Shares": stats.get("shareCount", 0),
            "Comments": stats.get("commentCount", 0),
            "Views": stats.get("playCount", 0),
            "Collects": stats.get("collectCount", 0),
            "Music ID": music.get("id", ""),
            "Music Title": music.get("title", ""),
            "Music Author": music.get("authorName", ""),
            "Music Original": music.get("original", False),
            "Hashtags": ", ".join(hashtags),
            "Challenge Count": len(challenges),
            "Original Item": item.get("originalItem", False),
            "Text Language": item.get("textLanguage", ""),
        }
    
    def scrape(self, keyword, max_results=50, cookies=None, delay=1):
        """Scrape multiple pages of results"""
        all_videos = []
        offset = 0
        count = 16  # TikTok typically returns 16 items per page
        
        print(f"Starting scrape for keyword: {keyword}")
        print(f"Target: {max_results} results")
        
        while len(all_videos) < max_results:
            print(f"Fetching offset {offset}...")
            
            data = self.search(keyword, offset=offset, count=count, cookies=cookies)
            
            if not data or data.get("status_code") != 0:
                print(f"Error: {data.get('status_code') if data else 'No response'}")
                break
            
            items = data.get("data", [])
            if not items:
                print("No more results found")
                break
            
            for item in items:
                if item.get("type") == 1:  # Video type
                    video_data = self.extract_video_data(item)
                    if video_data:
                        all_videos.append(video_data)
                        
                        if len(all_videos) >= max_results:
                            break
            
            if len(all_videos) >= max_results:
                break
                
            # Increment offset by 16 for next page
            offset += 16
            time.sleep(delay)  # Be respectful with rate limiting
        
        print(f"Scraped {len(all_videos)} videos")
        return all_videos
    
    def export_to_csv(self, videos, filename=None):
        """Export videos data to CSV"""
        if not videos:
            print("No videos to export")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tiktok_scrape_{timestamp}.csv"
        
        df = pd.DataFrame(videos)
        
        # Export to CSV with UTF-8 encoding
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print(f"Exported {len(videos)} videos to {filename}")
        return filename


def load_cookies_from_file(filepath="docs/damn.md"):
    """Load cookies from damn.md file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Find cookie line (line with 'cookie' header)
            for i, line in enumerate(lines):
                if line.strip().lower() == 'cookie':
                    # Get the next line which contains the cookie value
                    if i + 1 < len(lines):
                        cookie_line = lines[i + 1].strip()
                        if cookie_line:
                            return cookie_line
    except FileNotFoundError:
        print(f"Cookie file not found: {filepath}")
    except Exception as e:
        print(f"Error loading cookies: {e}")
    return None


def main():
    """Main function"""
    scraper = TikTokScraper()
    
    # Get keyword from command line or use default
    if len(sys.argv) > 1:
        keyword = sys.argv[1]
    else:
        keyword = "Best Peptides"
    
    # Get max results
    max_results = 50
    if len(sys.argv) > 2:
        try:
            max_results = int(sys.argv[2])
        except ValueError:
            print("Invalid max_results, using default: 50")
    
    # Try to load cookies from damn.md
    cookies = load_cookies_from_file()
    if cookies:
        print("Cookies loaded from damn.md")
    else:
        print("No cookies found, using default headers")
    
    # Scrape videos
    videos = scraper.scrape(keyword, max_results=max_results, cookies=cookies)
    
    # Export to CSV
    if videos:
        scraper.export_to_csv(videos)
    else:
        print("No videos found to export")


if __name__ == "__main__":
    main()

