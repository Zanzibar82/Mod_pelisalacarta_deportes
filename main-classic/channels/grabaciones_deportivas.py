# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para Grabaciones Deportivas
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
from core import logger
from core import config
from core import scrapertools
from core.item import Item


__channel__ = "grabaciones_deportivas"
__type__ = "generic"
__title__ = "Grabaciones Deportivas"
__language__ = "ES"

DEBUG = config.get_setting("debug")
host_live = "http://livetv.sx"
headers = [['User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0']]

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.channels.grabaciones_deportivas mainlist")
    itemlist = []
    itemlist.append(Item(channel=__channel__, title="Live TV (Todos los deportes)" , action="livetv", thumbnail="http://i.imgur.com/u0IFWnQ.png?1", fanart="http://i.imgur.com/jR13N33.jpg"))
    itemlist.append(Item(channel="footballia", title="Footballia (Fútbol de todas las épocas)" , action="mainlist", thumbnail="http://i.imgur.com/VOHOvWD.png", fanart="http://i.imgur.com/1fiynYf.jpg"))
    itemlist.append(Item(channel="fullmatches", title="Full Matches & Shows (Solo Fútbol)" , action="mainlist", thumbnail="http://i.imgur.com/W7rO4y0.png", fanart="http://i.imgur.com/jR13N33.jpg"))
    itemlist.append(Item(channel="hemerotecanba", title="La Hemeroteca NBA (Fútbol, NFL, NCAA y más...)" , action="mainlist", thumbnail="http://i.imgur.com/Vit5mac.png", fanart="http://i.imgur.com/REZiwru.jpg"))
    itemlist.append(Item(channel="fullmatchtv", title="FullMatchTV (Fútbol, NBA, NFL...)" , action="mainlist", thumbnail="http://i.imgur.com/h00Z6L0.png", fanart="http://i.imgur.com/RByzN1j.jpg"))
    itemlist.append(Item(channel="sportvideo", title="Sport-Video (Torrent - NBA, Fútbol, NHL...)" , action="mainlist", thumbnail="http://i.imgur.com/BeCuQqm.png", fanart="http://i.imgur.com/dMEhXWP.jpg?1"))
    itemlist.append(Item(channel="socceryou", title="SoccerYou (Solo Fútbol)" , action="mainlist", thumbnail="http://i.imgur.com/0bHYHXp.png", fanart="http://i.imgur.com/1fiynYf.jpg"))

    return itemlist

def livetv(item):
    logger.info("pelisalacarta.channels.grabaciones_deportivas livetv")
    itemlist = []
    itemlist.append(Item(channel=__channel__, title="Fútbol" , action="entradas", url="http://livetv.sx/es/video/", thumbnail=item.thumbnail, fanart=item.fanart))
    itemlist.append(Item(channel=__channel__, title=bbcode_kodi2html("[COLOR gold]+++ Liga BBVA[/COLOR]") , action="torneo", url="http://livetv.sx/es/videotourney/15/", thumbnail=item.thumbnail, fanart=item.fanart))
    itemlist.append(Item(channel=__channel__, title=bbcode_kodi2html("[COLOR gold]+++ Premier League[/COLOR]") , action="torneo", url="http://livetv.sx/es/videotourney/1/", thumbnail=item.thumbnail, fanart=item.fanart))
    itemlist.append(Item(channel=__channel__, title="Baloncesto"      , action="entradas", url="http://livetv.sx/es/video/", thumbnail=item.thumbnail, fanart=item.fanart))
    itemlist.append(Item(channel=__channel__, title=bbcode_kodi2html("[COLOR gold]+++ NBA[/COLOR]") , action="torneo", url="http://livetv.sx/es/videotourney/3/", thumbnail=item.thumbnail, fanart=item.fanart))
    itemlist.append(Item(channel=__channel__, title=bbcode_kodi2html("[COLOR gold]+++ ACB[/COLOR]") , action="torneo", url="http://livetv.sx/es/videotourney/215/", thumbnail=item.thumbnail, fanart=item.fanart))
    itemlist.append(Item(channel=__channel__, title="Otros Deportes"      , action="cat", url="http://livetv.sx/es/video/", thumbnail=item.thumbnail, fanart=item.fanart))
    itemlist.append(Item(channel=__channel__, title="Competiciones"      , action="competiciones", url="http://livetv.sx/es/video/", thumbnail=item.thumbnail, fanart=item.fanart))
    itemlist.append(Item(channel=__channel__, title="Buscar..."      , action="search", thumbnail=item.thumbnail))
    return itemlist

