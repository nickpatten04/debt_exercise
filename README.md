# debt_exercise


### Instructions
- To see the output of the exercise, you need just run main.py in the module directory. This will output out the debt
table in json lines format to the console.

### Overview
- From a high level overiew, I spent most of my time writing the objects to pull data from the APIs. I decided to
write the solution in a way that allows us to easily spin up new objects if and when we need the same functionality for
additional tables. I accomplished this by creating base Table/TableRow object that will be inhereted from child classes.
From there, pulling the api data and writing it to a json format was relatively straightforward with the requests and
json libraries.

### Process
- As far as process goes, I approached this challenge from a reusability standpoint. I wanted to create a solution that
not only solved the problem but would allow for seemless implementation methods in the future. All we would really have
to do at this point for additional tables is create some objects with methods to extract data. All the underlying iterative
and database logic would be held in the Table/TableRow classes.
