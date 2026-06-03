import json
import random
import string
from pathlib import Path
import streamlit as st

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Vault Bank",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --gold:    #C9A84C;
    --gold-lt: #E8C97A;
    --dark:    #0D0D0D;
    --card:    #161616;
    --border:  #2A2A2A;
    --text:    #E8E0D0;
    --muted:   #7A7060;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--dark) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* App title */
.vault-title {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 900;
    letter-spacing: -1px;
    color: var(--gold);
    text-align: center;
    margin-bottom: 0;
    line-height: 1;
}
.vault-sub {
    font-size: 0.78rem;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: var(--muted);
    text-align: center;
    margin-bottom: 2rem;
}

/* Cards */
.bank-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.2rem;
}
.bank-card h3 {
    font-family: 'Playfair Display', serif;
    color: var(--gold);
    font-size: 1.2rem;
    margin-bottom: 0.5rem;
}

/* Divider */
.gold-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
    margin: 1.4rem 0;
}

/* User info row */
.info-row {
    display: flex;
    justify-content: space-between;
    padding: 0.45rem 0;
    border-bottom: 1px solid var(--border);
    font-size: 0.92rem;
}
.info-label { color: var(--muted); }
.info-val   { color: var(--text); font-weight: 500; }

/* Balance badge */
.balance-badge {
    background: linear-gradient(135deg, #1A1500, #2A2000);
    border: 1px solid var(--gold);
    border-radius: 8px;
    padding: 0.9rem 1.4rem;
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    color: var(--gold-lt);
    text-align: center;
    margin: 1rem 0;
}
.balance-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.72rem;
    letter-spacing: 0.2em;
    color: var(--muted);
    text-transform: uppercase;
    display: block;
    margin-bottom: 0.3rem;
}

/* Success / error banners */
.msg-success {
    background: #0D1F0D; border-left: 3px solid #4CAF50;
    border-radius: 6px; padding: 0.7rem 1rem;
    color: #A5D6A7; font-size: 0.9rem; margin: 0.6rem 0;
}
.msg-error {
    background: #1F0D0D; border-left: 3px solid #EF5350;
    border-radius: 6px; padding: 0.7rem 1rem;
    color: #EF9A9A; font-size: 0.9rem; margin: 0.6rem 0;
}
.msg-warn {
    background: #1F1800; border-left: 3px solid var(--gold);
    border-radius: 6px; padding: 0.7rem 1rem;
    color: var(--gold-lt); font-size: 0.9rem; margin: 0.6rem 0;
}

