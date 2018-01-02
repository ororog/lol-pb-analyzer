from django.conf import settings
from riotwatcher import RiotWatcher

class Watcher:
  _watcher = None
  _apikey = settings.RGAPI

  def __new__(cls):
    if cls._watcher is None:
      cls._watcher = RiotWatcher(cls._apikey)
    return cls._watcher
