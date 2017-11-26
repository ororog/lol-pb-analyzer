from pb_analyzer.models import *

class Analyzer:
  def analyze_match(self, match):
    results = {}
    for participant_identity in match.participantidentity_set.all():
      player = participant_identity.player
      summoner = Summoner.objects.filter(account_id=player.account_id).first()
      if not summoner:
        summoner = Summoner.objects.create(
          name=player.summoner_name,
          account_id=player.account_id,
        )
      results[participant_identity.participant_id] = {
        'match': match,
        'summoner': summoner,
      }

    for participant in match.participant_set.all():
      id = participant.participant_id
      stats = participant.participantstats
      timeline = participant.participanttimeline
      results[id]['stats'] = stats
      results[id]['timeline'] = timeline
      results[id]['participant'] = participant

    for result in results.values():
      match_result = SummonerMatchResult.objects.filter(
          match=result['match'], summoner=result['summoner']
      ).first()
      if not match_result:
        SummonerMatchResult.objects.create(
          match=result['match'],
          summoner=result['summoner'],
          timeline=result['timeline'],
          stats=result['stats'],
          participant=result['participant'],
        )
