# -*- coding: utf-8 -*-
#:-----------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para enlaces a sopcast y acestream
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
from core import logger, config

# Returns an array of possible video url's from the page_url
def get_video_url( page_url , premium = False , user="" , password="" , video_password="" ):
    logger.info("pelisalacarta.servers.p2p server=p2p, la url es la buena " + page_url)

    if page_url.startswith("acestream"):
        mode = "1"
        name = "acestream"
    elif page_url.startswith("sop"):
        mode = "2"
        name = "Sopcast"
    
    if "|" in page_url:
        name = page_url.split("|")[1]
        page_url = page_url.split("|")[0]

    video_data = {
        'plexus' : {
            'url' : "plugin://program.plexus/?url=%s&mode=%s&name=%s" % (page_url, mode, name)
        }
        'p2p-streams' : {
            'url' : "plugin://plugin.video.p2p-streams/?url=%s&mode=%s&name=%s" % (page_url, mode, name)
        }
    }
}
    
    video_urls = []
    
    for plugin, data in sorted(video_data.iteritems()):
        video_urls.append([ "[" + plugin + "] %s" % (name), data['url']])
    
    return video_urls
