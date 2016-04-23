# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para livetv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
import re
from core import scrapertools
from core import logger
from core import config
from core.item import Item
from servers import servertools
import xbmc
__channel__ = "topbongda"
__category__ = "d"
__type__ = "generic"
__title__ = "Topbongda"
__language__ = "ES"

host ="https://topbongda.com/wendy/ajax"
song = os.path.join(config.get_runtime_path()+"/music", 'Easy.mp3')

DEBUG = config.get_setting("debug")

def isGeneric():
    
    return True

#Proxy para acceder a datos ajax
def get_page(url):

    data = scrapertools.cachePage("http://ssl-proxy.my-addr.org/myaddrproxy.php/"+url)
    
    
    return data


def mainlist(item):
    logger.info("pelisalacarta.topbongda mainlist")
    itemlist = []
    
   
    if item.extra != "next_page":
       item.url = "http://topbongda.com/wendy/ajax/home_matches/?page=1"
       xbmc.executebuiltin('xbmc.PlayMedia('+song+')')
    data = get_page(item.url)

    patronmain ='{"current"(.*?)"count"'
    matchesmain = re.compile(patronmain,re.DOTALL).findall(data)

    for bloque_partidos in matchesmain:
        
        patron = '{"begin_at": "(\d+:\d+)".*?"home_team_icon": "//([^"]+)".*?"year": (\d\d\d\d), "slug": "(.*?)",.*?"on_air": (.*?),.*?"mid": (.*?), "away_team_icon": "//([^"]+)".*?"league": "(.*?)".*?"begin_at_date": ".*?, (.*?)".*?"title": "(.*?)"'
        matches=re.compile(patron,re.DOTALL).findall(bloque_partidos)
        
        for hora, thumbnail,year,slug,on_air,mid,fanart,league,date, title  in matches:
            fulltitle = title
            thumbnail = "https://"+thumbnail
            fanart = "https://"+fanart
            time= re.compile('(\d+):(\d+)',re.DOTALL).findall(hora)
            #Corregimos las 5h de diferencia horaria con Vietnam
            for horas, minutos in time:
                if  horas== "00":
                    horas = horas.replace("00","24")
                    #if minutos != "00":
                    dates = re.compile('(\d+)(/\d+/\d+)',re.DOTALL).findall(date)
                    for day, m_y in dates:
                        days = int(day) - 1
                        date = str(days) + m_y
            
                check =re.compile('(\d)\d',re.DOTALL).findall(horas)
                if "0"in check:
                    horas = horas.replace("0","")
                    horas = 24 + int(horas)
                    dates = re.compile('(\d+)(/\d+/\d+)',re.DOTALL).findall(date)
                    for day, m_y in dates:
                        days = int(day) - 1
                        date = str(days) + m_y
            
                wrong_time =int(horas)
                value = 5
                correct_time = wrong_time - value
                correct_time = str(correct_time)
                ok_time = correct_time +":"+ minutos
            if ok_time == "24:00":
               ok_time = "00:00"
               date= day + m_y
            #Cambiamos caracteres Vietnamitas
            if "Ngoại Hạng Anh" in league:
                league = "Premier League"
            if "Hạng Nhất Anh" in league:
                league = "Premier League"
            #Se marca cuando un encuentro está en directo
            if on_air =="true":
               title = "[COLOR chartreuse][B]"+title +"[/B][/COLOR]"+ "[COLOR olivedrab]([/COLOR]"+"[COLOR yellowgreen]"+league+"[/COLOR]"+"[COLOR olivedrab])[/COLOR]"+ " "+"[COLOR crimson][B]LIVE!![/B][/COLOR]"
               url = "http://topbongda.com/wendy/ajax/match_links/?mid=" + mid
            else:
               title ="[COLOR chartreuse]"+ok_time+"[/COLOR]" +"[COLOR olivedrab]--[/COLOR]"+"[COLOR gold]"+date+"[/COLOR]"+" "+"[COLOR seagreen][B]"+title+"[/B][/COLOR]" + "[COLOR olivedrab]([/COLOR]"+"[COLOR yellowgreen]"+league+"[/COLOR]"+"[COLOR olivedrab])[/COLOR]"
               url = "http://topbongda.com/wendy/ajax/match_detail/?slug="+slug+"&year="+year

            itemlist.append( Item(channel=__channel__, title=title,action="enlaces",url = url,thumbnail= thumbnail,fanart=fanart, extra = fulltitle,folder=True) )
        
    #paginación
    current_page_number = int(scrapertools.get_match(item.url,'\?page=(\d+)'))
    next_page_number = current_page_number + 1
    item.url = re.sub(r"\?page=\d+","?page={0}",item.url)
            
    next_page_number = current_page_number + 1
    next_page = item.url.format(next_page_number)
                    
    title= "[COLOR green]Pagina siguiente>>[/COLOR]"
                        
    itemlist.append( Item(channel=__channel__, title=title, url=next_page, fanart="http://s6.postimg.org/bpbkkt8k1/topbongdafansiguiente.jpg", thumbnail="http://s6.postimg.org/qhboyep3l/topbongdasiguiente.png",
                                              action="mainlist",extra="next_page", folder=True) )
    
    
    return itemlist

