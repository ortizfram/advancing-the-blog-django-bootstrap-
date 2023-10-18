# custom_filters.py
from django import template

register = template.Library()

@register.filter(name='facebook_share_url')
def facebook_share_url(absolute_url):
    return f'https://www.facebook.com/sharer/sharer.php?u={absolute_url}'

@register.filter(name='whatsapp_share_url')
def whatsapp_share_url(absolute_url):
    return f'https://api.whatsapp.com/send?text={absolute_url}'

@register.filter(name='linkedin_share_url')
def linkedin_share_url(absolute_url):
    return f'https://www.linkedin.com/shareArticle?mini=true&url={absolute_url}'
