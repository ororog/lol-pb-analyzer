import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lol.settings')
django.setup()

from pb_analyzer.analyzer import Analyzer
from pb_analyzer.models import Match

def main():
  analyzer = Analyzer()
  analyzer.analyze_match(Match.objects.all().first())

if __name__ == '__main__':
  main()
