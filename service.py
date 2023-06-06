from lib import Cache, tver, Favourites, MyList

if __name__ == '__main__':
    #initialize DB
    mylist = MyList()
    Cache().create()
    Favourites().create()
    mylist.create()
    
    # cache warming
    for (category, _, _) in tver.get_categories():
        tver.fetch_episodes(category)

    # build MyList
    mylist.delete_expired()
    mylist.build()
