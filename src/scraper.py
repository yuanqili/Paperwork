import dataset
import requests


class SemanticScholar:

    def __init__(self):
        return

    @staticmethod
    def api(paper_id):
        # s2 keys
        # 'abstract', 'arxivId', 'authors', 'citationVelocity', 'citations', 'doi',
        # 'influentialCitationCount', 'paperId', 'references', 'title', 'topics',
        # 'url', 'venue', 'year'
        api = 'http://api.semanticscholar.org/v1/paper'
        url = f'{api}/{paper_id}'
        j = requests.get(url).json()
        result = {
            'title': j['title'],
            'authors': ', '.join([a['name'] for a in j['authors']]),
            'venue': j['venue'],
            'year': j['year'],
            'url': j['url'],
        }
        print(f'{result["venue"]} {result["year"]} | {result["title"]}')
        print(result['authors'])
        print(result['url'])

        return result


if __name__ == '__main__':
    db = dataset.connect('sqlite:///paper.db')
    table = db['ss']

    s2_ids = [
        'ea9d2a2b4ce11aaf85136840c65f3bc9c03ab649',
        '83174a52f38c80427e237446ccda79e2a9170742',
        '6c8b30f63f265c32e26d999aa1fef5286b8308ad',
        '0f84a81f431b18a78bd97f59ed4b9d8eda390970',
        '1827de6fa9c9c1b3d647a9d707042e89cf94abf0',
        '4215fbbff39a0213888718549f215b124bd2e611',
    ]

    for s2_id in s2_ids:
        j = SemanticScholar.api(s2_id)
        table.insert(j)
