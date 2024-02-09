from flask import Flask, jsonify, request, g
from flask_restful import Api
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from database import Database


@dataclass
class Media:
    name: str = None
    year: int = None
    duration: str = None
    link: str = None


class QuittAPI:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['DATABASE'] = 'Quitt.db'
        self.api = Api(self.app)
        self.url = "https://quitt.net"
        self.media = []
        self.port = 5000

        try:
            self.db = Database('Quitt.db')
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    @staticmethod
    def scrape_media_data(item_div):
        h2_tag = item_div.find('h2', class_='film-name')
        name_element = h2_tag.find('a')
        year_element = item_div.find('span', class_='fdi-item')
        duration_element = item_div.find('span', class_='fdi-item fdi-duration')
        link_element = item_div.find('a', class_='film-poster-ahref flw-item-tip')['href']

        name = name_element.get_text(strip=True) if name_element else None
        year = year_element.text if year_element else None
        duration = duration_element.text if duration_element else "Season"
        link = f"https://quitt.net/{link_element}" if link_element else None

        return Media(name, year, duration, link)

    def search_media(self, media_name):
        self.media = []
        search_url = f'{self.url}/search/{media_name.replace(" ", "-")}'

        try:
            response = requests.get(search_url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                media_div = soup.find('div', class_='film_list-wrap')

                if media_div:
                    for item_div in media_div.find_all('div', class_='flw-item'):
                        media = self.scrape_media_data(item_div)
                        self.media.append(Media(media.name, media.year, media.duration, media.link))

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

        return self.media

    def run(self):
        @self.app.teardown_appcontext
        def close_db_connection(exception=None):
            db = g.pop('db', None)
            if db is not None:
                db.close_connection()

        @self.app.route('/search/<media_name>', methods=['GET'])
        def search_route(media_name):
            try:
                media = self.search_media(media_name)

                if media:
                    self.db.add_media(media)

                    response_str = '\n'.join(f"{i + 1}: {media}" for i, media in enumerate(media))
                    print(f"{response_str}\n")
                    return jsonify(media)
                else:
                    return jsonify({'message': 'No media found'}), 404

            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @self.app.route('/media/<media_name>', methods=['GET', 'DELETE'])
        def media_operations(media_name):
            if request.method == 'GET':
                return self.get_media_by_name(media_name)

            elif request.method == 'DELETE':
                return self.delete_media(media_name)

            return jsonify({'error': 'Invalid request method'}), 405

        self.app.run(port=self.port, debug=True)

    def get_media_by_name(self, media_name):
        result = self.db.get_media_by_name(media_name)
        if result:
            return jsonify(result)
        return jsonify({'message': 'Media not found'}), 404

    def delete_media(self, media_name):
        success = self.db.delete_media(media_name)
        if success:
            return jsonify({'message': 'Media deleted successfully'})
        return jsonify({'message': 'Failed to delete media'}), 500
