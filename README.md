# kml-route-with-time-markers
Script to add markers into a kml file with a route given the start time and the goal time. The idea is to take a kml file (in this case of a half marathon) and based on the `start_time` of the run, an estimated `goal_time` it will take to run the route (in minutes) and the desired `interval` (let's say 5 minutes), create a new kml file with map markers marking the points at which the runner will be every `interval` minutes.
The usage is as follows

### Initialize project
install [poetry](https://python-poetry.org/docs/)

`curl -sSL https://install.python-poetry.org | python3 -`

and in project dir do:
```
python -m venv .venv
source .venv/bin/activate
poetry install
```

### Usage
`python code/add-markers-to-route.py --input_file data/input/helsinki-half-route.kml --goal_time 105 --start_time 08:15 --interval 5`

### Input
![Screenshot 2023-06-14 at 16 04 10](https://github.com/adamhrin/kml-route-with-time-markers/assets/35726498/ad0c5453-67f4-471a-aadd-5c2e06263393)

### Output
![Screenshot 2023-06-14 at 16 05 02](https://github.com/adamhrin/kml-route-with-time-markers/assets/35726498/d801827c-6d13-453f-812c-8e23300c53d0)