#######Sección Live TV
def search(item,texto):
    logger.info("pelisalacarta.channels.grabaciones_deportivas search")
    itemlist = []
    item.url = "http://livetv.sx/es/videosearch/?q=" + texto
    return partidos(item)


def entradas(item):
    logger.info("pelisalacarta.channels.grabaciones_deportivas entradas")
    itemlist = []
    data = scrapertools.cachePage(item.url)
    data = scrapertools.decodeHtmlentities(data)
    title = item.title.replace("+++ ","")
    ymd = scrapertools.find_single_match(data, '<div id="vafs".*?value="([^"]+)"')
    cat = scrapertools.find_single_match(data, '<label for="s([^"]+)">(?:<b>|)'+title+'(?:</b>|)</label>')

    item.extra = cat
    item.url = item.url + ymd
    itemlist = partidos(item)

    if itemlist[0].action== "": return itemlist
    if not "Primer día con vídeos disponibles" in itemlist[0].title: itemlist.insert(0, Item(channel=__channel__, title="--Hoy--", url="", action="", thumbnail=item.thumbnail, folder=False)) 
    itemlist.append(Item(channel=__channel__, title=bbcode_kodi2html("     [COLOR red]***Elegir Fecha***[/COLOR]"), url="", action="", thumbnail=item.thumbnail, folder=False))
    matches = scrapertools.find_multiple_matches(data, '<a class="small"href="([^"]+)".*?<b>(.*?)</b>')
    length = len(itemlist)
    for scrapedurl, scrapedtitle in matches:
        if scrapedtitle == "Hoy": continue
        scrapedurl = host_live + scrapedurl
        itemlist.insert(length, Item(channel=__channel__, title=scrapedtitle, url=scrapedurl, action="partidos", extra=cat, thumbnail=item.thumbnail, folder=True))

    calendar = scrapertools.cachePage("http://livetv.sx/ajax/vacal.php?cal&lng=es")
    matches = scrapertools.find_multiple_matches(calendar, "load\('([^']+)'\).*?<b>(.*?)</b>")
    for scrapedurl, scrapedtitle in matches:
        scrapedurl = host_live + scrapedurl
        itemlist.append(Item(channel=__channel__, title=scrapedtitle, url=scrapedurl, action="calendario", extra=cat, thumbnail=item.thumbnail, folder=True))

    return itemlist

def cat(item):
    logger.info("pelisalacarta.channels.grabaciones_deportivas cat")
    itemlist = []
    data = scrapertools.cachePage(item.url)
    data = scrapertools.decodeHtmlentities(data)
    matches = scrapertools.find_multiple_matches(data, '<label for="s.*?">(.*?)</label>')
    
    for scrapedtitle in matches:
        scrapedtitle = scrapertools.htmlclean(scrapedtitle)
        itemlist.append(Item(channel=__channel__, title=scrapedtitle, url=item.url, action="entradas", thumbnail=item.thumbnail, folder=True))

    return itemlist

