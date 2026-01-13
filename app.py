from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

app = Flask(__name__)


def check_technical(parsed, base_url):
    results = {}
    results['https'] = parsed.scheme == 'https'
    try:
        results['sitemap'] = requests.get(urljoin(base_url, '/sitemap.xml')).status_code == 200
    except:
        results['sitemap'] = False
    try:
        results['robots'] = requests.get(urljoin(base_url, '/robots.txt')).status_code == 200
    except:
        results['robots'] = False
    return results

def check_onpage(soup):
    results = {}
    results['title'] = soup.title.string.strip() if soup.title else None
    desc_tag = soup.find('meta', attrs={'name': 'description'})
    results['description'] = desc_tag['content'].strip() if desc_tag and desc_tag.get('content') else None
    results['h1_tags'] = [h1.get_text().strip() for h1 in soup.find_all('h1')]
    images = soup.find_all('img')
    results['images'] = len(images)
    results['images_with_alt'] = sum(1 for img in images if img.get('alt'))
    return results

def check_content(soup):
    text = soup.get_text(separator=' ')
    words = text.split()
    word_count = len(words)
    keywords_tag = soup.find('meta', attrs={'name': 'keywords'})
    keywords = [k.strip().lower() for k in keywords_tag['content'].split(',')] if keywords_tag and keywords_tag.get('content') else []
    keyword_presence = {kw: (kw in text.lower()) for kw in keywords}
    return {'word_count': word_count, 'keywords': keywords, 'keyword_presence': keyword_presence}

def check_links(soup, parsed):
    all_links = [a.get('href') for a in soup.find_all('a', href=True)]
    internal = [l for l in all_links if urlparse(l).netloc == '' or urlparse(l).netloc == parsed.netloc]
    external = [l for l in all_links if urlparse(l).netloc and urlparse(l).netloc != parsed.netloc]
    return {'internal_links': len(internal), 'external_links': len(external)}

def check_social(soup):
    og_title = soup.find('meta', property='og:title')
    twitter_card = soup.find('meta', attrs={'name': 'twitter:card'})
    return {'social_tags': bool(og_title or twitter_card)}

def calculate_score(technical, onpage, content, links, social):
    tech_score = sum([technical['https'], technical['sitemap'], technical['robots']]) / 3 * 25
    img_ratio = (onpage['images_with_alt'] / onpage['images']) if onpage['images'] else 1
    onpage_score = sum([
        bool(onpage['title']),
        bool(onpage['description']),
        bool(onpage['h1_tags']),
        img_ratio > 0.5
    ]) / 4 * 25

    content_score = 0
    if content['word_count'] > 300:
        content_score += 10
    if content['keywords']:
        keyword_hit = any(content['keyword_presence'].values())
        content_score += (10 if keyword_hit else 0)
    content_score = min(content_score, 20)

    links_score = min(links['internal_links'] / 5, 1) * 10 + min(links['external_links'] / 5, 1) * 5
    links_score = min(links_score, 15)

    social_score = 15 if social['social_tags'] else 0

    total = tech_score + onpage_score + content_score + links_score + social_score
    return round(total, 2)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form.get('url')
    if not url:
        return render_template('index.html', error="Please enter a URL")

    if not url.startswith('http'):
        url = 'http://' + url

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"

        technical = check_technical(parsed, base_url)
        onpage = check_onpage(soup)
        content = check_content(soup)
        links = check_links(soup, parsed)
        social = check_social(soup)
        score = calculate_score(technical, onpage, content, links, social)

        return render_template('result.html', url=url, technical=technical,
                               onpage=onpage, content=content, links=links,
                               social=social, score=score)
    except Exception as e:
        return render_template('index.html', error=f"Error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)

