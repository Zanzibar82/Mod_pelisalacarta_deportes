# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal de configuración
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import os, time

from core import config
from core import jsontools
from core import logger
from core import scrapertools
from core.item import Item

DEBUG = True
CHANNELNAME = "update_sports"
REMOTE_VERSION_FILE = "https://raw.githubusercontent.com/CmosGit/Mod_pelisalacarta_deportes/master/actualizador/update_sports.xml"
LOCAL_XML_FILE = os.path.join(config.get_runtime_path() , 'channels', "update_sports.xml" )

def isGeneric():
    return True


def mainlist(item):
    logger.info("pelisalacarta.channels.configuracion mainlist")

    itemlist = []
    actualizar, version1, version2, message = check()
    if actualizar:
        title = "[COLOR darkorange]Nueva actualización: v"+version1+" a v"+version2+"[/COLOR]"
        itemlist.append(Item(channel=CHANNELNAME, title=title, action="", thumbnail=item.thumbnail, folder=False))
        title = "[COLOR green]Cambios: "+message+"[/COLOR]"
        itemlist.append(Item(channel=CHANNELNAME, title=title, action="", thumbnail=item.thumbnail, folder=False))
    else:
        itemlist.append(Item(channel=CHANNELNAME, title="[COLOR darkorange]Ninguna actualización disponible[/COLOR]", action="", thumbnail=item.thumbnail, folder=False))

    itemlist.append( Item(channel=CHANNELNAME, title="Actualizar todo", action="actualiza", select="all", thumbnail=item.thumbnail, folder=False) )
    itemlist.append( Item(channel=CHANNELNAME, title="Actualizar channelselector", action="actualiza", select="channelselector", thumbnail=item.thumbnail, folder=False) )
    itemlist.append( Item(channel=CHANNELNAME, title="Actualizar servertools", action="actualiza", select="server", thumbnail=item.thumbnail, folder=False) )

    return itemlist


def actualiza(item):
    logger.info("pelisalacarta.channels.configuracion actualiza")
    logger.info("pelisalacarta.core.configuracion url=%s" % item.url)

    error = False
    if item.select == "server":
        filename = os.path.join(config.get_runtime_path(), 'servers', 'servertools.py')
        url = "https://raw.githubusercontent.com/CmosGit/Mod_pelisalacarta_deportes/master/main-classic/servers/servertools.py"
        error = do_download(url, filename)
        if error:
            dialog_notification("Error", "Se ha producido un error en la actualización de los archivos")
        else:
            dialog_notification("Éxito", "Actualizado correctamente servertools.py")
    elif item.select == "channelselector":
        filename = os.path.join(config.get_runtime_path(), 'channelselector.py')
        url = "https://raw.githubusercontent.com/CmosGit/Mod_pelisalacarta_deportes/master/main-classic/channelselector.py"
        error = do_download(url, filename)
        if error:
            dialog_notification("Error", "Se ha producido un error en la actualización de los archivos")
        else:
            dialog_notification("Éxito", "Actualizado correctamente channelselector.py")
    else:
        url = "https://api.github.com/repos/CmosGit/Mod_pelisalacarta_deportes/git/trees/master?recursive=1"
        data = scrapertools.cachePage(url)
        data = jsontools.load_json(data)
        count = 0
        for child in data["tree"]:
            if not child["path"].startswith("main-classic"): continue
            if child["type"] == "blob":
                url = "https://raw.githubusercontent.com/CmosGit/Mod_pelisalacarta_deportes/master/" + child["path"]
                filename = os.path.join(config.get_runtime_path(), child["path"].replace("/","\\"))
                filename = filename.replace("\\main-classic","")
                error_download = do_download(url, filename)
                if error_download: error = True
                count += 1

        url = "https://raw.githubusercontent.com/CmosGit/Mod_pelisalacarta_deportes/master/actualizador/update_sports.xml"
        error = do_download(url,LOCAL_XML_FILE)
        count += 1

        if error:
            dialog_notification("Error", "Se ha producido un error en la actualización de los archivos")
        else:
            dialog_notification("Actualizado correctamente", str(count)+" archivos actualizados")
        

def do_download(url, localfilename):
    logger.info("pelisalacarta.core.configuracion localfilename=%s" % localfilename)
    logger.info("pelisalacarta.core.configuracion descarga fichero...")
    inicio = time.clock()
    
    error = False
    try:
        os.remove(localfilename)
    except:
        pass

    try:
        from core import downloadtools
        downloadtools.downloadfile(url, localfilename, continuar=True)
    except:
        error = True
        pass
    
    fin = time.clock()
    logger.info("pelisalacarta.core.configuracion Descargado en %d segundos " % (fin-inicio+1))
    return error


def check():
    data = scrapertools.cachePage(REMOTE_VERSION_FILE)
    version_publicada = scrapertools.find_single_match(data,"<version>([^<]+)</version>").strip()
    message = scrapertools.find_single_match(data,"<changes>([^<]+)</changes>").strip()

    # Lee el fichero con la versión instalada
    file = open(LOCAL_XML_FILE)
    data = file.read()
    file.close()
    version_local = scrapertools.find_single_match(data,"<version>([^<]+)</version>").strip()
    if float(version_publicada) > float(version_local):
        return True, version_publicada, version_local, message
    else:
        return False, "", "", ""


def dialog_notification(heading, message, icon=0, time=5000, sound=True):
    import xbmcgui
    dialog = xbmcgui.Dialog()
    l_icono=(xbmcgui.NOTIFICATION_INFO , xbmcgui.NOTIFICATION_WARNING, xbmcgui.NOTIFICATION_ERROR)
    dialog.notification (heading, message, l_icono[icon], time, sound)