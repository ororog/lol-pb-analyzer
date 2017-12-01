from pb_analyzer.models import *
from collections import defaultdict

class Analyzer:
  def analyze_match(self, match):
    results = {}
    for participant_identity in match.participantidentity_set.all():
      player = participant_identity.player
      summoner = Summoner.objects.filter(account_id=player.current_account_id).first()
      if not summoner:
        summoner = Summoner.objects.create(
          name=player.summoner_name,
          account_id=player.current_account_id,
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

  def analyze_match_by_game_id(self, game_id):
    match = Match.objects.filter(game_id=game_id).first()
    if match:
      return self.analyze_match(match)
    else:
      return None

  def analyze_summoner(self, summoner):
    match_results = SummonerMatchResult.objects.filter(summoner=summoner)
    result = {
      'champions': {},
      'lane': {
        'TOP': {'win': 0, 'lose': 0, 'games': 0, 'ratio': 0},
        'JUNGLE': {'win': 0, 'lose': 0, 'games': 0, 'ratio': 0},
        'MIDDLE': {'win': 0, 'lose': 0, 'games': 0, 'ratio': 0},
        'DUO_CARRY': {'win': 0, 'lose': 0, 'games': 0, 'ratio': 0},
        'DUO_SUPPORT': {'win': 0, 'lose': 0, 'games': 0, 'ratio': 0},
      },
      'champions_by_lane': {
        'TOP': {'champions': {}},
        'JUNGLE': {'champions': {}},
        'MIDDLE': {'champions': {}},
        'DUO_CARRY': {'champions': {}},
        'DUO_SUPPORT': {'champions': {}},
      },
      'total_games': 0,
    }
    for match_result in match_results:
      if match_result.stats.win:
        win_lose = 'win'
      else:
        win_lose = 'lose'
      champion_id = match_result.participant.champion_id
      if not champion_id in result['champions']:
        result['champions'][champion_id] = {'win': 0, 'lose': 0, 'ratio': 0, 'games': 0}
      result['champions'][champion_id][win_lose] += 1
      result['champions'][champion_id]['games'] += 1
      lane = match_result.timeline.lane
      if lane == 'NONE':
        continue
      elif lane == 'BOTTOM':
        lane = match_result.timeline.role
      if lane == 'NONE':
        continue

      result['lane'][lane][win_lose] += 1
      result['lane'][lane]['games'] += 1
    return result

  def merge_result(self, results):
    res = {
      'champions': {},
      'lane': {
        'TOP': {'win': 0, 'lose': 0, 'games': 0, 'ratio': 0},
        'JUNGLE': {'win': 0, 'lose': 0, 'games': 0, 'ratio': 0},
        'MIDDLE': {'win': 0, 'lose': 0, 'games': 0, 'ratio': 0},
        'DUO_CARRY': {'win': 0, 'lose': 0, 'games': 0, 'ratio': 0},
        'DUO_SUPPORT': {'win': 0, 'lose': 0, 'games': 0, 'ratio': 0},
      },
      'champions_by_lane': {
        'TOP': {'champions': {}},
        'JUNGLE': {'champions': {}},
        'MIDDLE': {'champions': {}},
        'DUO_CARRY': {'champions': {}},
        'DUO_SUPPORT': {'champions': {}},
      },
      'total_games': 0,
    }
    for data in results:
      for champion_id, value in data['champions'].items():
        if not champion_id in res['champions']:
          res['champions'][champion_id] = {'win': 0, 'lose': 0, 'games': 0, 'ratio': 0}
        res['champions'][champion_id]['win'] += value['win']
        res['champions'][champion_id]['lose'] += value['lose']
        res['champions'][champion_id]['games'] += value['games']

      for lane_key, lane_data in res['lane'].items():
        lane_data['win'] += data['lane'][lane_key]['win']
        lane_data['lose'] += data['lane'][lane_key]['lose']
        lane_data['games'] += data['lane'][lane_key]['games']

    return res
