# Report6-OleksiiLeshchenko
Report6-OleksiiLeshchenko is a small CLI for viewing racer's results.
It can show all racers info in ascending (or descending) order  or show one racer's info. Also, if the racer's info has mistake, script will show you it in separate block under valid results.

## Installation

Install and update using `pip`:


    $ pip install -i https://test.pypi.org/simple/ report6-OleksiiLeshchenko
    
## Usage
Since installing you need to place data files in "data" folder. Examples of needed data format you can see in "data" folder.
After loading the files you can run the script in terminal from root directory in two ways:


    $ report --files <folder_path> ls [asc|desc]

  - report - command to execute the script
  - --files (or -f for short) - option specified that next str will be path to data
  - <folder_path> - path to data. The path is "data" in our case
  - ls - subcommand to show full race's info
  - [asc|desc] - argument for specifying the sorting direction of the results (default order is asc)


    $ report --files <folder_path> driver "<driver_full_name>"
    

  - report - command to execute the script
  - <folder_path> - path to data. The path is "data" in our case
  - driver - subcommand to show one racer's info
  - <driver_full_name> - racer's full name, for example, Fernando Alonso

## Examples
$ report --files data ls desc
 ```python
16. Kevin Magnussen      | HAAS FERRARI     | 0:01:13.393
15. Lance Stroll      | WILLIAMS MERCEDES     | 0:01:13.323
14. Marcus Ericsson      | SAUBER FERRARI     | 0:01:13.265
13. Brendon Hartley      | SCUDERIA TORO ROSSO HONDA     | 0:01:13.179
...
2. Sebastian Vettel      | FERRARI     | 0:01:04.415
------------------------------------------------------------------------
1. Augusto Pinochet      | VAZ 2101     | 0:01
------------------------------------------------------------------------
Daniel Ricciardo race time is incorrect — finish 2018-05-24 12:11:24.067000 before start 2018-05-24 12:14:12.054000
Lewis Hamilton race time is incorrect — finish 2018-05-24 12:11:32.585000 before start 2018-05-24 12:18:20.125000
 ```
 $ report -f data ls
 ```python
1. Augusto Pinochet      | VAZ 2101     | 0:01
2. Sebastian Vettel      | FERRARI     | 0:01:04.415
3. Valtteri Bottas      | MERCEDES     | 0:01:12.434
4. Stoffel Vandoorne      | MCLAREN RENAULT     | 0:01:12.463
...
15. Lance Stroll      | WILLIAMS MERCEDES     | 0:01:13.323
------------------------------------------------------------------------
16. Kevin Magnussen      | HAAS FERRARI     | 0:01:13.393
------------------------------------------------------------------------
Daniel Ricciardo race time is incorrect — finish 2018-05-24 12:11:24.067000 before start 2018-05-24 12:14:12.054000
Lewis Hamilton race time is incorrect — finish 2018-05-24 12:11:32.585000 before start 2018-05-24 12:18:20.125000
 ```
 
$ report -f data driver "Fernando Alonso"
 ```python
Fernando Alonso      | MCLAREN RENAULT     | 0:01:12.657000
 ```

##Testing
To run test, execute command "cd tests & pytest" in terminal from the root directory







