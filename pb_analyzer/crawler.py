from django.conf import settings
from riotwatcher import RiotWatcher
from pb_analyzer.models import Match
import os

settings.configure(
  DEBUG=True,
  DATABASES={"default": {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": ":memory:"
  }},
  INSTALLED_APPS=[__name__]
)


RIOT_API_KEY = os.getenv('RGAPI')

# ororog: 200482207

def main():
  watcher = RiotWatcher(RIOT_API_KEY)
  region = 'jp1'
  matchlist = watcher.match.matchlist_by_account(
    region, 200482207, begin_index=0, end_index=3)

  for match_ref in matchlist['matches']:
    gameId = match_ref['gameId']
    match = watcher.match.by_id(region, gameId)
    print(match)

if __name__ == '__main__':
  main()
