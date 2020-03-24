## Ping Test Utility Tools
> Simple Python Program to visualize the ping result
>
> Compatitable to Python 3.6 or above

### Functions
- Plot the ping response time graph in real time
- Save the ping test result in term of graph (in .png) and detail result (in .csv)
- Set a timer for the ping test
- Set the buffer size of the ping test

### Demo
Real-Time Graph

![demo-graph](https://github.com/JonathanChan1234/Ping-Test-Utilities/blob/master/demo.gif)


Log File

| sequence | response time | ttl | start_time          | end_time            | log                                                                                                                                                                                                                                                                 |
|----------|---------------|-----|---------------------|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0        | 1             | 64  | 2020/03/24 10:48:40 | 2020/03/24 10:48:40 | Pinging 8.8.8.8 with 32 bytes of data:Reply from 8.8.8.8: bytes=32 time=7ms TTL=55Ping statistics for 8.8.8.8:    Packets: Sent = 1, Received = 1, Lost = 0 (0% loss),Approximate round trip times in milli-seconds:    Minimum = 7ms, Maximum = 7ms, Average = 7ms |




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
