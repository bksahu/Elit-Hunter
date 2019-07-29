from elithunter.elithunter import MovieLinks
from app.model import ModelSQLite

def fetch(base, website, start_id, end_id):
    # if not start_id:
    #     start_id = m.getLastId(website) + 1
    movies = MovieLinks(base, start_id, end_id)
    links = movies.getLinks()
    return links

def main():
    moviesBaba = fetch("https://links.moviebaba.in/archives", "links.moviebaba.in", 37000, 38000)
    import ipdb; ipdb.set_trace()
    kmhd = fetch("https://kmhd.pw/archives", "kmhd.pw", 48000, 49000)
    m = ModelSQLite()
    links = moviesBaba + kmhd
    m.create_items(sorted(links, key=lambda i:i["created_at"]))

if __name__ == "__main__":
    main()
