# instacard
Send instagram post as a postcard




# Setup

Download project
```
git clone https://github.com/eruvanos/instacard.git
cd instacard
```

Create settings.py and add your credentials etc.
```python3
from instacard.model import Address

# Lob.com
LOB_API_KEY =
default_address = Address(
    name='',
    streetno='',
    city='',
    zip='',
    state='',
    country=''
)

# Instagram
USERNAME =
PASSWORD =

#DB
DB_URL = './db.json'

```

Install requirements
```
pip3 install -r requirements.txt
```

Start server
```
python3 -m instacard
```

Open your browser on `localhost:5000/<username>
