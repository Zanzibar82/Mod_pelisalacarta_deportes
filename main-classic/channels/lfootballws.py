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
import xbmc
import xbmcgui
from core.item import Item
from servers import servertools
from core.scrapertools import decodeHtmlentities as dhe
import random
import time

__channel__ = "lfootballws"
__category__ = "d"
__type__ = "generic"
__title__ = "Lfootballws"
__language__ = "ES"
song = os.path.join(config.get_runtime_path(), 'queen-we-will-rock-you.mp3')
host ="http://lfootball.ws/"
DEBUG = config.get_setting("debug")

def isGeneric():
    
    return True



def mainlist(item):
    logger.info("pelisalacarta.lfootballws lista")
    itemlist = []
    import xbmc, time
    
    xbmc.executebuiltin('Notification([COLOR crimson][B]BIENVENIDOS A...[/B][/COLOR], [COLOR yellow][B]'+'livefootballws'.upper()+'[/B][/COLOR],4000,"http://4.bp.blogspot.com/-Jtkwjc049c0/T7CKiNujy-I/AAAAAAAARPc/llNdvg_8TWk/s1600/football_128x128.png")')
    xbmc.executebuiltin("Container.Update")
    
    check =xbmc.getInfoLabel('Container.FolderPath')
    if "channelselector" in check:
        xbmc.executebuiltin('xbmc.PlayMedia('+song+')')

    
    """
        Lo que ocurre con
        url = http://translate.googleusercontent.com/translate_c?depth=1&nv=1&rurl=translate.google.com&sl=ru&tl=es&u=http://lfootball.ws/&usg=ALkJrhgzJfI1TDn3BxGgPbjgAHHS7J0i9g
        Redirecciones:
        1. http://translate.google.com/translate?depth=1&nv=1&rurl=translate.google.com&sl=ru&tl=es&u=http://lfootball.ws/
        2. http://translate.googleusercontent.com/translate_p?nv=1&rurl=translate.google.com&sl=ru&tl=es&u=http://lfootball.ws/&depth=2&usg=ALkJrhgAAAAAVupk4tLINTbmU7JrcQdl0G4V3LtnRM1n
        3. http://translate.googleusercontent.com/translate_c?depth=2&nv=1&rurl=translate.google.com&sl=ru&tl=es&u=http://lfootball.ws/&usg=ALkJrhhhRDwHSDRDN4t27cX5CYZLFFQtmA
        Lo que significa que necesitamos una key nueva cada vez en el argumento "usg" y para llegar a la url 3 debemos hacer la petición 1 y 2 con 'follow_redirects=False' o con la convinación de 'follow_redirects=False' y 'header_to_get="location"'
        """
    
    #### Opción 1: 'follow_redirects=False'
    ## Petición 1
    url = "http://translate.google.com/translate?depth=1&nv=1&rurl=translate.google.com&sl=ru&tl=es&u=http://lfootball.ws/"
    data = dhe( scrapertools.downloadpage(url,follow_redirects=False) )#.decode('cp1251').encode('utf8')
    ## Petición 2
    url = scrapertools.get_match(data, ' src="([^"]+)" name=c ')
    data = dhe( scrapertools.downloadpage(url,follow_redirects=False) )#.decode('cp1251').encode('utf8')
    ## Petición 3
    url = scrapertools.get_match(data, 'URL=([^"]+)"')
    data = dhe( scrapertools.cachePage(url) )#.decode('cp1251').encode('utf8')
    
    """
        #### Opción 2: 'follow_redirects=False' y 'header_to_get="location"'
        ## Petición 1
        url = "http://translate.google.com/translate?depth=1&nv=1&rurl=translate.google.com&sl=ru&tl=es&u=http://lfootball.ws/"
        data = dhe( scrapertools.downloadpage(url,follow_redirects=False) )#.decode('cp1251').encode('utf8')
        ## Petición 2
        url = scrapertools.get_match(data, ' src="([^"]+)" name=c ')
        url = scrapertools.get_header_from_response(url, header_to_get="location")
        ## Petición 3
        data = dhe( scrapertools.cachePage(url ) )#.decode('cp1251').encode('utf8')
        """
    
    
    
    #a:
    
    patronmain ='transmisión en vivo(.*?)<h3 class=sectionName> '
    matchesmain = re.compile(patronmain,re.DOTALL).findall(data)
    for main in matchesmain:
        print "liveeee"
        print main
        patron = '<img class=img src=(.*?) alt.*?<img class=img src=(.*?) alt.*?<a class=link href=.*?&u=.*?href.*?&u=(.*?)&usg.*?title="(.*?)"'#'<a class="link" href="([^"]+)" title="(.*?)".*?<span class="liga"><span>(.*?)</span></span>.*?<span class="date"><span>(.*?)</span></span>'
        matches = re.compile(patron,re.DOTALL).findall(main)
        for thumbnail, fanart,url,title in matches:
            #liga = re.sub(r'<span.*?">|</span>|class=.*?>|<span>.*?<span|<span.*?|>|<a.*?','',liga)
            #if "и" in liga:
            #   liga = "La liga"
    
            
            
            
            #info = "("+liga+")"
            title = "[COLOR chocolate][B]"+title +"[/B][/COLOR]" +" "+ "[COLOR crimson][B]EN VIVO!![/B][/COLOR]"
            print "lolo"
            print title
            print url
            itemlist.append( Item(channel=__channel__, title=title,action="enlaces",url=url,thumbnail =urlparse.urljoin(host,thumbnail),fanart =urlparse.urljoin(host,fanart),fulltitle = title,folder=True) )

    #b
    patronmain ='nuestra(.*?)partido'
    matchesmain = re.compile(patronmain,re.DOTALL).findall(data)
    print "ojuuu"
    print matchesmain
    
    
    for main in matchesmain:
    
        patron = '<img class=img src=([^"]+) alt.*?src=([^"]+) '
        patron +='.*?<a class=link href=.*?&u=.*?href.*?&u=([^"]+)&usg.*?'
        patron +='title="([^<]+)".*?'
        patron +='<span class="nameCon clear">(.*?)</li><li class=fl>'
        
        matches = re.compile(patron,re.DOTALL).findall(main)
        if len(matches)==0 :
           itemlist.append( Item(channel=__channel__, title="[COLOR orange][B]No hay encuentros previstos en estos momentos[/B][/COLOR]",thumbnail ="http://s6.postimg.org/619q91s41/comingsoon.png",fanart ="http://s6.postimg.org/7ucmxddap/soccer_field_desktop_20150703154119_5596ad1fde3e.jpg") )
        for thumbnail, fanart, url,title,liga_fecha in matches:
            print "zorro"
            print liga_fecha
            #liga = re.sub(r'<span.*?">|</span>|class=.*?>|<span>.*?<span|<span.*?|>|<a.*?','',liga)
            try:
                liga = scrapertools.get_match(liga_fecha,'<span class=liga><span>([^<]+)')
                liga = re.sub(r'de','',liga)
                fecha = re.sub(r'<span class=liga><span>.*?</span></span>|<span class="name fl"><span>.*?</span></span></span>|<span class=dopCon>.*?<span class=date><span>|<span class=date><span>|</span>|</a>|de|,|','',liga_fecha)
            except:
                liga=""
                
                fecha = scrapertools.get_match(liga_fecha,'<span class=dopCon><span class=date><span>([^<]+)</span>')
            if "taza" in liga:
                liga="Cup"

            print "perraco"
            if "00:" in fecha:
               fecha = fecha.replace("00:","24:")
               print fecha
            info = "("+liga+")"
            time= re.compile('(\d+):(\d+)',re.DOTALL).findall(fecha)
            for horas, minutos in time:
                
                print "horas"
                print horas
                wrong_time =int(horas)
                value = 2
                correct_time = wrong_time - value
                correct_time = str(correct_time)
                ok_time = correct_time +":"+ minutos
                fecha = re.sub(r'(\d+):(\d+)|el|de|,|<span class="nameCon clear">','',fecha).strip()
                
                print "joder"
                print fecha
                d_m = re.compile('([^<]+) (\d+)',re.DOTALL).findall(fecha)
                print "opcion a"
                print d_m
                if len(d_m)==0 :
                    d_m = re.compile('(\d+) ([^<]+)',re.DOTALL).findall(fecha)
                    print "pasa a opcion b"
                for x, y in d_m:
                    if x.isdigit():
                       print "opcion x=numero"
                       dia = x.strip()
                       mes = y.strip()
                    else:
                       print "opcion x = letras"
                       print d_m
                       mes = x.strip()
                       dia = y.strip()
    
                    dia_mes = (dia+" "+mes).title()
                    partido = "[COLOR khaki][B]"+dia_mes+"[/B][/COLOR]" +"[COLOR yellow][B]"+" "+ok_time+"[/B][/COLOR]"+"--"+"[COLOR chocolate][B]"+title +"[/B][/COLOR]"+" "+"[COLOR lightslategray]"+ info +"[/COLOR]"
                    
                    itemlist.append( Item(channel=__channel__, title=partido,action="enlaces",url=url,thumbnail =urlparse.urljoin(host,thumbnail),fanart =urlparse.urljoin(host,fanart), fulltitle= "[COLOR chocolate][B]"+title +"[/B][/COLOR]", folder=True) )
        

    
    
    return itemlist

