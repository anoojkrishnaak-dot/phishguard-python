import re
from urllib.parse import urlparse

import streamlit as st


# Page configuration
st.set_page_config(
    page_title="PhishGuard | URL Security Scanner",
    page_icon="🛡️",
    layout="centered"
)


# Application styling
st.markdown(
    """
    <style>
    .main {
        background-color: #0b1120;
    }

    .title {
        text-align: center;
        color: #38bdf8;
        font-size: 42px;
        font-weight: bold;
    }

    .subtitle {
        text-align: center;
        color: #cbd5e1;
        font-size: 17px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# URL detection function
def check_url(url):
    suspicious_signals = []
    score = 0

    url = url.strip()

    if not url:
        return "UNKNOWN", 0, ["Please enter a URL."]

    # Add a scheme for parsing if one is missing
    parsed_url = urlparse(
        url if "://" in url else "https://" + url
    )

    hostname = parsed_url.hostname or ""
    full_url = url.lower()

    # Check URL format
    if not hostname or "." not in hostname:
        suspicious_signals.append("Invalid or unusual domain format")
        score += 2

    # Check HTTPS
    if not url.lower().startswith("https://"):
        suspicious_signals.append("HTTPS is not explicitly used")
        score += 1

    # Check IP address instead of domain name
    if re.match(r"^\d{1,3}(?:\.\d{1,3}){3}$", hostname):
        suspicious_signals.append("URL uses an IP address as its host")
        score += 2

    # Check suspicious keywords
    keywords = [
        "login",
        "verify",
        "account",
        "password",
        "update",
        "secure",
        "banking",
        "signin",
        "wallet",
        "confirm"
    ]

    found_keywords = [
        word for word in keywords if word in full_url
    ]

    if len(found_keywords) >= 3:
        suspicious_signals.append(
            "Several sensitive keywords appear in the URL"
        )
        score += 2
    elif len(found_keywords) >= 1:
        suspicious_signals.append(
            "URL contains sensitive keywords: "
            + ", ".join(found_keywords)
        )
        score += 1

    # Check for @ symbol
    if "@" in parsed_url.netloc:
        suspicious_signals.append(
            "URL contains an @ symbol in its authority section"
        )
        score += 2

    # Check excessive subdomains
    if len(hostname.split(".")) > 4:
        suspicious_signals.append(
            "Domain contains an unusually large number of parts"
        )
        score += 1

    # Check URL length
    if len(url) > 100:
        suspicious_signals.append("Unusually long URL")
        score += 1

    # Check URL shorteners
    shorteners = [
        "bit.ly",
        "tinyurl.com",
        "t.co",
        "is.gd",
        "ow.ly"
    ]

    if any(hostname == domain or hostname.endswith("." + domain)
           for domain in shorteners):
        suspicious_signals.append(
            "URL uses a link-shortening service"
        )
        score += 1

    # Classify based on heuristic score (three categories)
    if score >= 4:
        result = "HIGHER RISK"
    elif score >= 2:
        result = "SUSPICIOUS"
    else:
        result = "LOWER RISK"

    if not suspicious_signals:
        suspicious_signals.append(
            "No warning signs detected by these basic checks"
        )

    return result, score, suspicious_signals


# Application interface
st.markdown(
    '<div class="title">🛡️ PhishGuard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Phishing URL Detection System'
    '</div>',
    unsafe_allow_html=True
)

st.write("")
st.info(
    "Check a URL for common phishing warning signs. "
    "This tool uses basic rules, not a trained machine-learning model."
)

url_input = st.text_input(
    "Enter a website URL",
    placeholder="https://example.com"
)

if st.button("🔍 Scan URL", use_container_width=True):
    if not url_input.strip():
        st.warning("Please enter a URL before scanning.")
    else:
        result, score, signals = check_url(url_input)

        st.subheader("Scan Results")

        if result == "HIGHER RISK":
            st.error("🚨 Higher Risk: Multiple warning signs detected")
        elif result == "SUSPICIOUS":
            st.warning("⚠️ Suspicious: Some warning signs detected")
        elif result == "LOWER RISK":
            st.success("✅ Lower Risk: Few warning signs detected")
        else:
            st.info("Unable to assess this URL.")

        st.metric("Heuristic Risk Score", score)

        st.write("**Warning signs:**")

        for signal in signals:
            st.write(f"- {signal}")

        st.caption(
            "A low score does not prove a website is safe. "
            "Do not enter passwords or banking details on "
            "websites you do not trust."
        )

with st.expander("🧪 Sample URLs to test"):
    st.write("**Lower Risk**")
    st.code("https://www.wikipedia.org\nhttps://github.com")
    st.write("**Suspicious**")
    st.code("http://bit.ly/3xYzAbC\nhttp://example-store.com/login")
    st.write("**Higher Risk**")
    st.code(
        "http://192.168.1.10/secure-login/verify-account\n"
        "http://paypal.com@secure-login.verify-account.example.com/confirm"
    )

st.divider()

st.markdown("### 🔐 Safety Tips")
st.write("- Check the domain name carefully.")
st.write("- Avoid suspicious links sent by unknown people.")
st.write("- Never share passwords or OTPs through unexpected links.")
st.write("- Use a trusted security service to investigate suspicious websites.")

st.caption("PhishGuard | Educational Cybersecurity Project")
