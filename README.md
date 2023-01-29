# Arma 3 market dashboard
 A simple market dashboard for the [ARMA 3](https://arma3.com) server [LIVEYOURLIFE](https://www.lyl.gg).
 ![grafik](https://user-images.githubusercontent.com/43930246/215349585-e494a3a1-b9f5-4de8-a8e0-8ac9bc1e9fa5.png)

## Installation
First you have to install the dependencys with the following command:
```console
foo@bar:~$ pip install -r requirements.txt
```
If you get this error: 
```error
ImportError: Unable to import required dependencies: numpy
```
Try this: 
```console
foo@bar:~$ sudo apt-get install libatlas-base-dev
```
After that you are ready to execute with: 
```console
foo@bar:~$ python3 app.py <Your cookie>
```
### Finding your cookie
The appication needs your login cookie from the [LIVEYOURLIFE](https://www.lyl.gg) website because the market data is only available as a logged in user. 

- Step 1: Go to the website and log in
- Step 2: Press F12
- Step 3: Go to "Web-Storage"
- Step 4: Click on "Cookies" then on "https://www.lyl.gg/"
- Step 5: Copy the value of the entry "wsc_267ea4_cookieHash"

Voilà there you have your cookie 🍪

![Arma3 dashboard](https://user-images.githubusercontent.com/43930246/215344445-e0e59e3b-97dc-4df3-8e09-7a9e13830d66.jpg)

## Setup 
I personally run the dashboard on my raspberry pi. But running it locally for a few hours should also be no problem. 

## Usage 

  ```console
usage: app.py [-h] [-i INTERVAL] cookie

A visualisation of market data fetched from the website of the arma 3 server lyl.

positional arguments:
  cookie                The value of the wsc_267ea4_cookieHash from the
                        request to https://www.lyl.gg/lyl-api/arma-dashboard.php.

optional arguments:
  -h, --help            show this help message and exit
  -i INTERVAL, --interval INTERVAL
                        Sets the interval in minutes in which new data is
                        fetched from the website. (default is 5)
```                      
###### Example
```console
foo@bar:~$ python3 app.py -i 10 f65d9a73f116a92a20afb641b599dc1dc6a39f63
```
Congratulation you now can access the dashboard 🎉<br>
Just go to http://0.0.0.0:8080/ if you run the app local. <br>
Otherwise go to http://\<Ip of your server\>:8080/
