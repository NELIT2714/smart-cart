import requests
import json
import requests
import cloudscraper

from api import app, templates

from fastapi import Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder

from bs4 import BeautifulSoup


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )


@app.get("/get_products")
async def get_products():

    with open("api/categories.json", encoding="utf-8") as categories_data:
        categories_data = json.load(categories_data)

    categories_urls_atb = categories_data["atb"]
    scraper = cloudscraper.create_scraper(delay=10, browser="chrome")

    pagination = scraper.get(categories_urls_atb[1] + "?page=10000").text
    soup_pagination = BeautifulSoup(pagination, "lxml")
    pages_count = int(soup_pagination.find("li", class_="product-pagination__item active").find("a").text)

    products = []

    for category in categories_urls_atb:
        for page in range(1, pages_count + 1):
            response = scraper.get(category + "?page=" + str(page)).text
            soup = BeautifulSoup(response, "lxml")
            articles = soup.find("div", class_="catalog-list").find_all("article", class_="catalog-item")

            for article in articles:
                article_title = article.find("div", class_="catalog-item__title").find("a")
                article_bottom = article.find("div", class_="catalog-item__bottom")

                article_name = article_title.text
                article_url = article_title.get("href")
                article_price = article_bottom.find("data").get("value")

                products.append({
                    "name": article_name,
                    "url": "https://www.atbmarket.com" + article_url,
                    "price": article_price
                })

    return products

