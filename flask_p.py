from flask import Flask, request, jsonify
from flask_restful import Api, Resource
#from flask_cors import CORS
import urllib
import sys
import json
app = Flask(__name__)
api = Api(app)
#CORS(app)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

class tweet(Resource):
    def get(self, request):
        # get json file from front-end
        data = request.json
        
        if 2 == 2:
            print(request)
            print(dir(request))
            tweet_list = []
            tweet_list.append({'text':'This is some test'})
            tweet_list.append({'text2': 'This is another one'})
            response = jsonify(data)
            return response
        input_query = data['query']
        poi = data['poi']
        country = data['country']
        topic = data['topic']
        lang = data['lang']

        # format the query
        encoded_query = "*"
        encoded_poi = ''
        encoded_country = ''
        encoded_topic = ''
        encoded_lang = ''

        input_query = input_query.strip('\n').replace(':', '\:')
        if input_query != 'null' and len(input_query) != 0:
            encoded_query = urllib.parse.quote(input_query) if sys.version_info >= (3,0) else urllib.pathname2url(input_query)


        # format filter condition
        if poi != 'null':
            encoded_poi = ' AND poi_name: ' + poi
            encoded_poi = urllib.parse.quote(poi) if sys.version_info >= (3,0) else urllib.pathname2url(poi)

        if country != 'null':
            encoded_country = ' AND country: ' + country
            encoded_country = urllib.parse.quote(country) if sys.version_info >= (3,0) else urllib.pathname2url(country)

        # if topic != 'null':
        #     encoded_topic = ' AND topic: ' + topic
        #     encoded_topic = urllib.parse.quote(topic) if sys.version_info >= (3,0) else urllib.pathname2url(topic)

        if lang != 'null':
            encoded_lang = ' AND lang: ' + lang
            encoded_lang = urllib.parse.quote(lang) if sys.version_info >= (3,0) else urllib.pathname2url(lang)

        complete_query = encoded_query + encoded_poi + encoded_country + encoded_topic + encoded_lang
        ip_address = '34.239.175.103:8983'
        filter = 'fl=user.screen_name%2C%20full_text&'

        # get solr API ENDPOINT
        print('encoded query', encoded_query)
        query_url = 'http://' + ip_address + '/solr/IRF20P1/select?' + filter + 'q=(text_en%3A%20'\
                    + complete_query + ')%20OR%20(text_it%3A%20' + complete_query + ')%20OR%20(text_hi%3A%20' + complete_query + ')&rows=20&wt=json'
        print("query_url", query_url)

        # save data as .json file
        data = urllib.request.urlopen(query_url) if sys.version_info > (3,0) else urllib.urlopen(query_url)
        docs = json.load(data)['response']['docs']
        tweet_list = []
        for doc in docs:
            tweet_list.append(doc)
        
        """tweet_list = []
        tweet_list.append({'text':'This is some test'})
        tweet_list.append({'text2': 'This is another one'})"""
        
        # return json file
        response = jsonify(tweet_list)
        return response

    def put(self):
        return ''

    def delete(self):
        return '',204


api.add_resource(tweet, '/getTweets')
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port = "8080")
