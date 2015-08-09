"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
from flask import Flask, render_template
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

@app.route('/')
def main():
    return render_template("main.html", cities=get_cities())

def get_cities():
    from xml.etree.ElementTree import parse
    import urllib
    cities = []
    tree = parse(urllib.urlopen('https://pogoda.yandex.ru/static/cities.xml'))
    for country in tree.findall('country'):
        name = country.get('name')
        if name == u'Россия':
            for item in country:
                cities.append(item.text + item.attrib['id'])
    #cities.sort()
    return cities


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)
