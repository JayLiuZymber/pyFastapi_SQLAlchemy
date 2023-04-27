# Getting Started with Uvicorn App

## 1 Setup
### 1.1 Setup SQL
Create new 'erp' SQL database, run command in MySql:
### `create database erp charset=utf8;`
PS. Change database name. Open 'database.py' file and modify below code:
`... @127.0.0.1:3306/<database name>?charset=utf8"`

### 1.2 Change Account
Open 'database.py' and modify below code:
`... mysql+pymysql://<your account name>:<your password>@127.0.0.1 ...`

## 2 Startup
### 2.1 Startup Python
Setup python environment, you need run below on terminal:
### `$ .\.venv\Scripts\activate`

### 2.2 Startup Uvicorn
In the project directory, you can run below command of one:
### (1) `$ uvicorn main:app --reload`
### (2) `$ python main.py`
### (3) `$ py main.py`

Runs the app in the development mode.\
Open [http://localhost:8000](http://localhost:8000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

## Debug Mode
### Open 'main.py' file and Press F5 run

Runs the app in the debug mode.\
Open [http://localhost:8000](http://localhost:8000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

