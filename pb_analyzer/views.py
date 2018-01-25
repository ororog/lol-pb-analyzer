import time
import urllib
from django.conf import settings
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
    return render(request, 'pb_analyzer/index.html', {
      'queue_count': Task.objects.all().count()
    })
  elif request.method == 'POST':
    context = RequestContext(request, {})
    summoner_names = request.POST['summoner_names'].split(',')
    crawler = Crawler()
    for summoner_name in summoner_names:
      summoner = Summoner.objects.filter(name=summoner_name).first()
      if not summoner:
        try:
          summoner = crawler.crawl_summoner_by_name(summoner_name)
          if not summoner:
            return HttpResponse('Summnoer "{}" is not found.'.format(summoner_name), context)
        except:
          import traceback
          traceback.print_exc()
          return HttpResponse('Sorry, API Limit exceeding now...', context)
    return redirect('analyze', ','.join(summoner_names))

def analyze(request, names):
  summoners = []
  for summoner_name in names.split(','):
    summoner_name = urllib.parse.unquote(summoner_name)
    summoner = Summoner.objects.filter(name=summoner_name).first()
    if not summoner:
      return HttpResponse('Summoner {} is not found'.format(summoner_name))
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
    account_id = request.POST['account_id']
    update_summoner(account_id)
    run_crawler(account_id)
    context = RequestContext(request, {})
    return redirect('analyze', names)

def update_summoner(account_id, region='jp1'):
  crawler = Crawler()
  crawler.update_summoner_by_id(account_id)

def run_crawler(account_id):
  try:
    game_ids = crawler.list_gameids_by_account_id(account_id, end_index=100)
    for game_id in game_ids:
      crawl_match_by_game_id(game_id)
  except:
    import traceback
    traceback.print_exc()

@background(schedule=0)
def crawl_match_by_game_id(game_id):
  crawler = Crawler()
  analyzer = Analyzer()
  if not Match.objects.filter(game_id=game_id).first():
    crawler.crawl_match_by_game_id(game_id)
    time.sleep(settings.SLEEP_TIME_AFTER_CRAWLING)
  analyzer.analyze_match_by_game_id(game_id)
