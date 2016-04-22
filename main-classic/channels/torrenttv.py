# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para livetv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
import re, htmlentitydefs
from core import scrapertools
from core import logger
from core import config
import xbmcplugin
import xbmcaddon
from core.item import Item
from servers import servertools
from core.scrapertools import decodeHtmlentities as dhe
import xbmc
__channel__ = "torrenttv"
__category__ = "deportes"
__type__ = "generic"
__title__ = "Torrenttv"
__language__ = "ES"

host ="http://super-pomoyka.us.to/trash/ttv-list/ttv.m3u"
song=os.path.join(config.get_runtime_path(), 'Queen We Are The Champions.mp3')
DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.torrenttv mainlist")
    itemlist = []
    
    xbmc.executebuiltin('xbmc.PlayMedia('+song+')')
    item.url = host
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    patron = 'EXTINF.*?,(.*?) \((Спорт)\).*?(acestream.*?)#'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for nombre,tipo, url  in matches:
        title = "[COLOR darkorange][B]"+nombre+"[/B][/COLOR]"
        
        if "acestream" in title:
           print "eliminado"
        else:
             itemlist.append( Item(channel=__channel__, title=title,action="play",url = url,thumbnail="http://s6.postimg.org/imesq7i4x/ttvlogo.png",fanart="http://s6.postimg.org/hy5y79jf5/Nike_soccer_wallpapers_HD_01_1280x720.jpg",fulltitle = title,folder=False) )

    
    
    return itemlist


def play(item):
    logger.info("pelisalacarta.torrenttv go")
    itemlist = []
    xbmc.executebuiltin('xbmc.PlayMedia(Stop)')
    fulltitle = item.fulltitle
    # Se incluye el título en la url para pasarlo al conector
    url= item.url + "|" + fulltitle
    itemlist.append(Item(channel=__channel__, title=item.title, server="p2p", url=url, action="play", folder=False))
    
    return itemlist



