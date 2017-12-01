import time
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import RequestContext
from pb_analyzer.crawler import Crawler
from pb_analyzer.analyzer import Analyzer
from pb_analyzer.models import Summoner, SummonerMatchResult, Match
from background_task.models import Task
from background_task import background


def index(request):
  if request.method == 'GET':
    return render(request, 'pb_analyzer/index.html')
  elif request.method == 'POST':
    context = RequestContext(request, {})
    summoner_names = request.POST['summoner_names'].split(',')
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
    summoner = Summoner.objects.filter(account_id=account_id).first()
    if not summoner:
      return HttpResponse('{}は存在しないidです'.format(account_id))
    summoners.append(summoner)

  analyzer = Analyzer()
  results = []
  for summoner in summoners:
    data = analyzer.analyze_summoner(summoner)
    results.append({
      'summoner': summoner,
      'result' : data,
    })

  team_result = analyzer.merge_result([result['result'] for result in results])

  if request.method == 'GET':
    return render(request, 'pb_analyzer/analysis.html', {
      'queue_count': Task.objects.all().count(),
      'team_result': team_result,
      'results': results
    })
  elif request.method == 'POST':
    run_crawler(request.POST['account_id'])
    context = RequestContext(request, {})
    return render(request, 'pb_analyzer/analysis.html', {
      'queue_count': Task.objects.all().count(),
      'team_result': team_result,
      'results': results,
    }, context)

@background(schedule=3)
def run_crawler(account_id):
  crawler = Crawler()
  game_ids = crawler.list_gameids_by_account_id(account_id, end_index=100)
  for game_id in game_ids:
    crawl_match_by_game_id(game_id)

@background(schedule=0)
def crawl_match_by_game_id(game_id):
  crawler = Crawler()
  analyzer = Analyzer()
  if not Match.objects.filter(game_id=game_id).first():
    crawler.crawl_match_by_game_id(game_id)
    time.sleep(2)
  analyzer.analyze_match_by_game_id(game_id)
