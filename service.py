import tver
from cache import Cache
from mylist import MyList

if __name__ == '__main__':
    #initialize DB
    mylist = MyList()
    Cache().create()
    mylist.create()
    
    # cache warming
    for (category, _, _) in tver.get_categories():
        tver.fetch_episodes(category)

    # build MyList
    mylist.delete_expired()
    mylist.build()
