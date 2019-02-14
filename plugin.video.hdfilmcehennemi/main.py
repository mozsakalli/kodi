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

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

# Free sample videos are provided by www.vidsplay.com
# Here we use a fixed set of properties simply for demonstrating purposes
# In a "real life" plugin you will need to get info and links to video files/streams
# from some web-site or online service.
VIDEOS = {'Animals': [{'name': 'Crab',
                       'thumb': 'http://www.vidsplay.com/wp-content/uploads/2017/04/crab-screenshot.jpg',
                       'video': 'http://www.vidsplay.com/wp-content/uploads/2017/04/crab.mp4',
                       'genre': 'Animals'},
                      {'name': 'Alligator',
                       'thumb': 'http://www.vidsplay.com/wp-content/uploads/2017/04/alligator-screenshot.jpg',
                       'video': 'http://www.vidsplay.com/wp-content/uploads/2017/04/alligator.mp4',
                       'genre': 'Animals'},
                      {'name': 'Turtle',
                       'thumb': 'http://www.vidsplay.com/wp-content/uploads/2017/04/turtle-screenshot.jpg',
                       'video': 'http://www.vidsplay.com/wp-content/uploads/2017/04/turtle.mp4',
                       'genre': 'Animals'}
                      ],
            'Cars': [{'name': 'Postal Truck',
                      'thumb': 'http://www.vidsplay.com/wp-content/uploads/2017/05/us_postal-screenshot.jpg',
                      'video': 'http://www.vidsplay.com/wp-content/uploads/2017/05/us_postal.mp4',
                      'genre': 'Cars'},
                     {'name': 'Traffic',
                      'thumb': 'http://www.vidsplay.com/wp-content/uploads/2017/05/traffic1-screenshot.jpg',
                      'video': 'http://www.vidsplay.com/wp-content/uploads/2017/05/traffic1.mp4',
                      'genre': 'Cars'},
                     {'name': 'Traffic Arrows',
                      'thumb': 'http://www.vidsplay.com/wp-content/uploads/2017/05/traffic_arrows-screenshot.jpg',
                      'video': 'http://www.vidsplay.com/wp-content/uploads/2017/05/traffic_arrows.mp4',
                      'genre': 'Cars'}
                     ],
            'Food': [{'name': 'Chicken',
                      'thumb': 'http://www.vidsplay.com/wp-content/uploads/2017/05/bbq_chicken-screenshot.jpg',
                      'video': 'http://www.vidsplay.com/wp-content/uploads/2017/05/bbqchicken.mp4',
                      'genre': 'Food'},
                     {'name': 'Hamburger',
                      'thumb': 'http://www.vidsplay.com/wp-content/uploads/2017/05/hamburger-screenshot.jpg',
                      'video': 'http://www.vidsplay.com/wp-content/uploads/2017/05/hamburger.mp4',
                      'genre': 'Food'},
                     {'name': 'Pizza',
                      'thumb': 'http://www.vidsplay.com/wp-content/uploads/2017/05/pizza-screenshot.jpg',
                      'video': 'http://www.vidsplay.com/wp-content/uploads/2017/05/pizza.mp4',
                      'genre': 'Food'}
                     ]}

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


def get_categories():
    """
    Get the list of video categories.

    Here you can insert some parsing code that retrieves
    the list of video categories (e.g. 'Movies', 'TV-shows', 'Documentaries' etc.)
    from some site or server.

    .. note:: Consider using `generator functions <https://wiki.python.org/moin/Generators>`_
        instead of returning lists.

    :return: The list of video categories
    :rtype: types.GeneratorType
    """
    return VIDEOS.iterkeys()


def get_videos(category):
    """
    Get the list of videofiles/streams.

    Here you can insert some parsing code that retrieves
    the list of video streams in the given category from some site or server.

    .. note:: Consider using `generators functions <https://wiki.python.org/moin/Generators>`_
        instead of returning lists.

    :param category: Category name
    :type category: str
    :return: the list of videos in the category
    :rtype: list
    """
    return VIDEOS[category]


