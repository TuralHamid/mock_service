###Follow Instructions to run the project properly

* Make sure Python is installed in your machine
  * `python --version`


* Assign your port number to value of `port` in **config.json** file
  * `"port":"YOUR_PORT_NUMBER"`

  
* Assign same port number to value of `SERVER_PORT` variable in **request.js** file
  * `var SERVER_PORT = YOUR_PORT_NUMBER`


* Write your server IP address in string format to value of `SERVER_IP` variable in **request.js** file
  * `var SERVER_IP = "YOUR_SERVER_IP"`


* Change **run_mock_service.sh** file permission to be able to run it
  * Firstly, go to project directory, then run command below
  * `chmod u+x run_mock_service.sh`


* Run **run_mock_service.sh** file to start server
  * `./run_mock_service.sh`


* In order to stop server, run command below
  * `fuser -k YOUR_PORT_NUMBER/tcp`