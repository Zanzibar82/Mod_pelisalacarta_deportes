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
import xbmc
from core.scrapertools import decodeHtmlentities as dhe

__channel__ = "livetv"
__category__ = "deportes"
__type__ = "generic"
__title__ = "Livetv"
__language__ = "ES"

host ="http://livetv.sx/es"
song = os.path.join(config.get_runtime_path(), 'imagine-dragons.mp3')

DEBUG = config.get_setting("debug")

def isGeneric():
    
    return True


def mainlist(item):
    logger.info("pelisalacarta.livetv mainlist")
    itemlist = []
    
    
    xbmc.executebuiltin('xbmc.PlayMedia('+song+')')
    
    
    #Live
    item.url = "http://livetv.sx/es/allupcomingsports"
    itemlist.append( Item(channel=__channel__, title="[COLOR red][B]LIVE!![/B][/COLOR]" , action="scraper_live", url=host, thumbnail="http://s6.postimg.org/brzwms041/LIVE.png", fanart="http://s6.postimg.org/lqkv999jl/321238_1024x768_www_The_Wallpapers_org.jpg"))
    
    # Main options
    item.url = "http://livetv.sx/es/allupcomingsports"
    data = dhe( scrapertools.cachePage(item.url) )
    patronmain ='<table width="100%" cellpadding=12 cellspacing=0>(.*?)<span class="sltitle">'
    matchesmain = re.compile(patronmain,re.DOTALL).findall(data)
    
    for main in matchesmain:
    
        patron = '<td background.*?href="([^"]+)".*?src="([^"]+)".*?<a class="main".*?><b>(.*?)</b></a>'
        matches = re.compile(patron,re.DOTALL).findall(main)
        for url,thumbnail,deporte in matches:
            if deporte== "Fútbol":
                extra = "http://s6.postimg.org/a2qtepkep/fotbal.jpg"
                deporte ="[COLOR palegreen][B]"+deporte+"[/B][/COLOR]"
            else:
                extra= "http://s6.postimg.org/fs71z0qkx/B9317206944_Z_1_20150503001849_000_GNEAM3_I82_1_0.jpg"
                deporte ="[COLOR skyblue][B]"+deporte+"[/B][/COLOR]"
            itemlist.append( Item(channel=__channel__, title=deporte,action="scraper",url = urlparse.urljoin(host,url),thumbnail= thumbnail,fanart="http://s6.postimg.org/lqkv999jl/321238_1024x768_www_The_Wallpapers_org.jpg",extra=extra,folder=True) )
        

    
    
    return itemlist
def scraper(item):
    logger.info("pelisalacarta.livetv scraper")
    
    itemlist = []
    
    # Descarga la página
    
    data = dhe( scrapertools.cachePage(item.url) )
    
    
    patron_bloque = '<table align="center" width="90%"></tr><tr><td colspan=4 height=48>(.*?)Archivo de transmisiones'
    matchesenlaces = re.compile(patron_bloque,re.DOTALL).findall(data)
    for pepe in matchesenlaces:
        patron = '<td width=34 align="center" valign="top">.*?src="([^"]+)".*?<a class.*?href="([^"]+)">(.*?)</a>.*?<span class="evdesc">(.*?)<br>(.*?)</span>'
        matches = re.compile(patron,re.DOTALL).findall(pepe)

        for thumbnail , ficha, title, fecha, info in matches:
            fecha = fecha.strip()
            info = info.strip()
            title = title.replace("&ndash;","___")
            fecha = deporte ="[COLOR gold][B]"+fecha+"[/B][/COLOR]"
            info = deporte ="[COLOR orange][B]"+info+"[/B][/COLOR]"
            if  item.extra =="http://s6.postimg.org/a2qtepkep/fotbal.jpg" :
               title ="[COLOR palegreen][B]"+title+"[/B][/COLOR]"
               extra = "futbol"
            else:
               title ="[COLOR skyblue][B]"+title+"[/B][/COLOR]"
               extra = "live"
            encuentro = fecha+ "--"+title +"--"+ info
            
            

            itemlist.append( Item(channel=__channel__, title=encuentro,action="enlaces",url = urlparse.urljoin(host,ficha),thumbnail= thumbnail,fanart=item.extra,extra=extra,fulltitile = title,folder=True) )
    return itemlist
def scraper_live(item):
    logger.info("pelisalacarta.livetv scraper")
    
    itemlist = []
    
    # Descarga la página
    
    data = dhe( scrapertools.cachePage(item.url) )
    
    
    patron_bloque = '<span class="date">Hoy.*?</span>(.*?)ensenar todo'
    matchesenlaces = re.compile(patron_bloque,re.DOTALL).findall(data)
    for pepe in matchesenlaces:
        patron = 'alt.*?src="([^"]+)".*?href="([^"]+)">([^"]+)</a>.*?<span class="evdesc">(\d+:\d+) \(([^"]+)\)'
        matches = re.compile(patron,re.DOTALL).findall(pepe)
        
        for thumbnail, url,title, hora, info in matches:
            info = info.strip()
            hora = hora.strip()
            info = "("+info+")"
            title = title.replace("&ndash;","___")
            hora = "[COLOR yellow][B]"+hora+"[/B][/COLOR]"
            info = "[COLOR orange][B]"+info+"[/B][/COLOR]"
            title ="[COLOR red][B]"+title+"[/B][/COLOR]"
            encuentro = hora +"--"+title +" "+ info
            
            
            
            itemlist.append( Item(channel=__channel__, title=encuentro,action="enlaces",url = urlparse.urljoin(host,url),thumbnail= thumbnail,extra="live",fulltitle= title,fanart= "http://s6.postimg.org/fs71z0qkx/B9317206944_Z_1_20150503001849_000_GNEAM3_I82_1_0.jpg",folder=True) )
    return itemlist

