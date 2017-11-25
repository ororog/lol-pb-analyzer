from django.db import models

# Create your models here.

class Match(models.Model):
  def __str__(self):
    return 'Match (game_id: {})'.format(self.gameId)
  seasonId = models.IntegerField()
  queueId = models.IntegerField()
  gameId = models.IntegerField()
  gameVersion = models.CharField(max_length=20)
  platformId = models.CharField(max_length=20)
  gameMode = models.CharField(max_length=20)
  mapId = models.IntegerField()
  gameType = models.CharField(max_length=20)
  gameDuration = models.IntegerField()
  gameCreation = models.IntegerField()

class ParticipantIdentity(models.Model):
  def __str__(self):
    return 'ParticipantIdentity (game_id: {}, participant_id: {})'.format(
      self.match.gameId, self.participantId
    )
  match = models.ForeignKey(Match)
  participantId = models.IntegerField()

class Player(models.Model):
  def __str__(self):
    return 'Player (name: {}, account_id: {})'.format(
      self.summonerName, self.accountId
    )
  participantIdentity = models.ForeignKey(ParticipantIdentity)
  currentPlatformId = models.CharField(max_length=20)
  summonerName = models.CharField(max_length=100)
  matchHistoryUri = models.CharField(max_length=100)
  platformId = models.CharField(max_length=20)
  currentAccountId = models.IntegerField()
  profileIcon = models.IntegerField()
  summonerId = models.IntegerField()
  accountId = models.IntegerField()

class Participant(models.Model):
  def __str__(self):
    return 'Participant (game_id: {}, participant_id: {})'.format(
      self.match.gameId, self.participantId
    )
  match = models.ForeignKey(Match)
  participantId	= models.IntegerField()
  teamId = models.IntegerField()
  championId = models.IntegerField()

class ParticipantStats(models.Model):
  def __str__(self):
    return 'ParticipantStats (participant_id: {}, win: {}'.format(
      self.participant.participantId, self.win
    )
  participant = models.ForeignKey(Participant)
  win = models.BooleanField()

class ParticipantTimeline(models.Model):
  def __str__(self):
    return 'ParticipantTimeline (participant_id: {}, lane: {}, role: {})'.format(
      self.participantId, self.lane, self.role
    )
  participant = models.ForeignKey(Participant)
  participantId = models.IntegerField()
  lane = models.CharField(max_length=20)
  role = models.CharField(max_length=20)
