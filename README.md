## Ping Test Utility Tools
> Simple Python Program to visualize the ping result
> Compatitable to Python 3.6 or above

### Functions
- Plot the ping response time graph in real time
- Save the ping test result in term of graph (in .png) and detail result (in .csv)
- Set a timer for the ping test
- Set the buffer size of the ping test

### Build and Run
-  Install Python 3.6 or above and virtual env in prior
-  Create an virtual environment
```
virtualenv venv
```
- Activate the virtual env by the following command
```
/venv/Scripts/activate
```
- Install the required packages
```
pip install matplotlib
```
- Run the program
```
python ping_os.py <host> -d <directory of the log file> -t <duration of the test>
-l <buffer size> -v <verbose>
``` 
