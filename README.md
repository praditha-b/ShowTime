<h1 align="center">
  ShowTime  
</h1>

<h5 align="center">A comprehensive movie ticket booking system</h5>
<h6 align="center">Written during my 5th semester BE for a course specified mini project in Database Management Systems (DBMS).</h6>

<p align="center">
The system follows a 3-tier architecture, with a web based front end, Python + Flask as the HTTP server and router, and SQLite3 server for the database. SQLAlchemy Python connector is used to query the SQLite3 server, which executes the queries. All HTTP requests to Flask are made via encrypted POST messages.
</p>

## 

<img src="/Project/website/static/images/demo.gif"/>

## Documentation

 ####  [PROJECT REPORT](https://drive.google.com/file/d/1UJhLTAFmzoYCfg5GVcOOJIe0z-G0rvEO/view?usp=sharing)


## Run Locally

Clone the project

```bash
  git clone https://github.com/praditha-b/ShowTime
```

Go to the project directory

```bash
  cd Project
```

Install dependencies

```bash
 pip install flask
 pip instal flask-login
 pip install flask-sqlalchemy

```

Start the server

```bash
  python main.py
```




