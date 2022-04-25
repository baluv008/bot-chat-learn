import requests
import time
from bs4 import BeautifulSoup

from flask import session

def get_train_from_to(source,dest,travel_date,travel_time):

    s = requests.Session()
    r1 = s.get("https://ojp.nationalrail.co.uk/service/timesandfares/%s/%s/%s/%s/dep"%(source,dest,travel_date,travel_time))

    sp = BeautifulSoup(r1.text, "lxml")
    departures = sp.find_all("div", "dep")

    if departures != []:
        duration = sp.find_all("div", "dur")
        changes = sp.find_all("div","chg")
        output = None
        for i,v in enumerate(departures):

            train_time = time.strptime(str(v.getText().strip()),"%H:%M")
            given_time = time.strptime(travel_time,"%H%M")
            if train_time > given_time:
                r2 = s.get("https://ojp.nationalrail.co.uk/service/details?outboundJourneyId=%s&outboundFareId=10&outboundResponseId=4&isOutboundJourneySelected=true"%(str(i+1)))
                # session["duration"] = duration
                # session["changes"] = changes
                session["stations"] = []
                price = sp.find_all("label", "opsingle")[i].text.strip()
                session["price"] = price
                get_stops(html_text=r2.text)

                output = duration[i].getText(),changes[i].getText(),"Next train after %s is at <b>%s</b>. It will take %s to reach %s with %s" %(travel_time, departures[i].getText(),duration[i].getText(),dest, changes[i].getText())
                break
            else:
                pass
        return output

def get_stops(html_text=None,source=None, dest=None,travel_date=None, travel_time=None):

    if html_text is None:
        get_train_from_to(source,dest, travel_date,travel_time)
    else:
        sp = BeautifulSoup(html_text, "lxml")


        for c in sp.find_all("div", "callingpointslide"):
            t = c.find_all("td")
            for i,item in enumerate(t):
                a_tag = item.find("a")
                arrives = item.next_sibling.text
                departs = item

                if a_tag is not None:
                    session["stations"].append(a_tag.getText()+" : "+arrives)

                elif arrives is not None:
                   pass
                elif departs is not None:
                    pass


# print(get_train_from_to("SOU","BSK","today","1500"))