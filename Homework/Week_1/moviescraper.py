#!/usr/bin/env python
# Name: Machiel Cligge
# Student number: 10772006
"""
This script scrapes IMDB and outputs a CSV file with highest rated movies.
"""

import csv
import re
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

TARGET_URL = "https://www.imdb.com/search/title?title_type=feature&release_date=2008-01-01,2018-01-01&num_votes=5000,&sort=user_rating,desc"
BACKUP_HTML = 'movies.html'
OUTPUT_CSV = 'movies.csv'


def extract_movies(dom):
    """
    Extract a list of highest rated movies from DOM (of IMDB page).
    Each movie entry should contain the following fields:
    - Title
    - Rating
    - Year of release (only a number!)
    - Actors/actresses (comma separated if more than one)
    - Runtime (only a number!)
    """


    movies = []
    for item in dom.select("div.lister-item-content"):
        for movieheader in item.select("h3.lister-item-header"):

            # Make each movie individual list
            movie = []

            # Add movie title to movie
            for title in movieheader.find_all('a'):
                movie.append(title.string)

            # Add rating to movie
            for ratingheader in item.select("div.ratings-imdb-rating"):
                for rating in ratingheader.find('strong'):
                    movie.append(rating.string)

            # Add release year to movie
            for year in movieheader.select("span.lister-item-year"):
                year = re.sub('[^0-9,.]', '', year.string)
                movie.append(year)

            # Add list of actors to movie
            for infoheader in item.select('p'):
                stars = []
                # Make list of stars in movie
                for star in infoheader.find_all('a'):
                    if "st" in star.get('href'):
                        stars.append(star.string)
                        mov_stars = ", ".join(stars)
            # Add stars to movie
            movie.append(mov_stars)

            # Add runtime to movie
            for runtime in item.select("span.runtime"):
                runtime = re.sub("[^0-9,.]", "", runtime.string)
                movie.append(runtime)

        # Add each movie to movie_output
        movies.append(movie)

    return movies


def save_csv(outfile, movies):
    """
    Output a CSV file containing highest rated movies.
    """
    writer = csv.writer(outfile)
    writer.writerow(['Title', 'Rating', 'Year', 'Actors', 'Runtime'])

    # Iterate over movies and add to csv
    for movie in movies:
        writer.writerow(movie)


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        print('The following error occurred during HTTP GET request to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


if __name__ == "__main__":

    # get HTML content at target URL
    html = simple_get(TARGET_URL)

    # save a copy to disk in the current directory, this serves as an backup
    # of the original HTML, will be used in grading.
    with open(BACKUP_HTML, 'wb') as f:
        f.write(html)

    # parse the HTML file into a DOM representation
    dom = BeautifulSoup(html, 'html.parser')

    # extract the movies (using the function you implemented)
    movies = extract_movies(dom)

    # write the CSV file to disk (including a header)
    with open(OUTPUT_CSV, 'w', newline='') as output_file:
        save_csv(output_file, movies)
