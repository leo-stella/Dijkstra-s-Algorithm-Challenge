import json
import sqlite3
from sqlite3 import Error
from collections import OrderedDict
import falcon


def get_data(mf_path=False, em_path=False):
    # errors related to the millennium-falcon file
    mf_error = False
    # errors related to the empire file
    em_error = False
    # errors related to the database
    db_error = False

    millennium_falcon = {}
    if not mf_path:
        mf_path = 'millennium-falcon.json'
    try:
        with open(mf_path) as f_falcon:
            millennium_falcon = json.load(f_falcon)
    except FileNotFoundError:
        print('"millennium-falcon.json" file does not exist')
        mf_error = True

    if millennium_falcon and isinstance(millennium_falcon['autonomy'], int):
        autonomy = millennium_falcon['autonomy']
    else:
        mf_error = True
        autonomy = None
        print('"Autonomy" value is not an integer')

    conn = None
    path_list = []
    try:
        conn = sqlite3.connect(millennium_falcon['routes_db'])
        cur = conn.cursor()
        cur.execute("SELECT * FROM ROUTES")
        path_list = cur.fetchall()
    except Error as e:
        db_error = True
        print(e)
    finally:
        if conn:
            conn.close()

    planets = []
    for path in path_list:
        planets.append(path[0])
        planets.append(path[1])
    planets = list(OrderedDict.fromkeys(planets))

    i = 0
    planet_dict = {}
    for planet in planets:
        planet_dict[planet] = i
        i += 1
    g = falcon.Graph(len(planets))
    for path in path_list:
        g.add_path(planet_dict[path[0]], planet_dict[path[1]], path[2])

    if millennium_falcon['departure'] in planets and millennium_falcon['arrival'] in planets:
        start_planet = planet_dict[millennium_falcon['departure']]
        destination_planet = planet_dict[millennium_falcon['arrival']]
    else:
        mf_error = True
        start_planet = None
        destination_planet = None
        print('Departure or arrival planets are not in the database planet list')

    empire = {}
    if not em_path:
        em_path = 'empire.json'
    try:
        with open(em_path) as f_empire:
            empire = json.load(f_empire)
    except FileNotFoundError:
        em_error = True
        print('"empire.json" file does not exist')

    if empire and isinstance(empire['countdown'], int):
        countdown = empire['countdown']
    else:
        em_error = True
        countdown = None
        print('"Autonomy" is not an integer')

    danger = []
    for i in range(len(empire['bounty_hunters'])):
        if empire['bounty_hunters'][i]['planet'] in planets and isinstance(empire['bounty_hunters'][i]['day'], int):
            danger.append((planet_dict[empire['bounty_hunters'][i]['planet']], empire['bounty_hunters'][i]['day']))
        else:
            em_error = True
            print('bounty_hunter "planet" is not in the database planet list OR "day" value is not an integer')
    if mf_error or em_error or db_error:
        return None, mf_error, db_error, em_error
    else:
        capture_prob = falcon.find_safest_path(g, start_planet, destination_planet, autonomy, countdown, danger)
        return capture_prob, mf_error, db_error, em_error
