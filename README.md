<p align="center">
  <img src="https://github.com/bksahu/Elit-Hunter/raw/master/static/logo.png" alt="logo" width="65%"/>
</p>

Live at: https://elit-hunter.herokuapp.com/

### Installation
```
$ git clone git@github.com:bksahu/Elit-Hunter.git
$ cd Elit-Hunter
$ pip install -r requirements.txt
```

### To start the local server
```
$ gunicorn app:app -b 127.0.0.1:5000
```
To see your website running, open your browser and enter this URL: http://localhost:5000

### To run the hunter to find new links
```
$ python hunter.py
```
