from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import RequestContext
from pb_analyzer.crawler import Crawler
from pb_analyzer.analyzer import Analyzer
from pb_analyzer.models import Summoner, SummonerMatchResult
from pb_analyzer.constants import CHAMPIONS_BY_ID
from background_task import background


def index(request):
  if request.method == 'GET':
    return render(request, 'pb_analyzer/index.html')
  elif request.method == 'POST':
    context = RequestContext(request, {})
    summoner_names = request.POST['summoner_names'].lower().replace(' ', '').split(',')
    summoner_ids = []
    crawler = Crawler()
    for summoner_name in summoner_names:
      summoner = Summoner.objects.filter(name=summoner_name).first()

      if not summoner:
        summoner = crawler.crawl_summoner_by_name(summoner_name)
        return HttpResponse('{}は存在しません'.format(summoner_name), context)
      summoner_ids.append(summoner.account_id)

    return redirect('analyze', ','.join([str(id) for id in summoner_ids]))


def analyze(request, ids):
  summoners = []
  for account_id in ids.split(','):
    print(account_id)
    summoner = Summoner.objects.filter(account_id=account_id).first()
    if not summoner:
      return HttpResponse('{}は存在しないidです'.format(account_id))
    summoners.append(summoner)

  if request.method == 'GET':
    analyzer = Analyzer()
    results = []
    for summoner in summoners:
      results.append({
        'summoner': summoner,
        'result' : analyzer.analyze_summoner(summoner),
      })
    return render(request, 'pb_analyzer/analysis.html', {
      'results': results,
      'CHAMPIONS_BY_ID': CHAMPIONS_BY_ID,
    })
  elif request.method == 'POST':
    run_crawler(summoner.account_id)
    analyzer = Analyzer()
    result = analyzer.analyze_summoner(summoner)
    context = RequestContext(request, {})
    return render(request, 'pb_analyzer/analysis.html', {
      'summoner': summoner,
      'result': result,
      'CHAMPIONS_BY_ID': CHAMPIONS_BY_ID,
    }, context)

@background(schedule=5)
def run_crawler(account_id):
  crawler = Crawler()
  analyzer = Analyzer()
  game_ids = crawler.crawl_match_by_id(account_id, end_index=100)
  for game_id in game_ids:
    analyzer.analyze_match_by_game_id(game_id)
