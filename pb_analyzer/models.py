import datetime
import pytz
from django.db import models

class Summoner(models.Model):
  def __str__(self):
    return 'Summoner (name: {}, account_id: {})'.format(
      self.name, self.account_id)
  name = models.CharField(max_length=100)
  account_id = models.BigIntegerField()
  summoner_level = models.BigIntegerField(null=True)
  updated_at = models.DateTimeField(blank=True, null=True)
  tier = models.CharField(null=True, max_length=20)
  rank = models.CharField(null=True, max_length=20)

  def is_update_enabled(self):
    JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
    now = datetime.datetime.now(JST)
    return (
      self.updated_at is None or
      now - datetime.timedelta(hours=1) > self.updated_at)

class Match(models.Model):
  def __str__(self):
    return 'Match (game_id: {})'.format(self.game_id)

  season_id = models.IntegerField()
  queue_id = models.IntegerField()
  game_id = models.BigIntegerField()
  game_version = models.CharField(max_length=20)
  platform_id = models.CharField(max_length=20)
  game_mode = models.CharField(max_length=20)
  map_id = models.IntegerField()
  game_type = models.CharField(max_length=20)
  game_duration = models.BigIntegerField()
  game_creation = models.BigIntegerField()

class ParticipantIdentity(models.Model):
  def __str__(self):
    return 'ParticipantIdentity (game_id: {}, participant_id: {})'.format(
      self.match.game_id, self.participant_id
    )

  match = models.ForeignKey(Match, models.CASCADE)
  participant_id = models.IntegerField()

class Player(models.Model):
  def __str__(self):
    return 'Player (name: {}, account_id: {})'.format(
      self.summoner_name, self.account_id
    )

  participant_identity = models.OneToOneField(ParticipantIdentity, models.CASCADE)
  current_platform_id = models.CharField(max_length=20)
  summoner_name = models.CharField(max_length=100)
  match_history_uri = models.CharField(max_length=100)
  platform_id = models.CharField(max_length=20)
  current_account_id = models.BigIntegerField()
  profile_icon = models.IntegerField()
  summoner_id = models.BigIntegerField()
  account_id = models.BigIntegerField()

class Participant(models.Model):
  def __str__(self):
    return 'Participant (game_id: {}, participant_id: {})'.format(
      self.match.game_id, self.participant_id
    )

  match = models.ForeignKey(Match, models.CASCADE)
  participant_id = models.IntegerField()
  team_id = models.IntegerField()
  champion_id = models.IntegerField()

class ParticipantStats(models.Model):
  def __str__(self):
    return 'ParticipantStats (participant_id: {}, win: {})'.format(
      self.participant.participant_id, self.win
    )

  participant = models.OneToOneField(Participant, models.CASCADE)
  win = models.BooleanField()

class ParticipantTimeline(models.Model):
  def __str__(self):
    return 'ParticipantTimeline (participant_id: {}, lane: {}, role: {})'.format(
      self.participant.participant_id, self.lane, self.role
    )

  participant = models.OneToOneField(Participant, models.CASCADE)
  lane = models.CharField(max_length=20)
  role = models.CharField(max_length=20)

class SummonerMatchResult(models.Model):
  def __str__(self):
    return 'SummonerMatchResult (summoner: {}, game_id: {})'.format(
      self.summoner.name, self.match.game_id
    )

  match = models.ForeignKey(Match, models.CASCADE)
  summoner = models.ForeignKey(Summoner, models.CASCADE)
  timeline = models.ForeignKey(ParticipantTimeline, models.CASCADE)
  stats = models.ForeignKey(ParticipantStats, models.CASCADE)
  participant = models.OneToOneField(Participant, models.CASCADE)
