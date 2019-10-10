import time

from elithunter.elithunter import MovieLinks
from db.model import ModelSQLite


def fetch(base, website, m, start_id=None, end_id=None):
    """ Fetchs the links.

    base: Base address
    webiste: Website address
    m: SQL object
    start_id: Starting link ID
    end_id: Ending link ID
    """
    if not start_id:
        start_id = m.getLastId(website) + 1
        end_id = start_id + 100
    movies = MovieLinks(base, start_id, end_id)
    links = movies.getLinks()
    return links

def main():
    try:
        m = ModelSQLite()
        print("Fetching MoviesBaba links...", end="")
        moviesBaba = fetch("https://links.moviebaba.in/archives", "links.moviebaba.in", m)
        time.sleep(60)
        print("Fetching kmhd links...", end="")
        kmhd = fetch("https://kmhd.pw/archives", "kmhd.pw", m)
        links = moviesBaba + kmhd
        m.create_items(sorted(links, key=lambda i:i["created_at"]))
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
