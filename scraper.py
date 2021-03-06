# coding=utf-8

import scraperwiki
import lxml.html
import sqlite3
import re

BASE_URL = 'http://www.hcdmza.gob.ar/web/institucional/bloques.html'

html = scraperwiki.scrape(BASE_URL)
ssRoot = lxml.html.fromstring(html)

PARTY_MAP = {
    'UCR': u'Unión Cívica Radical',
    'PJ': 'Partido Justicialista',
    'PTS-FIT': 'Partido de los Trabajadores Socialistas/FIT',
    'FIT-PTS': 'Partido de los Trabajadores Socialistas/FIT',
    'FIT': 'FIT',
    'PD': u'Partido Demócrata',
    'FR': 'Frente Renovador',
    'PRO': 'PRO'
}

# There seems to be a broken slideshow, but it contains useful data!
members = ssRoot.cssselect('div.camera_caption')
parsedMembers = []

for member in members:

    memberData = {}

    memberData['name'] = member.cssselect('div.camera_caption_title')[0].text.strip()

    details = member.cssselect('div.camera_caption_desc')[0].text.strip()

    url = member.getparent().attrib['data-link']

    idRegex = re.search('\/([0-9]*)-.*', url)
    memberData['id'] = idRegex.group(1)

    detailParts = details.rsplit('-', 1)

    memberData['party'] = PARTY_MAP[detailParts[0].strip().replace('Bloque ', '')]

    memberData['district'] = detailParts[1].strip()

    print memberData

    parsedMembers.append(memberData)

print 'Counted {} Members'.format(len(parsedMembers))

try:
    scraperwiki.sqlite.execute('DELETE FROM data')
except sqlite3.OperationalError:
    pass
scraperwiki.sqlite.save(
    unique_keys=['id'],
    data=parsedMembers)
