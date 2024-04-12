## Lab 5 - Websockets
CLI application to send request and parse websites

### Setup
To get the functionality of this code you need:

1. Clone Repository:

```
git clone https://github.com/maria-afteni/PW_Lab5.git
```

2. Install all needed requirements:

```
pip install -r requirements.txt
```

3. Create executable script:

```
pyinstaller --onefile go2web.py
```

4. Go to dist folder

```
cd dist
```

5. Run application with neede command:
```
./go2web.exe -h/-u/-s
```

## Commands

```
go2web -u <URL> # make HTTP request to specified website and get the parsed information
go2web -s <search-term> # make an HTTP request to google and get top 10 results
go2web -h # show help information
```

## Demo
![](https://github.com/maria-afteni/PW_Lab5/blob/requests/additional/go2web.gif)
