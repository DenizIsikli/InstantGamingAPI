import sqlite3
from flask import Flask, jsonify, request
from flask_restful import Api
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from cachetools import cached, TTLCache
from database import Database


@dataclass
class Product:
    name: str = None
    price: int = None
    link: str = None


class InstantGamingAPI:
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.url = "https://www.instant-gaming.com/en"
        self.products = []
        self.name = None
        self.info = None
        self.price = None
        self.link = None
        self.port = 5000

        try:
            self.db = Database('pricerunner.db')
        except sqlite3.Error as e:
            print(f"Error connecting to the database: {e}")

    @staticmethod
    def scrape_product_data(item_div):
        name_element = item_div.find('span', class_='title')
        price_element = item_div.find('div', class_='price')
        link_element = item_div.find('a', class_='cover video is-playable played')

        # Extract product information within each product's container
        name = name_element.text if name_element else None
        price = price_element.text if price_element else None
        link = link_element.text if link_element else None

        return Product(name, price, link)

    # Create a cache with a TTL (time-to-live) of 300 seconds
    cache = TTLCache(maxsize=100, ttl=300)

    @cached(cache)
    def search_product(self, product_name):
        self.url = f'{self.url}/search/?q={product_name.replace(" ", "+")}'

        try:
            response = requests.get(self.url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                product_div = soup.find('div', class_='search listing-items')

                if product_div:
                    for item_div in product_div.find_all('div', class_='item force-badge'):
                        product = self.scrape_product_data(item_div)
                        self.products.append(Product(product.name, product.price, product.link))
                        print(self.products)

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

        return self.products

    def get_product_by_name(self, product_name):
        query = "SELECT * FROM mytable WHERE name = ?"
        result = self.db.execute_query(query, (product_name,))
        if result:
            return jsonify(result)
        return jsonify({'message': 'Product not found'}), 404

    def update_product_price(self, product_name, new_price):
        query = "UPDATE mytable SET price = ? WHERE name = ?"
        self.db.execute_update(query, (new_price, product_name))
        return jsonify({'message': 'Product price updated successfully'})

    def delete_product(self, product_name):
        query = "DELETE FROM mytable WHERE name = ?"
        self.db.execute_update(query, (product_name,))
        return jsonify({'message': 'Product deleted successfully'})

    def run(self):
        @self.app.route('/search/<product_name>')
        def search_route(product_name):
            try:
                products = self.search_product(product_name)
                insert_query = "INSERT INTO mytable (name, price, link) VALUES (?, ?, ?)"

                for product in products:
                    data_to_insert = (product.name, product.price, product.link)
                    # self.db.execute_update(insert_query, data_to_insert)
                    return jsonify(products)

            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @self.app.route('/products/<product_name>', methods=['GET', 'PUT', 'DELETE'])
        def product_operations(product_name):
            if request.method == 'GET':
                return self.get_product_by_name(product_name)

            elif request.method == 'PUT':
                new_price = request.json.get('price')  # Assume updating the price
                return self.update_product_price(product_name, new_price)

            elif request.method == 'DELETE':
                return self.delete_product(product_name)

            return jsonify({'error': 'Invalid request method'}), 405

        self.app.run(port=self.port, debug=True)
