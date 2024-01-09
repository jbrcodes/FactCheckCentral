# Fact Check Central

A demo that scrapes the latest fact-checks from
several fact-checking websites.


## Installation

### 1. Clone Repo

```
git clone https://github.com/jbrcodes/fcc
```

### 2. Create Virtual Environment

```
cd foobar
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```


### 4. Install Browser for Playwright

```
playwright install chromium
```

No need to install other browsers...


### 5. Create a Database

```
createdb fcc
```

### Modify `/instance/config_dev.py`

### 6. Initialize Database

```
flask create
flask seed
```

## Running

### 1. Run a Scraper

```
flask scrape politifact
```

### 2. Start the Web Server

```
flask run
```