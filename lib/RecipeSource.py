from urllib.parse import urlparse
import re

sources_by_host = {
    "bonappetit.com" : "Bon Appétit",
}

def get_source_by_name(url):
    hostname = urlparse(url).netloc
    if re.match("www\.", hostname):
        hostname = hostname[4:]

    if hostname in sources_by_host:
        return sources_by_host[hostname]
    else:
        return None