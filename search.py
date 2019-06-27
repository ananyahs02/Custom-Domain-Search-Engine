import settings
import searchForTokens
import rankPages
import heapq
from flask import Flask, jsonify, render_template
from fuzzywuzzy import fuzz
app = Flask(__name__)

def print_results(ranked_doc):
    urls =[]
    while ranked_doc:
        if(len(urls) == 5000):
            break
        (score, doc_id) = heapq.heappop(ranked_doc)
        #print('score: '+str(score)+' url: '+ settings.code2url[doc_id])
        urls.append(settings.code2url[doc_id])
    return urls


@app.route('/search/<query>')
def search(query):
    _, doc_ids, query = searchForTokens.process_query(query)
    ranked_doc = rankPages.rank_docs(doc_ids, query)
    urls = print_results(ranked_doc)
    if(urls == []):
        for token in settings.doc_freq:
            if(fuzz.ratio(query,token) > 60):
                return search(token)
    return jsonify(urls)


if __name__ == "__main__":
    settings.load_data()
    app.run(debug=True,port = 4996)