def enlaces(item):
    logger.info("pelisalacarta.livetv enlaces")
    itemlist = []

    import xbmc
    if not xbmc.Player().isPlaying():
       xbmc.executebuiltin('xbmc.PlayMedia('+song+')')
   
    data = dhe( scrapertools.cachePage(item.url) ).decode('cp1251').encode('utf8')
    

    patronenlaces =' <table class="live-table">(.*?)<h1 class="sectionName">'
    matchesenlaces = re.compile(patronenlaces,re.DOTALL).findall(data)
    if len(matchesenlaces)==0:
        try:
            check= scrapertools.get_match(data,'<div class="CD_text">Событие завершено</div>')
            title = "Partido finalizado".title()
            itemlist.append( Item(channel=__channel__, title="[COLOR bisque][B]"+title+"[/B][/COLOR]",thumbnail =item.thumbnail, fanart= item.fanart, folder=False) )
        except:
            title = "Los enlaces aparecerán media hora antes del encuentro".title()
            itemlist.append( Item(channel=__channel__, title="[COLOR orange][B]"+title+"[/B][/COLOR]",thumbnail =item.thumbnail, fanart="http://s6.postimg.org/nmba7vde9/wallpaper_football_warsaw_stadium_national_hobbi.jpg", folder=False) )


    for bloque_enlaces in matchesenlaces:
        patron = '<a href=.*?<a href=".*?".*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<a href="(.*?)"'
        matches = re.compile(patron,re.DOTALL).findall(bloque_enlaces)
        
        for velocidad,canal,url in matches:
            print "lobo"
            print url
            if "sop" in url:
                player= "[COLOR deepskyblue][B]Sopcast[/B][/COLOR]"
            else :
                player = "[COLOR palegreen][B]Acestream[/B][/COLOR]"
            title = "[COLOR mediumorchid][B]"+canal+"[/B][/COLOR]" +" "+"("+player+")"+" "+"("+"[COLOR moccasin][B]"+velocidad+"[/B][/COLOR]"+")"
            itemlist.append( Item(channel=__channel__, title=title,action="play",url = url,thumbnail =item.thumbnail, fanart= "http://s6.postimg.org/plrvza7pr/Snchez_Pizjun_Borussia_opt.jpg", extra ="saliendo",fulltitle = item.fulltitle,folder=False) )

    return itemlist

def play(item):
    logger.info("pelisalacarta.lfootballws play")
    itemlist = []
    import xbmc
    xbmc.executebuiltin('xbmc.PlayMedia(Stop)')
    fulltitle = item.fulltitle
    # Se incluye el título en la url para pasarlo al conector
    url= item.url + "|" + fulltitle
    
    itemlist.append(Item(channel=__channel__, title=item.title, server="p2p", url=url, action="play", folder=False))
    
    return itemlist










