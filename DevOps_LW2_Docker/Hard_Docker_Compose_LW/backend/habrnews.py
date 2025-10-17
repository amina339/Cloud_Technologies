import os
from bottle import route, run, template, request, redirect, app  # type: ignore
from shared.scraputils import get_news_from_a_page
#from database.bd_filling import session
from shared.db import News
from bayes import NaiveBayesClassifier
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

database_url = os.getenv('DATABASE_URL')
engine = create_engine(database_url)

session = sessionmaker(bind=engine)

@route('/')
def index():
    redirect("/news")

@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@route("/add_label/")
def add_label():
    id = int(request.query.get("id"))
    label = request.query.get("label")
    s = session()
    row = s.query(News).get(id)
    row.label = label
    s.commit()
    redirect("/news")

def update_news():
    s = session()
    news = get_news_from_a_page("https://habr.com/ru/articles/")
    for a_news in news:
        habr_id = a_news["habr_id"]
        existing = s.query(News).filter(News.habr_id == habr_id).first()
        if not existing:
            new_news = News(
                title=a_news["title"],
                author=a_news["author"],
                url=a_news["url"],
                complexity=a_news["complexity"],
                habr_id=a_news["habr_id"],
                label=None
            )
            s.add(new_news)
        else:
            print(existing)
    s.commit()

@route("/update_news_for_labels")
def update():
    update_news()
    redirect("/news")


def classify_news():
    s = session()
    labeled_rows = s.query(News).filter(News.label != None).all()
    unlabeled_rows = s.query(News).filter(News.label == None).all()
    print(f"Labeled: {labeled_rows}")  # Для отладки
    print(f"Unlabeled: {unlabeled_rows}")  # Для отладки
    bayes = NaiveBayesClassifier()
    y_train = [news.label for news in labeled_rows]
    X_train = [" ".join([news.title, news.author, news.url, news.complexity]) for news in labeled_rows]
    X_test = [" ".join([news.title, news.author, news.url, news.complexity]) for news in unlabeled_rows]
    bayes.fit(X_train, y_train)
    prediction = bayes.predict(X_test)
    res = list(zip(unlabeled_rows, prediction))
    order = ["good", "maybe", "never"]
    sorted_news = [news for news, label in sorted(res, key=lambda x: order.index(x[1]))]
    return sorted_news

@route("/news_recommendations")
def show_news():
    sorted_news = classify_news()
    return template("recommendations", rows=sorted_news)

@route("/update_news")
def update_for_recommendation():
    update_news()
    redirect("/news_recommendations")

if __name__ == "__main__":
    run(host='0.0.0.0', port=8080, reloader=True)
