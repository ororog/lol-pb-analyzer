from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import RequestContext
from pb_analyzer.crawler import Crawler
from pb_analyzer.analyzer import Analyzer
from pb_analyzer.models import Summoner, SummonerMatchResult
from pb_analyzer.constants import CHAMPIONS_BY_ID


def index(request):
  if request.method == 'GET':
    return render(request, 'pb_analyzer/index.html')
  elif request.method == 'POST':
    context = RequestContext(request, {})
    summoner_name = request.POST['summoner_name']
    summoner = Summoner.objects.filter(name=summoner_name).first()

    if not summoner:
      crawler = Crawler()
      summoner = crawler.crawl_summoner_by_name(summoner_name)

    if summoner:
      return redirect('analyze', summoner.account_id)
    else:
      return HttpResponse('no summoner', context)

def analyze(request, ids):
  summoner = Summoner.objects.filter(account_id=ids).first()
  if not summoner:
    return HttpResponse('該当するサモナーはいません')

  if request.method == 'GET':
    analyzer = Analyzer()
    result = analyzer.analyze_summoner(summoner)
    return render(request, 'pb_analyzer/analysis.html', {
      'summoner': summoner,
      'result': result,
      'CHAMPIONS_BY_ID': CHAMPIONS_BY_ID,
    })
  elif request.method == 'POST':
    crawler = Crawler()
    game_ids = crawler.crawl_match_by_id(summoner.account_id)
    analyzer = Analyzer()
    for game_id in game_ids:
      analyzer.analyze_match_by_game_id(game_id)
    result = analyzer.analyze_summoner(summoner)
    context = RequestContext(request, {})
    return render(request, 'pb_analyzer/analysis.html', {
      'summoner': summoner,
      'result': result,
      'CHAMPIONS_BY_ID': CHAMPIONS_BY_ID,
    }, context)
