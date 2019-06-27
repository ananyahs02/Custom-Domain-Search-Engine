import searchForTokens
import settings
import tokenizer
import math
import heapq


def calculate_cosine_sim_slow(doc_vec, query):
    wt = 0.0
    score = 0.0
    product = 0.0
    for key in doc_vec:
        tfidf = (1 + math.log(doc_vec[key])) * math.log((settings.total_files/settings.doc_freq[key]))
        wt = wt+ tfidf**2
        if key in query:
           product = product + tfidf**2
    ## add query tfidf
    return product 


def calculate_cosine_sim(doc_vec, query):
    wt = doc_vec[0]
    vec = doc_vec[1]
    cos_prod = 0.0
    for key in query:
        cos_prod = cos_prod + vec.get(key,0)**2
    return (cos_prod/wt)

def rank_docs(doc_ids, query):
    ordered_results = []
    for doc_id in doc_ids:
        doc_vec = settings.read_json(settings.file_tf_path+doc_id+".json")
        score = calculate_cosine_sim(doc_vec, query)
        if(len(ordered_results) > 100):
            heapq.heappushpop(ordered_results,(-score, doc_id))
        else:
            heapq.heappush(ordered_results, (-score, doc_id))
    return ordered_results
        
def print_results(ranked_doc):
    while ranked_doc:
        (score, doc_id) = heapq.heappop(ranked_doc)
        print('score: '+str(score)+' url: '+ settings.code2url[doc_id])

if __name__ == "__main__":
    settings.load_data()
    query = 'artificial intelligence'
    _, doc_ids, query = searchForTokens.process_query(query)
    ranked_doc = rank_docs(doc_ids, query)
    print_results(ranked_doc)
        