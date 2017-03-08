#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import re
import json
import urllib2
from bs4 import BeautifulSoup


class WeatherFetcher:
    WEATHER_URL = 'http://weather.yahoo.co.jp/weather/jp/13/4410.html'

    def __init__(self):
        pass

    def main(self):
        self.fetch_weather()
        print(self.to_json())

    def to_json(self):
        w = []
        for day in self.week_days:
            wd = {}
            for title in self.week_weather:
                wd[title] = self.week_weather[title][day]
            day_o = self.convert_day(day)
            wd['date'] = "%s/%s" % (day_o['month'], day_o['day'])
            if re.match("^-+$", wd['weather']) is None:
                w.append(wd)
        return json.dumps(w, ensure_ascii=False)

    def title_map(self, title):
        tmap = {
            u'日付': 'date',
            u'天気': 'weather',
            u'気温（℃）': 'temperature',
            u'降水確率（％）': 'precipitation',
        }
        if title in tmap:
            return tmap[title]
        raise KeyError("No such title: %s" % (title))

    DAY_RE = re.compile(u"(?P<month>[0-9]+)月(?P<day>[0-9]+)日")

    def convert_day(self, day_expr):
        matcher = WeatherFetcher.DAY_RE.match(day_expr)
        if matcher is None:
            raise ValueError("Unknown day expression %s" % (day_expr))
        return matcher.groupdict()

    def fetch_weather(self):
        # TODO
        # self.fetch_2day_weather()
        self.fetch_week_weather()

    def fetch_week_weather(self):
        self.fetch_html()
        self.soup = BeautifulSoup(self.html, "html.parser")
        week_weather_tables = self.soup.select("div#yjw_week > table.yjw_table")
        if len(week_weather_tables) != 1:
            raise ValueError("Unexpected HTML: not just 1 table(s) in div#yjw_week: %s" % (len(week_weather_tables)))
        weather = {}
        days = []
        for tr in week_weather_tables[0].find_all("tr"):
            day_count = 0
            title_name = None
            for td in tr.find_all("td"):
                if day_count == 0:
                    title = td.text.strip()
                    title_name = self.title_map(title)
                    if title_name not in weather and title_name != 'date':
                        weather[title_name] = {}
                else:
                    if title_name == 'date':
                        days.append(td.text)
                    else:
                        if title_name == 'temperature':
                            weather[title_name][days[day_count - 1]] = list(map(lambda x: x.text, td.find_all("font")))
                        else:
                            weather[title_name][days[day_count - 1]] = td.text
                day_count += 1
        self.week_days = days
        self.week_weather = weather

    def fetch_html(self):
        res = urllib2.urlopen(WeatherFetcher.WEATHER_URL)
        if res.getcode() != 200:
            raise ValueError("Code must be 200")
        self.html = res.read()

if __name__ == '__main__':
    wf = WeatherFetcher()
    wf.main()
