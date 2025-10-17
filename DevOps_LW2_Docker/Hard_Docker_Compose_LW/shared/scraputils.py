import requests  # type: ignore
from bs4 import BeautifulSoup  # type: ignore

def safe_get(element, selector, class_=None, default='-'):
    """Безопасный поиск элемента с значением по умолчанию"""
    found = element.find(selector, class_=class_)
    return found.text.strip() if found and found.text else default

def extract_news(parser):
    """Extract news from a given web page"""
    news_list = []
    all_articles = parser.select('article[class="tm-articles-list__item"]')
    for article in all_articles:
        author = safe_get(article, "a", class_="tm-user-info__username")
        title = safe_get(article, "a", class_="tm-title__link")
        complexity = (
            article.find("span", class_="tm-article-complexity__label").text.strip()
            if article.find("span", class_="tm-article-complexity__label")
            else "-"
        )
        id = article["id"]
        #print(id)
        link = "https://habr.com" + article.find("a", class_="tm-title__link").get("href")
        dict = {"author": author, "complexity": complexity, "habr_id": id, "url": link, "title": title}
        news_list.append(dict)
    return news_list


def extract_next_page(parser):
    """Extract next page URL"""
    element = parser.find("a", id="pagination-next-page")
    next_page = element.get("href", "Следующей страницы нет")
    return next_page


def get_news(url, n_pages=1):
    """Collect news from a given web page"""
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://habr.com" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news

current_page = 17
def get_news_from_a_page(url):
    news = []
    global current_page
    url = url + f'page{current_page}/'
    print("Collecting data from page: {}".format(url))
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    news_list = extract_news(soup)
    news.extend(news_list)
    current_page += 1
    return news