from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import RequestContext
from pb_analyzer.crawler import Crawler
from pb_analyzer.models import Summoner

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
  crawler = Crawler()
  for id in [int(id) for id in ids.split(',')]:
    crawler.crawl_match_by_id(id)

  return HttpResponse('hello analyze {}'.format(ids))
