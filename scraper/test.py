import os
import unittest
from unittest import mock

from bs4 import BeautifulSoup

from scraper.common import notify, get_post_links
from scraper.models import Apartment, Listing


class TestCommonMethods(unittest.TestCase):

    def setUp(self):
        avto_test = os.path.join('..', 'scraper', 'test', 'avto_test.html')
        with open(avto_test, 'r') as f:
            contents = f.read()
            self.soup = BeautifulSoup(contents, 'html.parser')


    @mock.patch.dict(os.environ, {"DISCORD_WH": "https://discord.com/api/webhooks/832571075639771156/4w7b84FoShvgSSA-k7dIf6_12IORT891LDhNzGRN1I9lMPMe2DglYSrTPVL8gg4k47IR"})
    def test_notification(self):
        ap = Apartment()
        ap.description = 'Test message. If you see this message, the test passed.'
        self.assertTrue(notify(ap))

    def test_get_post_links(self):
        l = Listing()
        l.url = 'https://www.avto.net/Ads/results.asp?znamka=&model=&modelID=&tip=&znamka2=&model2=&tip2=&znamka3=&model3=&tip3=&cenaMin=0&cenaMax=12000&letnikMin=2017&letnikMax=2090&bencin=201&starost2=999&oblika=13&ccmMin=0&ccmMax=1350&mocMin=&mocMax=&kmMin=0&kmMax=100000&kwMin=0&kwMax=999&motortakt=0&motorvalji=0&lokacija=0&sirina=0&dolzina=&dolzinaMIN=0&dolzinaMAX=100&nosilnostMIN=0&nosilnostMAX=999999&lezisc=&presek=0&premer=0&col=0&vijakov=0&EToznaka=0&vozilo=&airbag=&barva=&barvaint=&EQ1=1000000000&EQ2=1000000100&EQ3=1000000000&EQ4=100000000&EQ5=1000000000&EQ6=1000000000&EQ7=1110100020&EQ8=1010000001&EQ9=1000000000&KAT=1010000000&PIA=&PIAzero=&PSLO=&akcija=0&paketgarancije=&broker=0&prikazkategorije=0&kategorija=0&ONLvid=0&ONLnak=0&zaloga=10&arhiv=0&presort=3&tipsort=DESC&stran=1&subSELLER=1'
        l.post_link_list_selector = '#results .stretched-link'

        links = get_post_links(self.soup, l)
        self.assertGreater(len(links), 0)

if __name__ == '__main__':
    unittest.main()