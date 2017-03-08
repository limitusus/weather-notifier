# Weather Notifier

[Weather Page by Yahoo! JP](http://weather.yahoo.co.jp/weather/jp/13/4410.html)

# Runtime Environment

Python 2.7.x

# Build Package

Follow the instruction by https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html

```sh
# Install requirements
pip install -r packages.list -t .
# Zip the directory contents (not the directory itself)
zip -r weather-notifier.zip * --exclude '@exclude.lst'
```