def enlaces(item):
    logger.info("pelisalacarta.livetv enlaces")
    xbmc.executebuiltin( "Container.Update" )
    if not xbmc.Player().isPlaying():
        xbmc.sleep(20)
        xbmc.executebuiltin('xbmc.PlayMedia('+song+')')
    
    itemlist = []
    data = dhe( scrapertools.cachePage(item.url) )
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    if "<i id=\"whelint\" style=\"line-height: 150%;\">" in data:
        
        if item.extra =="futbol":
           fanart = "http://s6.postimg.org/56n6n0k9d/Wembley.jpg"
        else:
           fanart ="http://s6.postimg.org/naq77nhxt/Sport_Wallpaper_HD_3000x2250.jpg"
        itemlist.append( Item(channel=__channel__, title="[COLOR orangered][B]Las referencias de la transmisión van a ser publicadas no más tarde de media hora de su principio[/B][/COLOR]",thumbnail="http://s6.postimg.org/p3t3vz34h/Panasonic_AJ_HDX900.png",fanart= fanart,folder=False) )
    else:
        if '<span class="lnkt">AceStream Links</span>' in data:
            patronacestream = '<span class="lnkt">AceStream Links</span>(.*?)<a name="comments"></a>'
            matchesacestream = re.compile(patronacestream,re.DOTALL).findall(data)
         
            for bloque_acestream in matchesacestream:
                patron ='<td width=16><img title.*?src="([^"]+)"></a></td>.*?<a href="(acestream:.*?)"'
                matches= re.compile(patron,re.DOTALL).findall(bloque_acestream)
                for idioma, url in matches:
                    #if velocidad == "":
                    #  velocidad = "S/N"
                    
                    itemlist.append( Item(channel=__channel__, title="[COLOR yellow][B]Enlaces Acestream[/B][/COLOR]",action="play",url = url,thumbnail = idioma,fanart ="http://s6.postimg.org/e5hudsej5/Nou_Camp_Stadium_Barcelona_Football_Wallpapers_H.jpg",fulltitle= item.fulltitle,folder=False) )
        else:
             itemlist.append( Item(channel=__channel__, title="[COLOR yellow][B]No hay elaces Acetream[/B][/COLOR]",thumbnail = "http://s6.postimg.org/c2c0jv441/torrent_stream_logo_300x262.png",fanart="http://s6.postimg.org/ttnmybjip/5499731408_42e3876093_b.jpg",folder=False) )
        #Enlaces Sopcast
        if "<span class=\"lnkt\">SopCast Links" in data:
            
            patronsopcast = '<span class="lnkt">SopCast Links</span>(.*?)<a name="comments"></a>'
            matchessopcast = re.compile(patronsopcast,re.DOTALL).findall(data)

            for bloque_sopcast in matchessopcast:
                patron ='<td width=16><img title.*?src="([^"]+)".*?title=.*?>([^<]+)</td>.*?<a href="(sop:.*?)"'
                matches= re.compile(patron,re.DOTALL).findall(bloque_sopcast)
                for idioma,bibrate,url in matches:
                    
                    title = "[COLOR aquamarine][B]Enlace Sopcast[/B][/COLOR]"+" ("+"[COLOR green][B]"+bibrate+"[/B][/COLOR]"+")"
                    itemlist.append( Item(channel=__channel__, title=title,action="play",url = url,thumbnail =idioma,fanart="http://s6.postimg.org/e5hudsej5/Nou_Camp_Stadium_Barcelona_Football_Wallpapers_H.jpg",fulltitle=item.fulltitle,folder=False) )
                        
        else:
    
            itemlist.append( Item(channel=__channel__, title="[COLOR aquamarine][B]No hay elaces Sopcast[/B][/COLOR]",thumbnail ="http://s6.postimg.org/v9z5ggmfl/sopcast.jpg",fanart= "http://s6.postimg.org/ttnmybjip/5499731408_42e3876093_b.jpg",folder=False) )
                        
                        

    return itemlist

def play(item):
    logger.info("pelisalacarta.livetv play")
    itemlist = []

    import xbmc
    xbmc.executebuiltin('xbmc.PlayMedia(Stop)')
    fulltitle= item.fulltitle
    import xbmc
    # Se incluye el título en la url para pasarlo al conector
    url= item.url + "|" + fulltitle
    itemlist.append(Item(channel=__channel__, title=item.title, server="p2p", url=url, action="play", folder=False))

    return itemlist





