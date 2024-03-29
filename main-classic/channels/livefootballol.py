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
__channel__ = "livefootballol"
__category__ = "d"
__type__ = "generic"
__title__ = "Livefootballol"
__language__ = "ES"

host ="http://www.livefootballol.me"
song=os.path.join(config.get_runtime_path(), 'Extreme.mp3')
DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.livefootballol mainlist")
    itemlist = []
    #check =xbmc.getInfoLabel('Container.FolderPath')
    
    xbmc.executebuiltin('xbmc.PlayMedia('+song+')')
    item.url = "http://www.livefootballol.me/live-football-streaming.html"
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    patronmain = '<h3>(.*?)CEST</h3></div>(.*?)</list>'
    matchesmain = re.compile(patronmain,re.DOTALL).findall(data)
    print "perro"
    print matchesmain
    
    for fecha , bloque_enlaces  in matchesmain:
        fecha = (translate(fecha,"es"))
        fecha = fecha.replace(fecha,"[COLOR yellow][B]"+fecha+"[/B][/COLOR]")
        itemlist.append( Item(channel=__channel__, title="                         "+fecha,action="enlaces",url = item.url,fanart = "http://s6.postimg.org/qdk670wb5/livefootbalolfan.jpg",thumbnail="http://s6.postimg.org/556hplhu9/calendar_clock_icon_34472.png",folder=False) )
        patron = '<img src="([^"]+)".*?> (\d\d:\d\d) \[(.*?)\] <a href="([^"]+)".*?>([^<]+)</a>'
        matches = re.compile(patron,re.DOTALL).findall(bloque_enlaces)
        for thumb, hora, tipo, enlace,partido in matches:
            hora = hora.replace(hora,"[COLOR green][B]"+hora+"[/B][/COLOR]")
            partido = partido.replace(partido,"[COLOR floralwhite][B]"+partido+"[/B][/COLOR]")
            tipo = tipo.replace(tipo,"[COLOR skyblue][B]"+tipo+"[/B][/COLOR]")
            title = hora+" "+partido+"("+tipo+")"
            url = enlace
            if not "unibet" in enlace:
               itemlist.append( Item(channel=__channel__, title=title,action="enlaces",url=urlparse.urljoin(host,enlace),thumbnail =urlparse.urljoin(host,thumb),fanart ="http://s6.postimg.org/qdk670wb5/livefootbalolfan.jpg",fulltitle = title,folder=True) )
    
    return itemlist

def enlaces (item):
    logger.info("pelisalacarta.livefootballol enlaces")
    itemlist = []
    data = scrapertools.cache_page(item.url)
    patronenlaces = '<p><strong>.*?</strong>(.*?)</table>'
    matchesenlaces= re.compile(patronenlaces,re.DOTALL).findall(data)
    for bloque_video in matchesenlaces:
        patron= '<a href="([^"]+)">(.*?)</a>'
        matches =re.compile(patron,re.DOTALL).findall(bloque_video)
        if len(matches)==0:
            
           xbmc.executebuiltin('Action(Back)')
           xbmc.sleep(10)
           xbmc.executebuiltin('Notification([COLOR crimson][B]NO HAY ENLACES...[/B][/COLOR], [COLOR yellow][B]'+'Sopcat/Acestrem'.upper()+'[/B][/COLOR],4000,"http://s6.postimg.org/c5x7330r5/livefootballollogo.png")')
        for enlace, canal in matches:
            title =  canal
            title= re.sub(r"</strong>|<strong>","",title)
            title=title.replace(title,"[COLOR orange]"+title+"[/COLOR]")
            if "AceStream" in title :
                title = title.replace("AceStream","[COLOR palegreen][B]AceStream[/B][/COLOR]")
                thumbnail = "http://s6.postimg.org/c2c0jv441/torrent_stream_logo_300x262.png"
            else:
                title =title.replace("Sopcast","[COLOR skyblue][B]Sopcast[/B][/COLOR]")
                thumbnail = "http://s6.postimg.org/v9z5ggmfl/sopcast.jpg"
             
            itemlist.append( Item(channel=__channel__, title=title,action="links",url=enlace,thumbnail =thumbnail,fanart ="http://s6.postimg.org/d0h14ergx/livefootbalolfan3.jpg",fulltitle =item.title,folder=True) )

    return itemlist
def links(item):
    logger.info("pelisalacarta.livefootballol links")
    itemlist = []
    data = scrapertools.cache_page(item.url)
    patron = '<a href="([^"]+)">.*?</a>(.*?)</td>'
    matches=re.compile(patron,re.DOTALL).findall(data)
    for link, calidad in matches:
        title = "[COLOR crimson][B]Link[/B][/COLOR]" +"  "+ calidad
        if not "<i class" in calidad:
              if "HD" in calidad:
                 thumbnail = "http://s6.postimg.org/lk0f25ztd/livefootballhdlink.png"
              else:
                 thumbnail="http://s6.postimg.org/ryzfyu6j5/livefootbalolsdlink.png"
              itemlist.append( Item(channel=__channel__, title=title,action="play",url=link,thumbnail =thumbnail,fanart ="http://s6.postimg.org/68qm1k2hd/livefootballfan2.jpg",fulltitle =item.title,folder=True) )
    return itemlist

def play(item):
    logger.info("pelisalacarta.livefootballol play")
    itemlist = []
    import xbmc
    xbmc.executebuiltin('xbmc.PlayMedia(Stop)')
    fulltitle = item.fulltitle
    # Se incluye el título en la url para pasarlo al conector
    url= item.url + "|" + fulltitle
    
    itemlist.append(Item(channel=__channel__, title=item.title, server="p2p", url=url, action="play", folder=False))
    
    return itemlist

def translate(to_translate, to_langage="auto", langage="auto"):
    ###Traducción atraves de Google
    '''Return the translation using google translate
        you must shortcut the langage you define (French = fr, English = en, Spanish = es, etc...)
        if you don't define anything it will detect it or use english by default
        Example:
        print(translate("salut tu vas bien?", "en"))
        hello you alright?'''
    agents = {'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)"}
    before_trans = 'class="t0">'
    link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s" % (to_langage, langage, to_translate.replace(" ", "+"))
    request = urllib2.Request(link, headers=agents)
    page = urllib2.urlopen(request).read()
    result = page[page.find(before_trans)+len(before_trans):]
    result = result.split("<")[0]
    return result

if __name__ == '__main__':
    to_translate = 'Hola como estas?'
    print("%s >> %s" % (to_translate, translate(to_translate)))
    print("%s >> %s" % (to_translate, translate(to_translate, 'fr')))
#should print Hola como estas >> Hello how are you
#and Hola como estas? >> Bonjour comment allez-vous?



