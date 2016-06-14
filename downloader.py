import sys
import os
import urllib
import urllib2
from bs4 import BeautifulSoup

def report(count, block_size, total_size):
    """Report save progression."""
    progress_size = int(count * block_size) / (1024 * 1024)
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r  {0}%, {1} MB".format(percent, progress_size))
    sys.stdout.flush()


def save(url, dst, force=False):
    """Download a file at url to local folder."""
    if not os.path.isfile(dst) or force:
        # Test if the directory exist or create
        d = os.path.dirname(dst)
        if not os.path.exists(d):
            os.makedirs(d)
        print(u"\nDownloading: {0} to {1}".format(url, dst))
        urllib.urlretrieve(url, dst, report)

def downloadYear(year):

    url = 'https://developer.apple.com/videos/wwdc' + str(year) +  '/'
    soup = BeautifulSoup(urllib2.urlopen(url).read(), "html.parser")
    container = soup.find('section', 'all-content')
    for section in container.find_all('li', 'video-tag event'):
        session_string = section.find('span', 'smaller')
        sessionID = session_string.text.split(' ')[1]
        downloadSessionVideo(str(year), sessionID)

def downloadSessionVideo(year, sessionID):
    folder_dst = 'WWDC/2015'
    url = 'https://developer.apple.com/videos/play/wwdc' + year + '/' + sessionID + '/'

    page = BeautifulSoup(urllib2.urlopen(url).read(), "html.parser")
    title = page.find('title').text.split('-')[0].strip()
    print '\n\n'+title
    resource = page.find('ul', 'supplements')
    a = resource.find_all('a')

    for a_href in a:
        if len(a_href) and 'SD' in a_href.text:
            dst = u"{0}/{1}/{2}.mp4".format(folder_dst, title, title)
            save(a_href['href'], dst)

        if len(a_href) and 'PDF' in a_href.text:
            dst = u"{0}/{1}/slides.pdf".format(folder_dst, title)
            save(a_href['href'], dst)

downloadYear(2015)

