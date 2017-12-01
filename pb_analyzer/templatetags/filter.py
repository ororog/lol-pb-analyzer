from django import template
from pb_analyzer.constants import CHAMPIONS_BY_ID
register = template.Library()

@register.filter
def get_item(dictionary, key):
  return dictionary.get(key)

@register.filter
def get_champion_name(champion_id):
  return CHAMPIONS_BY_ID[champion_id]
