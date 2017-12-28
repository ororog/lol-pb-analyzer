from django import template
from pb_analyzer.constants import CHAMPIONS_BY_ID
register = template.Library()

@register.filter
def get_item(dictionary, key):
  return dictionary.get(key)

@register.filter
def get_ratio(value, games):
  return str(round(100 * value / games, 2)) + "%" if games > 0 else "0.0%"

@register.filter
def get_champion_name(champion_id):
  return CHAMPIONS_BY_ID[champion_id]
