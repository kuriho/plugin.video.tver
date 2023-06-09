from lib.tver import get_categories
from lib import Cache, MyList, create_tables

if __name__ == '__main__':
    #initialize DB
    create_tables()
    
    # cache warming
    cache = Cache()
    cache.delete_expired()
    for (category, _, _) in get_categories():
        cache.get_or_download(category)

    # build MyList
    mylist = MyList()
    mylist.delete_expired()
    mylist.build()
