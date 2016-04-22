# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cineblog01
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
import re, htmlentitydefs

from core import scrapertools
from core import logger
from core import config
from platformcode import xbmctools
import xbmcplugin
import xbmcaddon
from core.item import Item
from servers import servertools
import xbmc
import time
zorro= os.getcwd()
print "eyyyy"
print zorro
__channel__ = "arenavision"
__category__ = "F,S,A"
__type__ = "generic"
__title__ = "Arenavision"
__language__ = "ES"

host ="http://arenavision.in"
song = os.path.join(config.get_runtime_path(), 'best-day-of-my-life.mp3')
DEBUG = config.get_setting("debug")
def isGeneric():
    return True


def mainlist(item):
    logger.info("pelisalacarta.arenavision schedule")
    
    itemlist = []
    
    check =xbmc.getInfoLabel('Container.FolderPath')
    print "lolooo"
    print check
    xbmc.executebuiltin('xbmc.PlayMedia('+song+')')
    
    # Descarga la página
    item.url="http://arenavision.in/agenda"
    data = scrapertools.cache_page(item.url)
    patron_bloque = 'Bruselas(.*?)</footer>'
    matchesenlaces = re.compile(patron_bloque,re.DOTALL).findall(data)
    for pepe in matchesenlaces:
        patron = '(\d+/\d+/\d+) (\d+:\d+) CET (.*?:)(.*? \(.*?\))(.*?)<.*?>'
        matches = re.compile(patron,re.DOTALL).findall(pepe)

        for dia , hora, deporte, partido, av in matches:
            dia = "[COLOR darkkhaki][B]"+dia+"[/B][/COLOR]"
            hora = "[COLOR chartreuse][B]"+hora+"[/B][/COLOR]"
            deporte = "[COLOR burlywood][B]"+deporte+"[/B][/COLOR]"
            partido = "[COLOR orangered][B]"+partido+"[/B][/COLOR]"
            title = dia + "--"+hora+"--"+ deporte + partido
        
            itemlist.append( Item(channel=__channel__, title=title,action="enlaces",url = "",extra= av , thumbnail= "http://s6.postimg.org/csumvetu9/arenavisionthumb.png",fanart="http://s6.postimg.org/e965djwr5/arenavisionfan.jpg",fulltitle= partido, folder=False) )
    return itemlist

def enlaces(item):
    logger.info("pelisalacarta.arenavision scraper")
    
    itemlist = []
    import xbmcgui
    patron = '(AV\d+)'
    matches = re.compile(patron,re.DOTALL).findall(item.extra)
    for (i , f) in enumerate(matches):
        if "AV" in f:
            a = re.compile('AV(\d+)',re.DOTALL).findall(f)
            for (b,c) in enumerate(a):
                   
                   
                if c== "9" or c =="8" or c =="7" or c =="6" or c =="5" or c =="4" or c =="3" :
                    c= " "+c
                   
                if c <= "20" :
                    matches[i] = f.replace(f,"[COLOR crimson][B]"+matches[i]+"[/B][/COLOR]")+ "[COLOR palegreen][B]  Acestream[/B][/COLOR]"
                else:
                    matches[i] = f.replace(f,"[COLOR crimson][B]"+matches[i]+"[/B][/COLOR]")+ "[COLOR deepskyblue][B]  Sopcast[/B][/COLOR]"
            
            
        get_url= [(i,x) for i, x in enumerate(matches)]
        get_url = repr(get_url)
            #get_url= re.sub(r"\[COLOR.*?\]\[.*?]|\[.*?\]\[/COLOR\].*?\[.*?\]\[/COLOR\]","",get_url)
        print "marco"
        print get_url
        fulltitle =item.fulltitle
        print "pacopepe"
        print fulltitle
    index = xbmcgui.Dialog().select("[COLOR orange][B]Selecciona Canal...[/B][/COLOR]", matches)
        
    if index != -1:
        index =str(index)
        print "kkkk"
        print get_url
        if index == 0:
            catch_url=scrapertools.get_match(get_url,'\('+index+',.*?\'\[COLOR crimson\]\[B\](.*?)\[')
        catch_url=scrapertools.get_match(get_url,''+index+',.*?\'\[COLOR crimson\]\[B\](.*?)\[')
        url =urlparse.urljoin(host,catch_url)
            
        import xbmc
        xbmc.executebuiltin('xbmc.PlayMedia(Stop)')
        ### Esto sustituye a la función go
        data = scrapertools.cache_page(url)
        patron = '\*INFO.*?Click.*?<a href="([^"]+)"'
        url = scrapertools.find_single_match(data, patron)
        item.url = url +"|" + fulltitle
        print "tu vieja"
        print item.url
        item.server = "p2p"        
        xbmctools.play_video(item)
			
    else:
        import xbmc
        xbmc.executebuiltin( "XBMC.Container.Update" )
        return


def press():
    import xbmc
    xbmc.executebuiltin('Action(Select)')