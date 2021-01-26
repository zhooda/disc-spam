# disc_spam

a simple webdriver discord spammer

## Usage

### Step 1:
```bash
$ git clone https://github.com/zhooda/disc_spam
$ cd disc_spam
$ pip3 install -r requirements.txt
```

### Step 2:

Edit the .env file with your desired settings and discord login information. You need to have the BROWSER, DISC_EMAIL, DISC_PASS, DISC_SERVER, DISC_CHANNEL, and TFA_ENABLED environment variables set in the .env file or this program will not work.

.env
```bash
# Supported browsers are chrome and firefox
BROWSER=chrome

# Your discord login information
DISC_EMAIL=discord@email.com
DISC_PASS=yourPasswordHere
DISC_SERVER="Monster Hunters Association"
DISC_CHANNEL="bot-commandos"

TFA_ENABLED=false
```

### Step 3:

- `ITERATIONS`: number of iterations you want to spam
- `INTERVAL`: time between messages (10s, 2m, 4h, 2d)
- `MESSAGE`: string message (wrap in "" if your message has spaces)

```bash
# python3 main.py <ITERATIONS> <INTERVAL> <MESSAGE>
$ python3 main.py 100 5s "this is a message"
```