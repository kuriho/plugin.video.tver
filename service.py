import tver
from cache import Cache
from mylist import MyList

if __name__ == '__main__':
    # cache warming
    Cache().create()
    for (category, _, _) in tver.get_categories():
        tver.fetch_episodes(category)

    # build MyList
    mylist = MyList()
    mylist.create()
    mylist.delete_expired()
    mylist.build()