def list_categories():
    """
    Create the list of video categories in the Kodi interface.
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_handle, 'My Video Collection')
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_handle, 'videos')
    # Get video categories
    categories = get_categories()
    # Iterate through categories
    for category in categories:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=category)
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'thumb': VIDEOS[category][0]['thumb'],
                          'icon': VIDEOS[category][0]['thumb'],
                          'fanart': VIDEOS[category][0]['thumb']})
        # Set additional info for the list item.
        # Here we use a category name for both properties for for simplicity's sake.
        # setInfo allows to set various information for an item.
        # For available properties see the following link:
        # https://codedocs.xyz/xbmc/xbmc/group__python__xbmcgui__listitem.html#ga0b71166869bda87ad744942888fb5f14
        # 'mediatype' is needed for a skin to display info for this ListItem correctly.
        list_item.setInfo('video', {'title': category,
                                    'genre': category,
                                    'mediatype': 'video'})
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = get_url(action='listing', category=category)
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def list_videos(category):
    """
    Create the list of playable videos in the Kodi interface.

    :param category: Category name
    :type category: str
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_handle, category)
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_handle, 'videos')
    # Get the list of videos in the category.
    videos = get_videos(category)
    # Iterate through videos.
    for video in videos:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=video['name'])
        # Set additional info for the list item.
        # 'mediatype' is needed for skin to display info for this ListItem correctly.
        list_item.setInfo('video', {'title': video['name'],
                                    'genre': video['genre'],
                                    'mediatype': 'video'})
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'thumb': video['thumb'], 'icon': video['thumb'], 'fanart': video['thumb']})
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/wp-content/uploads/2017/04/crab.mp4
        url = get_url(action='play', video=video['video'])
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = False
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def play_video(path):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=path)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)

def log(msg):
  xbmc.log(msg, level=xbmc.LOGNOTICE)

def fetch_url(url):
  req = urllib2.Request(url)
  req.add_header('Referer','https://www.hdfilmcehennemi1.com/')
  req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36')
  return urllib2.urlopen(req).read()

def list_search():
    xbmcplugin.setPluginCategory(_handle, 'HdFilmCehennemi.Com')
    xbmcplugin.setContent(_handle, 'videos')
    list_item = xbmcgui.ListItem(label='Search')
    url = get_url(action='search')
    is_folder = True
    xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

    list_item = xbmcgui.ListItem(label='Son Eklenenler')
    url = get_url(action='news')
    is_folder = True
    xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)

def do_search():
  text_to_search = get_input('')
  url = 'https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=10&hl=tr&source=gcsc&gss=.com&cx=015716483505879080032:ixt5mjxgo3i&safe=off&cse_tok=AKaTTZhXLPRINybw3smeHRwJhdEV:1550151152902&sort=&exp=csqr,4231017&callback=google.search.cse.api5553&{0}'.format(urlencode({'q':text_to_search}))
  #xbmc.log(url, level=xbmc.LOGNOTICE)

  req = urllib2.Request(url)
  req.add_header('Referer','https://www.hdfilmcehennemi1.com/')
  req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36')
  html = urllib2.urlopen(req).read()
  html = html[html.find('{') : html.rfind('}')+1]
  #xbmc.log(html, level=xbmc.LOGNOTICE)
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
  log('html='+html)
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

def list_news():
  xbmcplugin.setPluginCategory(_handle, 'News')
  xbmcplugin.setContent(_handle, 'videos')

  seen = {}
  for page in range(1,6):
    html = fetch_url('https://www.hdfilmcehennemi1.com/page/'+str(page)+'/')
    movies = re.findall('<div class="poster poster-pop" data-original-title="([^"]+)".*?data-types="([^"]+)".*?data-year="([^"]+)".*?data-content="([^"]+)".*?<a href="([^"]+)".*?<img.*?data-flickity-lazyload="([^"]+)"',html,re.MULTILINE|re.DOTALL)
       
    for m in movies:
      title = ''.join(m[0].split('|')[0].split('izle')).strip()
      if seen.get(title, False) == False :
        genre = str(m[1])
        year = str(m[2])
        desc = str(m[3])
        img = str(m[5])
        list_item = xbmcgui.ListItem(label=title+' ('+year+')', label2=desc)
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
        elif params['action'] == 'news':
            list_news()
        elif params['action'] == 'sources':
            list_sources(params['url'], params.get('title',''), params.get('image',''), params.get('genre',''), params.get('desc',''))
        elif params['action'] == 'listing':
            # Display the list of videos in a provided category.
            list_videos(params['category'])
        elif params['action'] == 'play':
            # Play a video from a provided URL.
            play_video(params['video'])
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