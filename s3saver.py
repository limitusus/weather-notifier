#!/usr/bin/env python
# -*- coding: utf-8 -*-

import calendar
import time
import boto3
import weather

BUCKET = 'limitusus-weather'

class S3Saver:
    def __init__(self, wf):
        self.wf = wf
        self.s3 = boto3.client('s3')

    def main(self):
        self.wf.fetch_weather()
        tokyo_time = time.gmtime(calendar.timegm(time.gmtime()) + 9 * 60 * 60)
        dt = time.strftime("%Y/%m/%Y-%m-%d", tokyo_time) + ".json"
        self.put_object(dt, self.wf.to_json())

    def put_object(self,key, data):
        self.s3.put_object(
            Bucket=BUCKET,
            Key=key,
            Body=data,
        )


def lambda_handler(input, context):
    wf = weather.WeatherFetcher()
    saver = S3Saver(wf)
    saver.main()

if __name__ == '__main__':
    lambda_handler(None, None)