def partidos(item):
    logger.info("pelisalacarta.channels.grabaciones_deportivas partidos")
    itemlist = []
    cookie_param = "vas="+item.extra
    headers.append(['Cookie',cookie_param])
    data = scrapertools.downloadpage(item.url, headers=headers).replace("\n","").replace("\t","")
    data = scrapertools.decodeHtmlentities(data)

    novideos = scrapertools.find_single_match(data, '<a href="([^"]+)">Pasar a la.*?fecha con videos disponibles')
    if novideos != "":
        scrapedurl = host_live + novideos
        date = scrapertools.find_single_match(novideos.rsplit("/",2)[1], '(\d{4})(\d{2})(\d{2})')
        scrapedtitle = "Primer día con vídeos disponibles: {0}/{1}/{2}".format(date[2], date[1], date[0])
        itemlist.append(Item(channel=__channel__, title=scrapedtitle, action="partidos", url=scrapedurl, extra=item.extra, thumbnail=item.thumbnail, folder=True))
        return itemlist
    elif "Intente aumentar o eliminar el filtro" in data:
        itemlist.append(Item(channel=__channel__, title="Categoría sin vídeos", action="", url="", thumbnail=item.thumbnail, folder=False))	
        return itemlist

    torneos = scrapertools.find_multiple_matches(data, '<td width=32.*?src="([^"]+)".*?<a class="main" href="([^"]+)"><b>(.*?)</b></a>')
    for thumbnail, url, title in torneos:
        scrapedurl = host_live + url
        itemlist.append(Item(channel=__channel__, title=bbcode_kodi2html("     [COLOR gold]***"+title+"***[/COLOR]"), url=scrapedurl, action="torneo", thumbnail=thumbnail, folder=True))
        bloque = scrapertools.find_single_match(data, '(<b>'+title+'</b></a>.*?(?:a class="main"|span class="whitetitle"))')

        matches = scrapertools.find_multiple_matches(bloque, '<td width=(?:16|40).*?(?:href="([^"]+)".*?</td>|</b>.*?</td>).*?<b>(.*?)</b>.*?</td>')
        count = 0
        for scrapedurl, scrapedtitle in matches:
            if scrapedurl == "": continue
            scrapedurl = host_live + scrapedurl
            count += 1
            itemlist.append(Item(channel=__channel__, title=scrapedtitle, url=scrapedurl, action="videos", thumbnail=thumbnail, folder=True))
        if count == 0:
            matches = scrapertools.find_multiple_matches(bloque, '<td width=(?:16|40).*?width="30%">.*?<b>(.*?)<\/b>.*?Video del partido.*?<a class="small" href="([^"]+)">')
            if len (matches) == 0: matches = scrapertools.find_multiple_matches(bloque, '<td width=(?:16|40).*?width="30%">.*?<b>(.*?)<\/b>.*?<a class="small" href="([^"]+)">')
            for scrapedtitle, scrapedurl in matches:
                scrapedurl = host_live + scrapedurl
                itemlist.append(Item(channel=__channel__, title=scrapedtitle, url=scrapedurl, action="findvideos", thumbnail=thumbnail, folder=True))
    return itemlist

def videos(item):
    logger.info("pelisalacarta.channels.grabaciones_deportivas videos")
    itemlist = []
    data = scrapertools.cachePage(item.url)
    data = scrapertools.decodeHtmlentities(data)

    matches = scrapertools.find_multiple_matches(data, '<a alt="([^"]+)" href="([^"]+)".*?src="([^"]+)"')
    goles = False
    for scrapedtitle, scrapedurl, scrapedthumbnail in matches:
        if ":" in scrapedtitle and item.title != "Mostrar Goles":
            goles = True
            continue
        scrapedurl = host_live + scrapedurl
        scrapedtitle = scrapedtitle.replace("Long Highlights","Resumen").replace("Highlights","Mejores Jugadas").replace("Full Match Record","Partido/Evento Completo")
        if not scrapedthumbnail.startswith("http"): scrapedthumbnail = "http:"+scrapedthumbnail
        itemlist.append(Item(channel=__channel__, title=bbcode_kodi2html("[COLOR green]"+scrapedtitle+"[/COLOR]"), url=scrapedurl, action="findvideos", thumbnail=scrapedthumbnail, folder=True))

    if item.title != "Mostrar Goles" and goles:
        itemlist.append(Item(channel=__channel__, title="Mostrar Goles", url=item.url, action="videos", folder=True))

    return itemlist

def calendario(item):
    logger.info("pelisalacarta.channels.grabaciones_deportivas calendario")
    itemlist = []
    data = scrapertools.cachePage(item.url)

    matches = scrapertools.find_multiple_matches(data, "load\('([^']+)'\).*?<b>(.*?)</b>")
    if len (matches) == 0: matches = scrapertools.find_multiple_matches(data, '<a href="([^"]+)">(.*?)</a>')
    for scrapedurl, scrapedtitle in matches:
        if "video" in scrapedurl: action = "partidos"
        else: action = "calendario"
        scrapedurl = host_live + scrapedurl
        scrapedtitle += " de "+item.title
        itemlist.insert(0, Item(channel=__channel__, title=scrapedtitle, url=scrapedurl, action=action, extra=item.extra, thumbnail=item.thumbnail, folder=True))

    return itemlist

