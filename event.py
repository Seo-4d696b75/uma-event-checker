import json
from difflib import SequenceMatcher
from joblib import Parallel, delayed


data = json.load(open('event.json', 'r', encoding='utf-8'))

def find_event(txt):
    process = lambda event: SequenceMatcher(None, event['e'], txt).quick_ratio()
    #score = Parallel(n_jobs=4)([delayed(process)(e) for e in data])
    score = [process(e) for e in data]
    max_score = max(score)
    if max_score > 0.6:
        return [d for idx,d in enumerate(data) if score[idx]==max_score]
    else:
        return []

def filter_events(events,name):
    process = lambda event: SequenceMatcher(None, event['n'], name).quick_ratio()
    #score = Parallel(n_jobs=4)([delayed(process)(e) for e in data])
    score = [process(e) for e in events]
    max_score = max(score)
    idx = score.index(max_score)
    return events[idx]
