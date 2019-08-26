import os

import requests
from fuzzywuzzy import fuzz
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils.util import format_str, build_url


class SemanticScholar:

    host_url = 'https://www.semanticscholar.org'
    api_url = 'http://api.semanticscholar.org/v1/paper'

    def __init__(self):
        self.sp_host = os.getenv('sp_host')
        self.sp_port = os.getenv('sp_port')

    def parse_and_search(self, file_path):

        result = {'path': str(file_path)}

        parse_result = SemanticScholar.parse(file_path, self.sp_host, self.sp_port, 'v1/json/pdf')
        result['parsed_id'] = parse_result['docSha']
        result['parsed_title'] = parse_result['title']
        result['parsed_authors'] = parse_result['authors']

        api_result = SemanticScholar.api(parse_result['docSha'])
        if not api_result['ok']:
            ok, search_results = SemanticScholar.search(parse_result['title'])
            if ok:
                sorted(search_results, key=lambda d: d['score'])
                sr = search_results[0]
                match_score = fuzz.ratio(parse_result['title'].lower(), sr['title'].lower())
                if match_score >= 90:
                    api_result = SemanticScholar.api(sr['id'])

        if api_result['ok']:
            result['s2id'] = api_result['paperId']
            result['title'] = api_result['title']
            result['authors'] = [a['name'] for a in api_result['authors']]
            result['venue'] = api_result['venue']
            result['year'] = api_result['year']
            result['abstract'] = api_result['abstract']
            result['topics'] = [t['topic'] for t in api_result['topics']]

        return result

    @staticmethod
    def parse(file_path, host, port, path='v1/json/pdf'):
        url = f'{host}:{port}/{path}'
        headers = {'Content-Type': 'application/pdf'}
        data = open(file_path, 'rb').read()
        response = requests.post(url, headers=headers, data=data)
        result = response.json()['doc']
        if result.get('title'):
            result['title'] = format_str(result['title'])
        if result.get('authors'):
            result['authors'] = [format_str(author) for author in result['authors']]
        return result

    @staticmethod
    def api(paper_id):
        url = f'{SemanticScholar.api_url}/{paper_id}'
        j = requests.get(url).json()
        # s2 keys
        # 'abstract', 'arxivId', 'authors', 'citationVelocity', 'citations', 'doi',
        # 'influentialCitationCount', 'paperId', 'references', 'title', 'topics',
        # 'url', 'venue', 'year'
        j['ok'] = not j.get('error')
        return j

    @staticmethod
    def search(title, timeout=10):
        url = build_url(SemanticScholar.host_url, 'search', params={
            'q': title,
            'sort': 'relevance',
            'fos': 'computer-science',
        })

        options = Options()
        options.add_argument('--headless')
        driver_path = f'{os.getenv("resource_root")}/{os.getenv("chromedriver_path")}'
        driver = webdriver.Chrome(executable_path=driver_path, options=options)
        driver.get(url)
        try:
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'search-result-title'))
            )
            elements = driver.find_elements_by_class_name('search-result-title')
            result = [{
                'title': elem.text,
                'id': elem.find_element_by_tag_name('a').get_attribute('href').split('/')[-1],
                'score': fuzz.ratio(title.lower(), elem.text.lower())
            } for elem in elements]
            status = True
        except TimeoutException:
            result = []
            status = False

        return status, result
