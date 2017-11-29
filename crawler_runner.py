import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lol_pb_analyzer.settings')
django.setup()

from pb_analyzer.crawler import Crawler
from pb_analyzer.analyzer import Analyzer

# ororog: 200482207

def main():
  crawler = Crawler()
  analyzer = Analyzer()
  game_ids = crawler.crawl_match_by_id(200482207, end_index=50)
  for game_id in game_ids:
    analyzer.analyze_match_by_game_id(game_id)

if __name__ == '__main__':
  main()
