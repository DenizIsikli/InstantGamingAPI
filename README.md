# Disclaimer

Quitt.net has been taken down and is no longer available meaning that this API is no longer functional.
This repository is kept for informational purposes only.

# QuittAPI

QuittAPI is a Flask-based RESTful API developed to retrieve information about movies and TV shows available on Quitt.net. It offers various endpoints to access and manage product information in a structured format.

## Installation and Setup

To run the QuittAPI, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/quitt-api.git
    ```

2. Install dependencies:

    ```bash
    cd quitt-api
    pip install -r requirements.txt
    ```

3. Run the application:

    ```bash
    python app.py
    ```

## Usage

The QuittAPI provides endpoints for movie and TV show-related operations:

### Search for a Movie or TV Show

- **URL:** `/search/<product_name>`
- **Method:** GET
- **Description:** Searches for a movie or TV show by name and returns a list of matching products.
- **Parameters:**
  - `product_name` (string): The name of the movie or TV show to search for.

### Get Product Information

- **URL:** `/products/<product_name>`
- **Methods:** GET, PUT, DELETE
- **Description:** Perform operations on a specific movie or TV show.
  - `GET`: Retrieve details of a movie or TV show by its name.
  - `PUT`: Update the price of a movie or TV show by providing a new price in the request body (JSON format).
  - `DELETE`: Delete a movie or TV show by its name.

## Database Integration

The QuittAPI integrates with a SQLite database named `Quitt.db` to store and manage product information. Ensure the database is set up and accessible before running the application.

## Dependencies

- Flask: Web framework for building the API.
- Flask-RESTful: Extension for creating REST APIs with Flask.
- Requests: Library for making HTTP requests.
- BeautifulSoup: For web scraping and parsing HTML data.
- Dataclasses: Provides a decorator for quickly defining classes with a set of fields.

## Contributions

Contributions to enhance the functionality, add new features, or fix issues are welcome. Please submit pull requests or report any bugs via GitHub issues.

## Disclaimer

This project is for educational purposes and is not affiliated with Quitt.net. Use the API responsibly and ensure compliance with Quitt.net's terms of service when accessing their data.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
