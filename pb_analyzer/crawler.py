import os
import time
import datetime
import re
import requests
import pytz

from pb_analyzer.models import *
from pb_analyzer.watcher import Watcher
from pb_analyzer.analyzer import Analyzer
from django.db import transaction

class Crawler:
  def __init__(self):
    self.__watcher = Watcher()

  def crawl_summoner_by_name(self, summoner_name, region='jp1'):
    if not Summoner.objects.filter(name=summoner_name).first():
      try:
        summoner_json = self.__watcher.summoner.by_name(region, summoner_name)
        account_id = int(summoner_json['accountId'])
        summoner = Summoner.objects.filter(account_id=account_id).first()
        if not summoner:
          return Summoner.objects.create(
            name=summoner_json['name'],
            account_id=summoner_json['accountId'],
            summoner_level=summoner_json['summonerLevel'],
          )
        else:
          summoner.summoner_name = summoner_json['name']
          summoner.summoner_level=summoner_json['summonerLevel']
          summoner.save()
          return summoner
      except requests.exceptions.HTTPError:
        return None

  def update_summoner_by_id(self, account_id, region='jp1'):
    summoner = Summoner.objects.filter(account_id=account_id).first()
    now = datetime.datetime.now(datetime.timezone.utc)
    if not summoner.is_update_enabled():
      return
    JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
    now = datetime.datetime.now(JST)
    summoner.updated_at = now
    summoner_json = self.__watcher.summoner.by_account(region, account_id)
    summoner_id = summoner_json['id']
    summoner_leagues_json = self.__watcher.league.positions_by_summoner(region, summoner_id)
    summoner.summoner_level = summoner_json['summonerLevel']
    league_json = [x for x in summoner_leagues_json if x['queueType'] == 'RANKED_SOLO_5x5']
    if len(league_json) > 0:
      summoner.tier = league_json[0]['tier']
      summoner.rank = league_json[0]['rank']
    else:
      summoner.tier = ''
      summoner.rank = ''
    summoner.save()

  def crawl_champions(self, region='jp1', locale='ja_JP'):
    return self.__watcher.static_data.champions(region, locale=locale)

  def list_gameids_by_account_id(self,
                                 account_id,
                                 region='jp1',
                                 season=[7, 8, 9, 10, 11],
                                 queue=[400, 420, 430, 440],
                                 begin_index=0,
                                 end_index=3):
    matchlist = self.__watcher.match.matchlist_by_account(
      region, account_id, begin_index=begin_index, end_index=end_index,
      season=season, queue=queue)
    return [match_ref['gameId'] for match_ref in matchlist['matches']]

  def crawl_match_by_id(self,
                        account_id,
                        region='jp1',
                        begin_index=0,
                        end_index=3):
    matchlist = self.__watcher.match.matchlist_by_account(
      region, account_id, begin_index=begin_index, end_index=end_index)

    for match_ref in matchlist['matches']:
      game_id = match_ref['gameId']
      self.crawl_match_by_game_id(game_id)
      time.sleep(2)
    return [match_ref['gameId'] for match_ref in matchlist['matches']]

  def crawl_match_by_game_id(self, game_id, region='jp1'):
    m = Match.objects.filter(game_id=game_id).first()
    if m:
      return m
    with transaction.atomic():
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

  def __create_args_from_json(self, json, keys, base_args={}):
    return {
      **base_args,
      **{self.__to_snake(k): json[k] for k in keys}
    }

  def __to_snake(self, camel_case):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_case)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
