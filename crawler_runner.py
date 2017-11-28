import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lol_pb_analyzer.settings')
django.setup()

from pb_analyzer.crawler import Crawler

# ororog: 200482207

def main():
  crawler = Crawler()
  champions = crawler.crawl_champions()
  champions_by_id = {}
  for name, data in  champions['data'].items():
    champions_by_id[data['id']] = data['name']
  for id in sorted(champions_by_id.keys()):
    print("{}: '{}',".format(id, champions_by_id[id]))
if __name__ == '__main__':
  main()
