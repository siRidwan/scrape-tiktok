#!/usr/bin/env python3
"""
Contoh penggunaan TikTok Scraper
"""

from scraper import TikTokScraper

def example_basic():
    """Contoh penggunaan dasar"""
    scraper = TikTokScraper()
    
    # Scrape dengan keyword
    keyword = "BPC-157"
    max_results = 20
    
    print(f"Mencari video dengan keyword: {keyword}")
    videos = scraper.scrape(keyword, max_results=max_results)
    
    if videos:
        # Export ke CSV
        filename = scraper.export_to_csv(videos, "tiktok_results.csv")
        print(f"\nHasil disimpan di: {filename}")
        
        # Tampilkan ringkasan
        print(f"\nRingkasan:")
        print(f"- Total video: {len(videos)}")
        print(f"- Total views: {sum(v.get('Views', 0) for v in videos):,}")
        print(f"- Total likes: {sum(v.get('Likes', 0) for v in videos):,}")
    else:
        print("Tidak ada video ditemukan")

if __name__ == "__main__":
    example_basic()

