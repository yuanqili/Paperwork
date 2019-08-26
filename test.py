import os
from pathlib import Path

from tinydb import TinyDB, Query
from dotenv import load_dotenv

from parse.semantic_scholar import SemanticScholar

if __name__ == '__main__':
    load_dotenv()

    db = TinyDB(os.getenv('db_path'))
    ss = SemanticScholar()

    library = Path('/Users/yuanqili/Develop/live-video-analytics/paper')
    papers = [p for p in sorted(library.iterdir()) if p.suffix == '.pdf']

    for paper in papers:
        print(f'processing {paper}')
        parse = ss.parse_and_search(paper)
        db.insert(parse)

    db.all()
