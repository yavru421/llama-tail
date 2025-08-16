from ddgs import DDGS
from typing import List

def ddgs_search(query: str, max_results: int = 5) -> List[str]:
    ddgs = DDGS()
    results = ddgs.text(query, max_results=max_results)
    return [r['body'] for r in results if 'body' in r]