/* Streamlit input overrides */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    background: #1C1C1C !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 6px !important;
}
[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label {
    color: var(--muted) !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.05em !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #1A1400, #2A2000) !important;
    color: var(--gold) !important;
    border: 1px solid var(--gold) !important;
    border-radius: 6px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    padding: 0.5rem 1.4rem !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: var(--gold) !important;
    color: var(--dark) !important;
}

/* Nav pills */
.nav-wrap {
    display: flex; flex-wrap: wrap; gap: 0.5rem;
    justify-content: center; margin-bottom: 1.5rem;
}
.nav-pill {
    background: var(--card); border: 1px solid var(--border);
    color: var(--muted); border-radius: 50px;
    padding: 0.38rem 1rem; font-size: 0.8rem;
    cursor: pointer; transition: all 0.2s;
    font-family: 'DM Sans', sans-serif;
    letter-spacing: 0.05em;
    text-decoration: none;
}
.nav-pill.active, .nav-pill:hover {
    border-color: var(--gold); color: var(--gold-lt); background: #1A1400;
}

/* Selectbox override */
[data-testid="stSelectbox"] > div > div {
    background: #1C1C1C !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
}
</style>
""", unsafe_allow_html=True)


# ── Bank backend (same logic, no input() calls) ───────────────────────────────
DATABASE = "database.json"

def _load():
    if Path(DATABASE).exists():
        with open(DATABASE) as f:
            return json.loads(f.read())
    return []

def _save(data):
    with open(DATABASE, "w") as f:
        f.write(json.dumps(data, indent=2))

def _gen_acc():
    alpha = random.choices(string.ascii_letters, k=8)
    num   = random.choices(string.digits, k=4)
    acc   = alpha + num
    random.shuffle(acc)
    return "".join(acc)

def _find(data, accno, pin):
    return [u for u in data if u["AccountNO."] == accno and u["pin"] == pin]

def create_user(name, age, email, pin):
    data = _load()
    if age < 12:
        return False, "Age must be 12 or older to open an account."
    if len(str(pin)) != 4:
        return False, "PIN must be exactly 4 digits."
    info = {
        "name": name, "age": age, "email": email,
        "AccountNO.": _gen_acc(), "pin": pin, "balance": 0
    }
    data.append(info)
    _save(data)
    return True, info["AccountNO."]

def deposit(accno, pin, amount):
    data = _load()
    users = _find(data, accno, pin)
    if not users:
        return False, "Invalid account number or PIN."
    if amount <= 0:
        return False, "Amount must be positive."
    users[0]["balance"] += amount
    _save(data)
    return True, users[0]["balance"]

def withdraw(accno, pin, amount):
    data = _load()
    users = _find(data, accno, pin)
    if not users:
        return False, "Invalid account number or PIN."
    if amount <= 0:
        return False, "Amount must be positive."
    if amount > users[0]["balance"]:
        return False, "Insufficient balance."
    users[0]["balance"] -= amount
    _save(data)
    return True, users[0]["balance"]

def get_details(accno, pin):
    data = _load()
    users = _find(data, accno, pin)
    if not users:
        return None
    return users[0]

def update_user(accno, pin, new_name, new_email, new_pin):
    data = _load()
    users = _find(data, accno, pin)
    if not users:
        return False, "Invalid account number or PIN."
    if new_name:  users[0]["name"]  = new_name
    if new_email: users[0]["email"] = new_email
    if new_pin:
        if len(str(new_pin)) != 4:
            return False, "New PIN must be exactly 4 digits."
        users[0]["pin"] = new_pin
    _save(data)
    return True, "Details updated successfully."

def delete_account(accno, pin):
    data = _load()
    users = _find(data, accno, pin)
    if not users:
        return False, "Invalid account number or PIN."
    data.remove(users[0])
    _save(data)
    return True, "Account deleted successfully."


# ── UI ────────────────────────────────────────────────────────────────────────
st.markdown('<div class="vault-title">VAULT</div>', unsafe_allow_html=True)
st.markdown('<div class="vault-sub">Private Banking System</div>', unsafe_allow_html=True)

PAGES = ["Create Account", "Deposit", "Withdraw", "View Details", "Update Details", "Delete Account"]
if "page" not in st.session_state:
    st.session_state.page = PAGES[0]

selected = st.selectbox("", PAGES, index=PAGES.index(st.session_state.page), label_visibility="collapsed")
st.session_state.page = selected

st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

# ── Helper: account + pin fields ──────────────────────────────────────────────
def acc_pin_fields(key_prefix):
    acc = st.text_input("Account Number", key=f"{key_prefix}_acc", placeholder="e.g. aB3xR7mZ1q2K")
    pin = st.number_input("PIN (4 digits)", min_value=0, max_value=9999,
                          step=1, key=f"{key_prefix}_pin", format="%04d")
    return acc.strip(), int(pin)

def msg(kind, text):
    cls = {"success": "msg-success", "error": "msg-error", "warn": "msg-warn"}[kind]
    st.markdown(f'<div class="{cls}">{text}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
page = st.session_state.page

# ── 1. Create Account ─────────────────────────────────────────────────────────
if page == "Create Account":
    st.markdown('<div class="bank-card"><h3>Open New Account</h3></div>', unsafe_allow_html=True)
    with st.form("create_form"):
        name  = st.text_input("Full Name")
        age   = st.number_input("Age", min_value=1, max_value=120, step=1)
        email = st.text_input("Email Address")
        pin   = st.number_input("Set PIN (4 digits)", min_value=0, max_value=9999, step=1, format="%04d")
        submit = st.form_submit_button("Open Account")

    if submit:
        if not name or not email:
            msg("error", "Please fill in all fields.")
        else:
            ok, result = create_user(name.strip(), int(age), email.strip(), int(pin))
            if ok:
                msg("success", f"✓ Account created! Your Account Number: **{result}**")
                st.markdown(f"""
                <div class="bank-card">
                  <div class="balance-badge">
                    <span class="balance-label">Account Number</span>
                    {result}
                  </div>
                  <p style="color:var(--muted);font-size:0.82rem;text-align:center;margin:0">
                    Save this number — you'll need it for all transactions.
                  </p>
                </div>""", unsafe_allow_html=True)
            else:
                msg("error", result)

# ── 2. Deposit ────────────────────────────────────────────────────────────────
elif page == "Deposit":
    st.markdown('<div class="bank-card"><h3>Deposit Funds</h3></div>', unsafe_allow_html=True)
    with st.form("deposit_form"):
        accno, pin = acc_pin_fields("dep")
        amount = st.number_input("Amount to Deposit (₹)", min_value=1, step=100)
        submit = st.form_submit_button("Deposit")

    if submit:
        ok, result = deposit(accno, pin, int(amount))
        if ok:
            msg("success", f"✓ ₹{amount:,} deposited successfully.")
            st.markdown(f"""
            <div class="balance-badge">
              <span class="balance-label">New Balance</span>
              ₹ {result:,}
            </div>""", unsafe_allow_html=True)
        else:
            msg("error", result)

# ── 3. Withdraw ───────────────────────────────────────────────────────────────
elif page == "Withdraw":
    st.markdown('<div class="bank-card"><h3>Withdraw Funds</h3></div>', unsafe_allow_html=True)
    with st.form("withdraw_form"):
        accno, pin = acc_pin_fields("wdr")
        amount = st.number_input("Amount to Withdraw (₹)", min_value=1, step=100)
        submit = st.form_submit_button("Withdraw")

    if submit:
        ok, result = withdraw(accno, pin, int(amount))
        if ok:
            msg("success", f"✓ ₹{amount:,} withdrawn successfully.")
            st.markdown(f"""
            <div class="balance-badge">
              <span class="balance-label">Remaining Balance</span>
              ₹ {result:,}
            </div>""", unsafe_allow_html=True)
        else:
            msg("error", result)

# ── 4. View Details ───────────────────────────────────────────────────────────
elif page == "View Details":
    st.markdown('<div class="bank-card"><h3>Account Details</h3></div>', unsafe_allow_html=True)
    with st.form("view_form"):
        accno, pin = acc_pin_fields("view")
        submit = st.form_submit_button("Fetch Details")

    if submit:
        user = get_details(accno, pin)
        if not user:
            msg("error", "No account found with those credentials.")
        else:
            st.markdown(f"""
            <div class="balance-badge">
              <span class="balance-label">Balance</span>
              ₹ {user['balance']:,}
            </div>
            <div class="bank-card">
              <div class="info-row"><span class="info-label">Name</span>       <span class="info-val">{user['name']}</span></div>
              <div class="info-row"><span class="info-label">Age</span>        <span class="info-val">{user['age']}</span></div>
              <div class="info-row"><span class="info-label">Email</span>      <span class="info-val">{user['email']}</span></div>
              <div class="info-row"><span class="info-label">Account No.</span><span class="info-val">{user['AccountNO.']}</span></div>
            </div>""", unsafe_allow_html=True)

# ── 5. Update Details ─────────────────────────────────────────────────────────
elif page == "Update Details":
    st.markdown('<div class="bank-card"><h3>Update Account Details</h3></div>', unsafe_allow_html=True)
    msg("warn", "Leave fields blank to keep existing values.")
    with st.form("update_form"):
        accno, pin = acc_pin_fields("upd")
        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
        new_name  = st.text_input("New Name (optional)")
        new_email = st.text_input("New Email (optional)")
        new_pin_raw = st.text_input("New PIN (optional, 4 digits)", max_chars=4, placeholder="leave blank to keep")
        submit = st.form_submit_button("Update Details")

    if submit:
        new_pin = int(new_pin_raw) if new_pin_raw.strip().isdigit() else None
        ok, result = update_user(accno, pin, new_name.strip(), new_email.strip(), new_pin)
        if ok:
            msg("success", f"✓ {result}")
        else:
            msg("error", result)

# ── 6. Delete Account ─────────────────────────────────────────────────────────
elif page == "Delete Account":
    st.markdown('<div class="bank-card"><h3>Close Account</h3></div>', unsafe_allow_html=True)
    msg("error", "⚠ This action is permanent and cannot be undone.")

    with st.form("delete_form"):
        accno, pin = acc_pin_fields("del")
        confirm = st.checkbox("I understand this will permanently delete my account.")
        submit  = st.form_submit_button("Delete Account")

    if submit:
        if not confirm:
            msg("warn", "Please check the confirmation box to proceed.")
        else:
            ok, result = delete_account(accno, pin)
            if ok:
                msg("success", f"✓ {result}")
            else:
                msg("error", result)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="gold-divider"></div>
<div style="text-align:center;color:var(--muted);font-size:0.72rem;letter-spacing:0.15em;text-transform:uppercase;padding-bottom:1rem;">
  Vault Bank · Secure · Private · Reliable
</div>
""", unsafe_allow_html=True)