def enlaces(item):
    logger.info("pelisalacarta.topbongda scraper")
    
    itemlist = []
    
    # Descarga la página
    if "match_detail" in item.url:
        data = get_page(item.url)
        patron = '"week": "(.*?)".*?remaining_seconds": \[(\d+),'
        matches=re.compile(patron,re.DOTALL).findall(data)
        for jornada, remaining in matches:
            no_link="Aun no hay enlaces"
            no_link = no_link.title()
            
            if "Vòng" in jornada:
               jornada = jornada.replace("Vòng","Jornada")
        
            itemlist.append( Item(channel=__channel__,title="[COLOR darkgreen][B]"+jornada+"[/B][/COLOR]"+"    "+"[COLOR forestgreen][B]"+item.extra+"[/B][/COLOR]", url="",action="mainlist",fanart="http://s6.postimg.org/mktb5axsh/topbongdafantime.jpg",thumbnail="http://s6.postimg.org/ippx2qemp/topbongdathumbtime.png", folder=False) )
            itemlist.append( Item(channel=__channel__,title="                          "+"[COLOR springgreen]"+no_link+"[/COLOR]", url="",action="mainlist",fanart="http://s6.postimg.org/mktb5axsh/topbongdafantime.jpg",thumbnail="http://s6.postimg.org/ippx2qemp/topbongdathumbtime.png", folder=False) )
            num=int(remaining)
            dia =(int(num/84600))
            hor=(int(num/3600))
            minu=int((num-(hor*3600))/60)
            seg=num-((hor*3600)+(minu*60))
            if hor >= 24:
               remaining= (str(dia)+" día/s")
            elif hor == 0:
               
               remaining= (str(minu)+"m "+str(seg)+"s")
            else:
               remaining= (str(hor)+"h "+str(minu)+"m "+str(seg)+"s")
            
            itemlist.append( Item(channel=__channel__,title="                                          "+"[COLOR lawngreen]Disponibles en[/COLOR]"+"  "+"[COLOR palegreen][B]"+str(remaining)+"[/B][/COLOR]", url="",action="mainlist",fanart="http://s6.postimg.org/mktb5axsh/topbongdafantime.jpg",thumbnail="http://s6.postimg.org/ippx2qemp/topbongdathumbtime.png", folder=False) )
    else:
       data = get_page(item.url)
       data = re.sub(r'"Flash".*?}','',data)
    
       patron_bloque = '{"name": "(.*?)",.*?(.*?)]]}'
       matchesenlaces = re.compile(patron_bloque,re.DOTALL).findall(data)
       
       if len(matchesenlaces)== 0:
          title ="No hay ningun enlace Sopcast / Acestream".title()
          itemlist.append( Item(channel=__channel__,title="[COLOR limegreen][B]"+title+"[/B][/COLOR]", url="",action="mainlist",fanart="http://s6.postimg.org/unwjdqopd/topbongdafannolink.jpg",thumbnail="http://s6.postimg.org/m6x12tk0h/topbongdathumbnolink.png", folder=False) )
    
       for tipo, bloque_links in matchesenlaces:
        
        
            if tipo == "AceStream":
                tipo = "[COLOR yellow][B]"+tipo+"[/B][/COLOR]"
                thumbnail= "http://s6.postimg.org/c2c0jv441/torrent_stream_logo_300x262.png"
            if tipo == "Sopcast":
                tipo = "[COLOR aquamarine][B]"+tipo+"[/B][/COLOR]"
                thumbnail= "http://s6.postimg.org/v9z5ggmfl/sopcast.jpg"
            itemlist.append( Item(channel=__channel__,title=tipo.strip(), url="",action="mainlist",thumbnail=thumbnail, fanart= "http://s6.postimg.org/phle2p9xr/topbongdafanmatch.jpg",folder=False) )
            patron ='\["(.*?)",.*?, "(.*?)"'
            matches=re.compile(patron,re.DOTALL).findall(bloque_links)
            for link, idioma in matches:
                
                if "sop" in link:
                   thumbnail="http://s6.postimg.org/v9z5ggmfl/sopcast.jpg"
                if "acestream" in link:
                   thumbnail="http://s6.postimg.org/c2c0jv441/torrent_stream_logo_300x262.png"
                title = idioma.strip()
                title = "[COLOR darkolivegreen][B]"+title+"[/B][/COLOR]"
                itemlist.append( Item(channel=__channel__, title="        "+title,action="play",url =link,thumbnail= thumbnail,fanart="http://s6.postimg.org/phle2p9xr/topbongdafanmatch.jpg",extra = item.extra, folder=True) )


    return itemlist



def play(item):
    logger.info("pelisalacarta.topbongda play")
    itemlist = []
    import xbmc
    xbmc.executebuiltin('xbmc.PlayMedia(Stop)')
    fulltitle = "[COLOR palegreen][B]"+item.extra+"[/B][/COLOR]"
    # Se incluye el título en la url para pasarlo al conector
    url= item.url + "|" + fulltitle
    
    itemlist.append(Item(channel=__channel__, title=item.title, server="p2p", url=url, action="play", folder=False))
    
    return itemlist





