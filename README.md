# Starwars
Starwars code challenge

## The approach

The problem is a bit similar to Dijkstra’s algorithm. It is similar to finding the shortest path between two cities on google maps with some obstacles on the way and a deadline. 

I thought of each planet as a node in a graph, and the distance between the planets as weights of the edges of this graph. 

Then created a matrix of these distances with the indexes being planets. 

## How to run 

In this code, I used Flask, HTML, and CSS for the front-end and Python, and SQLite for the back-end. 

To run the code in the browser:

1- run the app.py file:     $ python3 app.py

This will run a flask app with debugger ON which reflects real-time code changes to the browser. 

2- Access http://localhost:5000/upload on your browser. 

3- Upload the “empire.json” file 

4- Press the “See Results” button to see the final result. 

To run the code from the command line:

$ python3 cli.py millennium-falcon.json empire.json



Below is the explanation of each file and the variables in them. 

## app.py
"app.py" uses flask to run python codes and display them on the browser. 

The “upoad_file” function calls for “index.html” and the user is shown an upload button to upload the "empire.json" file. 

After pressing the upload button, the “Uploader” function is called and it checks the file name and extension. If it is “empire.json” and if a previous file exists inside the folder, the old file will be deleted and the new file will be saved. Otherwise, an error message will be displayed.

If the "empire.json" file was uploaded successfully, a “See Results” button will be displayed which will go to the "results.html" file and calls the “get_result” function.

This function gets the final “odds of being captured percentage” and some errors from the "get_data" function of the "resources.py" file (which will be explained later) and show the percentage. If errors exist, error messages will appear. 

The flask app has a "static" folder to store images and CSS data and a "templates" folder to store HTML files. 

## resources.py
This file reads 2 JSON files and accesses the SQLite database. 

1- Try to open the "millennium-falcon.json" file. It checks if the file exists in the same folder and also checks its contents such as if “autonomy” is an integer, if "departure" and "arrival" planets exist in the database planet list.

If there is something wrong appropriate error message will be displayed in the console and the “mf_error” variable become “True” so that an error message be displayed in the web browser too. 

2- Access the SQLite database, read all rows of data from the “ROUTES” table, and put them inside the “path_list” variable. If can not access the database, set "db_error" to "True". 

From the "path_list" put all planet names inside a list and use “OrderDict” to get the unique parameters. 

Assigned an integer to each planet name, so instead of using strings, later on, we can deal with integers starting from 0. 

Use the “Graph” class from the "falcon.py" file and create a matrix of distances between planets. If two planets are not connected put -1 in the matrix. 

3- Open the "empire.json" file and check if it exists, and check the file context for errors. 
If errors exist, set "em_error" to True. 

Finally, If any of the errors are "True", return "None" as the result and if not, call for the "find_safest_path" function from the "falcon.py" file to find the best path and the probability of being captured. 

## falcon.py

Thinking about how google maps works and using Dijkstra’s algorithm, I used PriorityQueue to store and then access routes step by step. 

The attributes put inside the queue are (route, total_dist, dangerous_day, days_traveled) where "route" and "dangerous_day" are lists and "total_dist" and "days_traveled" are integers. 

Imagine we start from planet 0 and the destination is planet 3 considering: 

Tatooine : 0 , Hoth : 1 , Dagobah : 2 , Endor : 3

First, we add the start planet to the route list. ([0], 0, [], 0)

Then we check the matrix of distances to see which planets are connected to planet 0. From the matrix, we can see that Tatooine to Hoth distance is 6 days. 

If the "distance" is bigger than "autonomy", we ignore this path and go to the next. 

If the "distance" is equal to the "autonomy" we add the "distance" to "total_dist". The spaceship has to refuel, therefore we add 1 to the "total_dist". But if the arrival planet is the destination do not add this 1. 

Also set "days_traveled" to 0. This variable is used to track how many days the ship has traveled on its fuel, so we know how many more days it can travel before refueling. 

If the "distance" is less than "autonomy", add "distance" to "total_dist" and "days_traveled". 

If "total_dist" becomes larger than “countdown” this path is impossible so we continue to the next path. 

To check which days bounty hunters might capture the ship, check if the arrival day on each planet is the same day as the bounty hunters are there, add that day to the "dangerous_day" list. If the ship had refueled on some planet, the “refuel” variable becomes "True" and we add the next day also to the "dangerous_day" if bounty hunters are there. 

Add the visited planet to the "route" list, and then the whole tuple (route, total_dist, dangerous_day, days_traveled) to the queue. 

At the same time, in the while loop, check if the last planet visited in the "route" is the destination planet. If so, add the tuple to another PriorityQueue called “paths”. 

At the end of the function, check “paths” one by one to find the one with the least number of "dangerous_days" and set it to the min_capture_days. 
At the same time, compare the "counter" and "total_dist" to see if "total_dist" is less than the counter. 

If “total_dist” is smaller than “counter”, it means that the spaceship can wait on the departure planet or other planets to avoid bounty hunters. 

By checking the exact days of bounty hunters on "dangerous_days" plus the difference between "total_dist" and "counter" can see if it's possible for the ship to wait and avoid the enemy. 

Finally, having the minimum number of days can show the percentage of being captured. 

## cli.py 

This file is to run the code from the command line. It sets the path to the 2 JSON files and calls for the “get_data” function of the resources.py file. It prints out the percentage of saving the galaxy in the command line. 

To run : $ python3 cli.py millennium-falcon.json empire.json

 
## Example (same one as the question):

Let us say we have 4 planets each assigned an integer as follows. 

Tatooine : 0 , Hoth : 1 , Dagobah : 2 , Endor : 3

The distance is as follows: 

**[universe.db]** 
| ORIGIN   | DESTINATION | TRAVEL_TIME |
|----------|-------------|-------------|
| Tatooine | Dagobah     | 6           |
| Dagobah  | Endor       | 4           |
| Dagobah  | Hoth        | 1           |
| Hoth     | Endor       | 1           |
| Tatooine | Hoth        | 6           |


Distance matrix will be like:
 
| Indexes | 0 | 1 | 2 | 3 |
|---------|---|---|---|---|
| 0 | -1 | 6 | 6 | -1 |
| 1  | 6 | -1 | 1 | 1 |
| 2  | 6 | 1 | -1 | 4 |
| 3  | -1 | 1 | 4 | -1 |


**[millennium-falcon.json]** 
```
{
  "autonomy": 6,
  "departure": "Tatooine",
  "arrival": "Endor",
  "routes_db": "universe.db"
}
```

**[empire.json]** 
```
{
  "countdown": 12, 
  "bounty_hunters": [
    {"planet": "Hoth", "day": 6 }, 
    {"planet": "Hoth", "day": 7 },
    {"planet": "Hoth", "day": 8 }
  ]
}
```

For example, if we have a queue path ([0,1,2,3], 12, [6,7], 5) it means that the route is from Tatooine to Hoth (6 days + 1 refuel), to Dagobah (1 day), to Endor (4days). In total it takes 12 days. Bounty hunters are in Hoth on day 6 and 7 so these are added to dangerous_days. After refueling, traveled 1+4=5 days so last parameter is 5. 



