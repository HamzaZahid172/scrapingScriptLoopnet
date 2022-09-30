from bs4 import BeautifulSoup
import requests
import json
import argparse


headers = {
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
}


class App:
    listes = {}
    address = []
    price = []
    type = []
    area = []
    built_in =  []
    unit = []
    def __init__(self, url, path):


        all_url = [url]


  
        for link in all_url:

            self.scrapedata(link)
            pagination_urls = self.pagination(link)
            print(pagination_urls)
            try:
                for pg_url in pagination_urls:
                    self.scrapedata(pg_url)
            except:
                pass

        with open(f'{path}/Final_Output.json', "w") as outfile:
            json.dump(self.listes, outfile, indent=4)
        print("Complete Now Thanks You")


    def pagination(self,link):
        try:
            paguination_url = []
            req =requests.get(link,headers=headers,timeout=10)
            makesoup = BeautifulSoup(req.text,"lxml")
            total_count = round(int(makesoup.find("span",{"class":"total-results-paging-digits"}).text.split('of')[1].strip())/20)
            for x in range(total_count):
                paguination_url.append(link.split('?')[0] + str(x+2))
            return paguination_url
        except:
                'Not_pagination'


            
    def scrapedata(self,url):
   
        try:
            req =requests.get(url,headers=headers,timeout=10)
            makesoup = BeautifulSoup(req.text,"lxml")
            try:
                for add in makesoup.findAll("div",{"class":"header-col"}):
                    self.address.append(add.text.replace('\n',"").replace('\r',"").strip())
                self.listes['Address'] = self.address
            except:
                pass

            try:
                for typ in makesoup.select('article[class*="placard tier"]'):
                    self.type.append(typ['gtm-listing-property-type-name'].replace('\n',"").replace('\r',"").strip() + ' Building')
                self.listes['Type'] = self.type
            except:
                pass
            try:
                for typ in makesoup.select('script[type="application/ld+json"]:nth-child(5)'):
                    data = json.loads(typ.text)
                    for x in range(len(data['about'])):
                        try:
                            self.price.append('$ ' + data['about'][x]['item']['price'])
                            self.area.append(data['about'][x]['item']['description'].split('SF')[0] + 'SF')
                        except:
                            self.price.append('')
                            self.area.append(data['about'][x]['item']['description'].split('SF')[0] + 'SF')
                        self.listes['cost'] = self.price
                        self.listes['area'] = self.area
            except:
                pass

            try:
                for typ in makesoup.select('div[class="data"] ul'):
                    built_len = len(typ.text.replace('\n',"").replace('\r',"").strip().split('Built in'))
                    if(built_len == 2):
                        strings = typ.text.replace('\n',"").replace('\r',"").strip().split('Built in')[1].split(' ')
                        built_date_len = [x for x in strings if x]
                        self.built_in.append(built_date_len[0])

                    else:
                        self.built_in.append('')
                self.listes['Built In'] = self.built_in
            except:
                pass
            try:
                for typ in makesoup.select('div[class="data"] ul'):
                    built_len = len(typ.text.replace('\n',"").replace('\r',"").strip().split(' Available'))
                    if(built_len == 2):
                        strings = typ.text.replace('\n',"").replace('\r',"").strip().split(' Available')[0].split(' ')
                        built_date_len = [x for x in strings if x]
                        self.unit.append(str(built_date_len[len(built_date_len)-2]) + 'Unit')

                    else:
                        self.unit.append('')
                    self.listes['Unit'] = self.unit
            except:
                pass
            
        except:
            pass
        return self.listes 

        


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--Url=', dest='Url', type=str, help='Add Url')
    parser.add_argument('--Path=', dest='Path', type=str, help='Add Path')
    args = parser.parse_args()

    app = App(args.Url, args.Path)

