# TikTok Scraper

Scraper untuk mengambil data video TikTok dari hasil pencarian dan mengekspornya ke format CSV.

## Instalasi

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Penggunaan

### Basic Usage
```bash
python scraper.py [keyword] [max_results]
```

### Contoh
```bash
# Scrape dengan keyword default "BPC-157" dan 50 hasil
python scraper.py

# Scrape dengan keyword custom
python scraper.py "fitness"

# Scrape dengan keyword dan jumlah hasil custom
python scraper.py "fitness" 100
```

## Output

Script akan menghasilkan file CSV dengan nama `tiktok_scrape_YYYYMMDD_HHMMSS.csv` yang berisi:

- Video ID
- Description
- Create Time
- Video URL
- Play URL
- Download URL
- Cover Image
- Duration, Width, Height
- Author Information (Username, Nickname, Followers, etc.)
- Statistics (Likes, Shares, Comments, Views)
- Music Information
- Hashtags
- Dan lainnya

## Catatan

- Script menggunakan TikTok Web API
- Rate limiting: delay 1 detik antara request (dapat diubah di fungsi `scrape`)
- Cookies opsional: dapat ditambahkan untuk akses lebih baik
- Hasil akan otomatis di-export ke CSV dengan encoding UTF-8

## Troubleshooting

Jika mendapatkan error:
1. Pastikan semua dependencies terinstall
2. Cek koneksi internet
3. TikTok mungkin memblokir request - coba tambahkan cookies dari browser
4. Sesuaikan delay jika terlalu cepat

