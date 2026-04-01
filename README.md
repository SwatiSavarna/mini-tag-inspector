# Tracking Pixel Demo (Learning Project)


This is a small project I built to understand how tracking pixels actually work behind the scenes,especially how much information gets collected from something as simple as loading an image.





## Project Structure

```
mini_tag_inspector/
├── app.py            # Flask backend (serves pixel + logs data)
├── index.html        # Dashboard (explains + shows captured data)
├── email.html        # Sample email that triggers the pixel
└── requirements.txt
```

---



## How to Run



```bash
# install dependencies
pip install -r requirements.txt

# run the server
python app.py
```


Then open:
* http://localhost:5001 → dashboard
* http://localhost:5001/email → sample email
* http://localhost:5001/pixel.png → tracking pixel
* http://localhost:5001/api/logs → raw logs
* http://localhost:5001/api/clear → clear logs

---

## What this project shows

When the email page loads, it automatically requests a 1×1 pixel image from the server.


Even though it’s just an image request, the server still receives a lot of information through HTTP headers.

The dashboard updates every few seconds to show what gets captured.

---

## Data captured (from just one request)

* IP address
* Browser and OS (based on user-agent)
* Language preferences
* Timestamp
* Referrer (where the request came from)
* Query params (like user ID or campaign ID)


---

## Why this works

Browsers automatically send a bunch of headers with every request — even for something as simple as an image.

So even without JavaScript or cookies, you can still get useful (and sometimes sensitive) information.

---

## Things I learned while building this

* Tracking doesn’t always need cookies or scripts
* HTTP headers alone reveal a lot
* Email tracking is basically this exact mechanism
* Small implementation mistakes can break things easily 



---

## Final thoughts

This is a basic implementation just to understand the concept.
There’s definitely a lot more complexity in real-world tracking systems.
