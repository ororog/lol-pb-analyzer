import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lol_pb_analyzer.settings')
django.setup()

from pb_analyzer.crawler import Crawler

# ororog: 200482207

def main():
  crawler = Crawler()
  crawler.crawl_match_by_id(200482207)

if __name__ == '__main__':
  main()