def competiciones(item):
    logger.info("pelisalacarta.channels.grabaciones_deportivas competiciones")
    itemlist = []
    data = scrapertools.cachePage(item.url).replace("\n","").replace("\t","")
    data = scrapertools.decodeHtmlentities(data)
    if item.title == "Competiciones":
        matches = scrapertools.find_multiple_matches(data, '<td colspan=4.*?>\s+<span class="whitetitle">(.*?)</span>')
        for scrapedtitle in matches:
            itemlist.append(Item(channel=__channel__, title=scrapedtitle, action="competiciones", url=item.url, thumbnail=item.thumbnail, folder=True))
    else:
        bloques = scrapertools.find_multiple_matches(data, '(<span class="whitetitle">'+item.title+'</span>.*?(?:<span class="whitetitle"|<i>))')
        for bloque in bloques:
            matches = scrapertools.find_multiple_matches(bloque, '<label for="c([^"]+)">(.*?)</label>')
            for cat, scrapedtitle in matches:
                scrapedurl = host_live + "/es/videotourney/"+cat+"/"
                itemlist.append(Item(channel=__channel__, title=scrapedtitle, action="torneo", url=scrapedurl, thumbnail=item.thumbnail, folder=True))

    return itemlist


def torneo(item):
    logger.info("pelisalacarta.channels.grabaciones_deportivas torneo")
    itemlist = []
    data = scrapertools.cachePage(item.url).replace("\n","").replace("\t","")
    data = scrapertools.decodeHtmlentities(data)

    thumbnail = scrapertools.find_single_match(data,'<img width=37 src="([^"]+)"')
    dia = scrapertools.find_multiple_matches(data, '<td width=22.*?<b>(.*?)</b>')
    for title in dia:
        itemlist.append(Item(channel=__channel__, title="     [COLOR gold]***"+title+"***[/COLOR]", url="", action="", thumbnail=thumbnail, folder=False))
        bloque = scrapertools.find_single_match(data, '(<b>'+title+'</b>.*?(?:<td width=22|span class="whitetitle"))')

        matches = scrapertools.find_multiple_matches(bloque, '<td width=(?:16|40).*?(?:href="([^"]+)".*?</td>|</b>.*?</td>).*?<b>(.*?)</b>.*?</td>')
        count = 0
        for scrapedurl, scrapedtitle in matches:
            if scrapedurl == "": continue
            scrapedurl = host_live + scrapedurl
            count += 1
            itemlist.append(Item(channel=__channel__, title=scrapedtitle, url=scrapedurl, action="videos", thumbnail=thumbnail, folder=True))

        if count == 0:
            matches = scrapertools.find_multiple_matches(bloque, '<td width=(?:16|40).*?width="30%">.*?<b>(.*?)<\/b>.*?Video del partido.*?<a class="small" href="([^"]+)">')
            if len (matches) == 0: matches = scrapertools.find_multiple_matches(bloque, '<td width=(?:16|40).*?width="30%">.*?<b>(.*?)<\/b>.*?<a class="small" href="([^"]+)">')
            for scrapedtitle, scrapedurl in matches:
                scrapedurl = host_live + scrapedurl
                itemlist.append(Item(channel=__channel__, title=scrapedtitle, url=scrapedurl, action="findvideos", thumbnail=thumbnail, folder=True))

    itemlist.append(Item(channel=__channel__, title="     [COLOR red]***Elegir Fecha***[/COLOR]", url="", thumbnail=item.thumbnail, folder=False))
    matches = scrapertools.find_multiple_matches(data, '<td align="center"><a href="([^"]+)">(.*?)</a>')
    for scrapedurl, scrapedtitle in matches:
        scrapedurl = host_live + scrapedurl
        year = scrapedurl.rsplit("/",2)[1]
        year = year[:4]
        scrapedtitle += " de "+year
        itemlist.append(Item(channel=__channel__, title=scrapedtitle, url=scrapedurl, action="torneo", thumbnail=item.thumbnail, folder=True))

    matches = scrapertools.find_multiple_matches(data, '<tr><td><a href="([^"]+)">(\d+)</td></td>')
    length = len(itemlist)
    for scrapedurl, scrapedtitle in matches:
        scrapedurl = host_live + scrapedurl
        scrapedurl = scrapertools.find_single_match(scrapedurl,"(http.*?\d{4})") + "12/"
        itemlist.insert(length, Item(channel=__channel__, title=scrapedtitle, url=scrapedurl, action="torneo", thumbnail=item.thumbnail, folder=True))

    return itemlist


def bbcode_kodi2html(text):
    if config.get_platform().startswith("plex") or config.get_platform().startswith("mediaserver"):
        import re
        text = re.sub(r'\[COLOR\s([^\]]+)\]',
                      r'<span style="color: \1">',
                      text)
        text = text.replace('[/COLOR]','</span>')
        text = text.replace('[CR]','<br>')
        text = re.sub(r'\[([^\]]+)\]',
                      r'<\1>',
                      text)
        text = text.replace('"color: white"','"color: auto"')

    return text