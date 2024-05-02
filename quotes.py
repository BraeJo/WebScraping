from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import plotly.graph_objs as go

def scrape_quotes(url):
    quotes = []
    for page_num in range(1, 11):
        req = Request(url + f'page/{page_num}/', headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(req)
        soup = BeautifulSoup(response.read(), 'html.parser')
        quote_divs = soup.find_all('div', class_='quote')
        for quote_div in quote_divs:
            text = quote_div.find('span', class_='text').text
            author = quote_div.find('small', class_='author').text
            tags = [tag.text for tag in quote_div.find_all('a', class_='tag')]
            quotes.append({'text': text, 'author': author, 'tags': tags})
    return quotes

def analyze_quotes(quotes):
    author_quotes = {}
    for quote in quotes:
        author_quotes[quote['author']] = author_quotes.get(quote['author'], 0) + 1
    
    most_quotes_author = max(author_quotes, key=author_quotes.get)
    least_quotes_author = min(author_quotes, key=author_quotes.get)
    
    quote_lengths = [len(quote['text']) for quote in quotes]
    average_quote_length = sum(quote_lengths) / len(quote_lengths)
    longest_quote = max(quotes, key=lambda x: len(x['text']))
    shortest_quote = min(quotes, key=lambda x: len(x['text']))
    
    all_tags = [tag for quote in quotes for tag in quote['tags']]
    tag_counts = {tag: all_tags.count(tag) for tag in set(all_tags)}
    most_popular_tag = max(tag_counts, key=tag_counts.get)
    total_tags_used = len(set(all_tags))
    
    top_10_authors = sorted(author_quotes.items(), key=lambda x: x[1], reverse=True)[:10]
    authors = [author[0] for author in top_10_authors]
    num_quotes = [author[1] for author in top_10_authors]
    fig = go.Figure(data=[go.Bar(x=authors, y=num_quotes)])
    fig.update_layout(title='Top 10 Authors by Number of Quotes')
    fig.show()

    return {
        'Author Statistics': {
            'Author with most quotes': most_quotes_author,
            'Author with least quotes': least_quotes_author
        },
        'Quote Analysis': {
            'Average quote length': average_quote_length,
            'Longest quote': longest_quote['text'],
            'Shortest quote': shortest_quote['text']
        },
        'Tag Analysis': {
            'Most popular tag': most_popular_tag,
            'Total tags used': total_tags_used
        }
    }

if __name__ == '__main__':
    url = 'http://quotes.toscrape.com/'
    quotes = scrape_quotes(url)
    analysis_results = analyze_quotes(quotes)
    print(analysis_results)
