import os
import time
import re
import requests
from pb_analyzer.models import *
from riotwatcher import RiotWatcher
from pb_analyzer.analyzer import Analyzer

# ororog: 200482207

class Crawler:
  def __init__(self, api_key=os.getenv('RGAPI')):
    self.__watcher = RiotWatcher(api_key)

  def crawl_summoner_by_name(self, summoner_name, region='jp1'):
    if not Summoner.objects.filter(name=summoner_name).first():
      try:
        summoner_json = self.__watcher.summoner.by_name(region, summoner_name)

        return Summoner.objects.create(
          name=summoner_json['name'],
          account_id=summoner_json['accountId'],
          summoner_level=summoner_json['summonerLevel'],
        )
      except requests.exceptions.HTTPError:
        return None

  def crawl_champions(self, region='jp1', locale='ja_JP'):
    return self.__watcher.static_data.champions(region, locale=locale)


  def crawl_match_by_id(self,
                        account_id,
                        region='jp1',
                        begin_index=0,
                        end_index=3):
    analyzer = Analyzer()
    matchlist = self.__watcher.match.matchlist_by_account(
      region, account_id, begin_index=begin_index, end_index=end_index)

    for match_ref in matchlist['matches']:
      game_id = match_ref['gameId']
      if not Match.objects.filter(game_id=game_id).first():
        match_json = self.__watcher.match.by_id(region, game_id)
        match = Match.objects.create(**{self.__to_snake(k): match_json[k] for k in (
          'seasonId', 'queueId', 'gameId', 'gameVersion',
          'platformId', 'gameMode', 'mapId', 'gameType',
          'gameDuration', 'gameCreation'
        )})

        participant_identities_json = match_json['participantIdentities']
        for participant_identity_json in participant_identities_json:
          participant_identity = ParticipantIdentity.objects.create(
            match=match,
            participant_id=participant_identity_json['participantId'],
          )

          player = Player.objects.create(**self.__create_args_from_json(
            participant_identity_json['player'],
            ('currentPlatformId', 'summonerName', 'matchHistoryUri', 'platformId',
             'currentAccountId', 'profileIcon', 'summonerId', 'accountId'),
            base_args={'participant_identity': participant_identity}))

        for participant_json in match_json['participants']:
          participant = Participant.objects.create(**self.__create_args_from_json(
            participant_json,
            ('participantId', 'teamId', 'championId'),
            base_args={'match': match},
          ))

          participant_stats_json = participant_json['stats']
          participants_stats = ParticipantStats.objects.create(
            participant=participant,
            win=participant_stats_json['win'],
          )

          participant_timeline_json = participant_json['timeline']
          participant_timeline = ParticipantTimeline.objects.create(
            participant=participant,
            lane=participant_timeline_json['lane'],
            role=participant_timeline_json['role'],
          )
        time.sleep(2)
    return [match_ref['gameId'] for match_ref in matchlist['matches']]

  def __create_args_from_json(self, json, keys, base_args={}):
    return {
      **base_args,
      **{self.__to_snake(k): json[k] for k in keys}
    }

  def __to_snake(self, camel_case):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_case)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
