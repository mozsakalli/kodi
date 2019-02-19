# -*- coding: utf-8 -*-
# Module: default
# Author: Mustafa Ozsakalli
# Created on: 28.11.2014
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import sys
from urllib import urlencode
from urlparse import parse_qsl
import urllib2
import json
import xbmcgui
import xbmcplugin
import xbmc
import base64
import re

SITEURL = 'https://www.hdfilmcehennemi1.com'

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

SEARCH_RESULT = []

def get_input(name):

    exit = True 
    while (exit):
          kb = xbmc.Keyboard('default', 'heading', True)
          kb.setDefault(name)
          kb.setHeading('Enter Search Keyword')
          kb.setHiddenInput(False)
          kb.doModal()
          if (kb.isConfirmed()):
              name = kb.getText()
              exit = False
    return(name)

def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :type kwargs: dict
    :return: plugin call URL
    :rtype: str
    """
    return '{0}?{1}'.format(_url, urlencode(kwargs))

def log(msg):
  xbmc.log(msg, level=xbmc.LOGNOTICE)

def fetch_url(url):
  req = urllib2.Request(url)
  req.add_header('Referer',SITEURL)
  req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36')
  return urllib2.urlopen(req).read()

SPECIALS = [
  {'title':'Son Eklenenler', 'key':''},
  {'title':'IMDb 7+ Filmler', 'key':'/imdb-7'},
  {'title':'En Çok Beğenilenler', 'key':'/en-cok-begenilenler'},
  {'title':'Animasyon Filmler', 'key':'/tur/animasyon'},
  {'title':'Bilim Kurgu Filmleri', 'key':'/tur/bilim-kurgu'},
  {'title':'Aksiyon Filmleri', 'key':'/tur/aksiyon'},
  {'title':'Macera Filmleri', 'key':'/tur/macera'},
  {'title':'Fantastik Filmler', 'key':'/tur/fantastik'},
  {'title':'Komedi Filmleri', 'key':'/tur/komedi'},
  {'title':'Belgesel Filmler', 'key':'/tur/belgesel'},
  {'title':'Hint Filmleri', 'key':'/ulke/hindistan'},
]

def list_search():
    xbmcplugin.setPluginCategory(_handle, 'HdFilmCehennemi.Com')
    xbmcplugin.setContent(_handle, 'videos')
    list_item = xbmcgui.ListItem(label='Film Ara')
    url = get_url(action='search')
    is_folder = True
    xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

    for item in SPECIALS :
      list_item = xbmcgui.ListItem(label=item['title'])
      url = get_url(action='special', title=str(item['title']), key=item['key'].encode('utf-8'))
      xbmcplugin.addDirectoryItem(_handle, url, list_item, True)

    #list_item = xbmcgui.ListItem(label='IMDb 7+ Filmler')
    #url = get_url(action='imdb7')f
    #is_folder = True
    #xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    #xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)

def find_search_link():
  html = fetch_url(SITEURL+'/?s=bumblebee')
  cx =re.findall("var cx = '([^']+)'", html)[0]
  log('cx = '+cx)
  html = fetch_url('https://cse.google.com/cse.js?cx='+cx)
  log(html)
  cse_token = re.findall('"cse_token": "([^"]+)"', html)[0]
  exp = ",".join(json.loads(re.findall('"exp": (\[[^\]]+\])', html)[0]))
  #",".join(re.findall('"exp": \["([^"]+)", "([^"]+)"', html))
  log('cse = '+cse_token+" exp="+exp)
  return "https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=10&hl=tr&source=gcsc&gss=.com&cx={0}&safe=off&cse_tok={1}&sort=&exp={2}&callback=google.search.cse.api56".format(cx, cse_token, exp)


def do_search():
  text_to_search = get_input('')
  url = find_search_link()
  url = url+'&{0}'.format(urlencode({'q':text_to_search}))
  #url = 'https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=10&hl=tr&source=gcsc&gss=.com&cx=015716483505879080032:ixt5mjxgo3i&safe=off&cse_tok=AKaTTZhXLPRINybw3smeHRwJhdEV:1550151152902&sort=&exp=csqr,4231017&callback=google.search.cse.api5553&{0}'.format(urlencode({'q':text_to_search}))
  #url = 'https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=10&hl=tr&source=gcsc&gss=.com&cx=015716483505879080032:ixt5mjxgo3i&safe=off&cse_tok=AKaTTZjvhM4zTZlDEUVQmW9nqIhC:1550331064626&sort=&exp=csqr,4231017&callback=google.search.cse.api19970&{0}'.format(urlencode({'q':text_to_search}))
  #english
  #url='https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=10&hl=en&source=gcsc&gss=.com&cx=013555815768498568673:vzcfsubz2aq&safe=off&cse_tok=AKaTTZjuQ86TcktKGwZ73gdm3EC0:1550350923553&sort=&exp=csqr,4231017&callback=google.search.cse.api3320&{0}'.format(urlencode({'q':text_to_search}))  
  html = fetch_url(url)
  #log(html)

  html = html[html.find('{') : html.rfind('}')+1]
  js = json.loads(html)

  xbmcplugin.setPluginCategory(_handle, 'HdFilmCehennemi.Com')
  xbmcplugin.setContent(_handle, 'videos')

  for movie in js['results']:
    meta = movie['richSnippet']['metatags']
    img = meta.get('ogImage','')
    if img != '' :
      title = ''.join(meta['ogTitle'].split('|')[0].split('izle')).strip()
      list_item = xbmcgui.ListItem(label=title)
      list_item.setArt({'thumb': img, 'icon': img, 'fanart': img})
      list_item.setInfo('video', {
        'plot': movie['content']
        })
      url = get_url(action='sources', url=meta['ogUrl'], title=title.encode('utf-8'), image=img.encode('utf-8'))
      xbmcplugin.addDirectoryItem(_handle, url, list_item, True)

  xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
  # Finish creating a virtual folder.
  xbmcplugin.endOfDirectory(_handle)

def extract_movies(html):
  #log('html='+html)
  html = ''.join(html.split("\n"))
  movies = []
  #rapid frame
  m = re.findall('file:"([^"]+)"(,label:"([^"]+)")?', html, re.MULTILINE)
  if(m):
    for v in m:
      if(v[2] != ''):
        movies.append({'title':v[2], 'url':v[0]})

  if(len(movies) == 0):
    #fx
    m = re.findall('file:"([^"]+)"', html, re.MULTILINE)
    if m and len(m)>0 and m[0] != '' :
      movies.append({'title':'', 'url':v[0]})


  return movies

def fetch_video_link(url):
  html = fetch_url(url)
  #log('html='+html)
  links = re.findall('<li( class="selected")?><a href="([^"]+)"><span[^>]*>([^<]+).*?</li>',re.findall('<ul class="hdc-parts"(.*?)</ul>', html, re.MULTILINE|re.DOTALL)[0], re.MULTILINE|re.DOTALL)
  #log('link-html = '+str(linkhtml))

  movies=[]
  for link in links:
    if(link[0]!=''):
      h=html
    else:
      h=fetch_url(link[1])

    m = re.search('atob\(([^\)]+)',h)
    if(m):
      varname = m.group(1);
      m = re.search("var "+varname+" = '([^']+)'", h)
      if(m):
        code = base64.b64decode(m.group(1))
        m = re.search('src="([^"]+)"', code)
        movielink = m.group(1)
        found = extract_movies(fetch_url(movielink))
        for m in found:
          movies.append({'title':link[2]+' - '+m['title'], 'url':m['url']})
  return movies


def list_sources(index_url, movieTitle, movieImage, movieGenre, movieDesc):
  movies = fetch_video_link(index_url)  
  xbmcplugin.setPluginCategory(_handle, movieTitle)
  xbmcplugin.setContent(_handle, 'videos')
  for m in movies:
    list_item = xbmcgui.ListItem(label=movieTitle+' - '+m['title'])
    list_item.setInfo('video', {'title': movieTitle+' - '+m['title'],
                                'mediatype': 'video'})
    list_item.setArt({'thumb': movieImage, 'icon': movieImage, 'fanart': movieImage})
    list_item.setProperty('IsPlayable', 'true')
    xbmcplugin.addDirectoryItem(_handle, m['url'], list_item, False)

  xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
  xbmcplugin.endOfDirectory(_handle)

def list_special(listTitle, listKey):
  log('special: '+listTitle+" , "+listKey)
  xbmcplugin.setPluginCategory(_handle, listTitle)
  xbmcplugin.setContent(_handle, 'videos')

  seen = {}
  for page in range(1,6):
    html = fetch_url(SITEURL+listKey+'/page/'+str(page)+'/')
    movies = re.findall('<div class="poster poster-pop" data-original-title="([^"]+)".*?data-types="([^"]+)".*?data-year="([^"]+)".*?data-content="([^"]+)".*?<a href="([^"]+)".*?<img.*?data-flickity-lazyload="([^"]+)".*?<span>IMDb</span>([^<]+)',html,re.MULTILINE|re.DOTALL)
    #log('new-movies: '+str(movies))       
    for m in movies:
      title = ''.join(m[0].split('|')[0].split('izle')).strip()
      if title[0:5] == 'Watch ':
        title = title[6]
      if seen.get(title, False) == False :
        genre = str(m[1])
        year = str(m[2])
        desc = str(m[3])
        img = str(m[5])
        imdb = str(m[6]).strip()
        list_item = xbmcgui.ListItem(label=title+' ('+year+' imdb:'+imdb+')', label2=desc)
        list_item.setArt({'thumb': img, 'icon': img, 'fanart': img})
        list_item.setInfo('video', {
          'genre':genre, 'tagline':desc, 'plot':desc
        })
        url = get_url(action='sources', url=str(m[4]), title=str(title), image=str(img), genre=genre, year=year, desc=desc)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
        seen[title] = True

  #xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
  xbmcplugin.endOfDirectory(_handle)


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring: URL encoded plugin paramstring
    :type paramstring: str
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'search':
            do_search()
        elif params['action'] == 'special':
            list_special(params['title'], params.get('key',''))
        elif params['action'] == 'sources':
            list_sources(params['url'], params.get('title',''), params.get('image',''), params.get('genre',''), params.get('desc',''))
        else:
            # If the provided paramstring does not contain a supported action
            # we raise an exception. This helps to catch coding errors,
            # e.g. typos in action names.
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring)+' action='+params['action'])
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        # list_categories()
        list_search()


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
