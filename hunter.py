from elithunter.elithunter import MovieLinks
from app.model import ModelSQLite

def fetch_and_store(base, website, start_id=None):
    m = ModelSQLite()
    if not start_id:
        start_id = m.getLastId(website) + 1
    moviebaba = MovieLinks(base, start_id, 1200)
    links = moviebaba.getLinks()
    m.create_items(links)

def main():
    fetch_and_store("https://links.moviebaba.in/archives", "links.moviebaba.in")
    fetch_and_store("https://kmhd.pw/archives", "kmhd.pw")

if __name__ == "__main__":
    main()
