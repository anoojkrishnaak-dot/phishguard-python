# 🛡️ PhishGuard — Phishing URL Detection System

PhishGuard checks a website URL for common phishing warning signs and sorts it into one of three categories: **Lower Risk**, **Suspicious**, or **Higher Risk**.

It uses simple, transparent rules (heuristics), not a trained machine-learning model. Every result shows exactly which warning signs were found.

> Educational cybersecurity project. A low score does **not** prove a website is safe.

## Live demo

Open `index.html` in any browser, or use the GitHub Pages link:
`https://anoojct877-prog.github.io/PhishguardIBM/`

## Two versions, same logic

| File | What it is | How to run |
|---|---|---|
| `index.html` | Standalone web app (HTML + CSS + JavaScript) | Open in a browser, no install |
| `app.py` | Streamlit web app (Python) | See below |

## Run the Streamlit version

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local address shown in the terminal (usually `http://localhost:8501`).

## How scoring works

Each warning sign adds points. The total decides the category.

| Check | Points |
|---|---|
| Invalid or unusual domain format | +2 |
| HTTPS not explicitly used | +1 |
| IP address used as the host | +2 |
| 1–2 sensitive keywords (login, verify, account, password, update, secure, banking, signin, wallet, confirm) | +1 |
| 3 or more sensitive keywords | +2 |
| `@` symbol in the authority section | +2 |
| More than 4 domain parts (many subdomains) | +1 |
| URL longer than 100 characters | +1 |
| Link-shortening service (bit.ly, tinyurl.com, t.co, is.gd, ow.ly) | +1 |

| Total score | Category |
|---|---|
| 0–1 | ✅ Lower Risk |
| 2–3 | ⚠️ Suspicious |
| 4 or more | 🚨 Higher Risk |

## Sample URLs to test

| URL | Expected result |
|---|---|
| `https://www.wikipedia.org` | Lower Risk (0) |
| `https://github.com` | Lower Risk (0) |
| `http://bit.ly/3xYzAbC` | Suspicious (2) |
| `http://example-store.com/login` | Suspicious (2) |
| `http://192.168.1.10/secure-login/verify-account` | Higher Risk (5) |
| `http://paypal.com@secure-login.verify-account.example.com/confirm` | Higher Risk (5) |

These are made-up test patterns, not real phishing sites.

## Project structure

```
PhishguardIBM/
├── index.html          # Standalone web version
├── app.py              # Streamlit version
├── requirements.txt    # Python dependency (streamlit)
├── PROJECT_REPORT.md   # Full project report
└── README.md           # This file
```

## Limitations

- Rule-based only; it can miss clever phishing URLs and can flag harmless ones.
- It looks only at the URL text. It does not visit the site, check domain age, or use blocklists.
- Not a replacement for a professional security service.

## Safety tips

- Check the domain name carefully.
- Avoid suspicious links sent by unknown people.
- Never share passwords or OTPs through unexpected links.
- Use a trusted security service to investigate suspicious websites.

## License

Educational use. Add a license of your choice (for example MIT) before reusing.
