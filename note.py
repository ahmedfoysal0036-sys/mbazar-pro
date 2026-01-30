st.query_params.clear()
import streamlit as st
import pandas as pd
import os
from datetime import datetime
from cryptography.fernet import Fernet
import google.generativeai as genai

# --- CONFIGURATION & ENCRYPTION ---
# (Master Faisal's private key for the Vault)
KEY = b'vU0_uB5eY3W3X6_zN9kL8mP1qR4tV7wY9zB2xK5mN8o='
cipher = Fernet(KEY)
BAZAR_FILE = "M_Bazar_Pro.csv"
VAULT_FILE = "Planetary_Vault.txt"
UPLOAD_DIR = "Vault_Files"
JOB_FILE = "Job_Log.txt"
API_KEY = "AIzaSyCCs6NikHG9DEUbmghkSRxJL2Y091l2DHY"

# --- SYSTEM DIRECTORIES ---
if not os.path.exists(UPLOAD_DIR): os.makedirs(UPLOAD_DIR)

# --- AI SETUP ---
try:
    genai.configure(api_key=API_KEY)
    ai_model = genai.GenerativeModel('gemini-1.5-flash')
    AI_READY = True
except:
    AI_READY = False

# --- CORE FUNCTIONS ---
def encrypt(t): return cipher.encrypt(t.encode()).decode()
def decrypt(t):
    try: return cipher.decrypt(t.encode()).decode()
    except: return "Decryption Error"

def get_bazar_data():
    if not os.path.exists(BAZAR_FILE):
        return pd.DataFrame(columns=["Month", "Item", "Price", "Qty", "Unit", "Person", "Total", "Date"])
    return pd.read_csv(BAZAR_FILE)

# --- UI STYLE ---
st.set_page_config(page_title="Ultimate Gallery - Master Faisal", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; }
    .header-box { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
    .card { background: white; border-radius: 10px; padding: 15px; border-left: 5px solid #1e3c72; margin-bottom: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- AUTH SYSTEM ---
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<div class="header-box"><h1>🛡️ Ultimate Gallery Admin</h1><p>Created by Ahmed Faisal</p></div>', unsafe_allow_html=True)
    u = st.text_input("Identity", placeholder="Enter Username")
    p = st.text_input("Access Code", type="password", placeholder="Enter Password")
    if st.button("🚀 AUTHORIZE SYSTEM"):
        if u == "faisal" and p == "1234":
            st.session_state.auth = True; st.rerun()
else:
    # --- SIDEBAR (AI & SECURITY) ---
    st.sidebar.title("🤖 Master AI Assistant")
    if AI_READY:
        user_q = st.sidebar.text_input("Ask for market info:")
        if st.sidebar.button("Ask Gemini"):
            with st.sidebar:
                try:
                    res = ai_model.generate_content(f"Answer briefly in Bangla: {user_q}")
                    st.success(res.text)
                except: st.error("AI Busy.")
    
    st.sidebar.markdown("---")
    hero_check = st.sidebar.text_input("Identity Challenge (Hero)", type="password")
    if st.sidebar.button("🔴 Logout"): st.session_state.auth = False; st.rerun()

    # --- MAIN DASHBOARD ---
    if hero_check.lower() == "tony":
        st.markdown('<div class="header-box"><h1>🌌 Master Dashboard V12.0</h1></div>', unsafe_allow_html=True)
        tabs = st.tabs(["🛒 M.Bazar Tracker", "🔒 Data Vault", "📂 Media Files", "📅 Daily Jobs"])

        # --- TAB 1: M.BAZAR ---
        with tabs[0]:
            st.subheader("🛒 Market Inventory Tracker")
            df_b = get_bazar_data()
            months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
            
            c1, c2, c3 = st.columns(3)
            sel_month = c1.selectbox("Filter Month", months, index=datetime.now().month-1)
            sel_person = c2.text_input("Buyer", value="Ahmed Faisal")
            month_df = df_b[df_b["Month"] == sel_month]
            c3.metric(f"Spent in {sel_month}", f"৳ {month_df['Total'].sum():,.2f}")

            with st.form("bazar_form", clear_on_submit=True):
                col1, col2, col3, col4 = st.columns(4)
                it_name = col1.text_input("Item")
                it_price = col2.number_input("Price/Unit", min_value=0.0)
                it_qty = col3.number_input("Qty", min_value=0.1)
                it_unit = col4.selectbox("Unit", ["KG", "GM", "Litre", "Piece", "Packet"])
                if st.form_submit_button("Add to List"):
                    total = it_price * it_qty
                    if it_unit == "GM": total = (it_price / 1000) * it_qty
                    new_row = pd.DataFrame([[sel_month, it_name, it_price, it_qty, it_unit, sel_person, total, datetime.now().strftime("%Y-%m-%d")]], columns=df_b.columns)
                    df_b = pd.concat([df_b, new_row], ignore_index=True)
                    df_b.to_csv(BAZAR_FILE, index=False); st.rerun()

            st.dataframe(month_df, use_container_width=True)
            if not month_df.empty:
                del_item = st.selectbox("Select Item to Remove", month_df.index, format_func=lambda x: f"{month_df.loc[x, 'Item']} ({month_df.loc[x, 'Date']})")
                if st.button("🗑️ Delete Selected Item"):
                    df_full = get_bazar_data()
                    df_full = df_full.drop(del_item)
                    df_full.to_csv(BAZAR_FILE, index=False); st.rerun()

        # --- TAB 2: VAULT (ENCRYPTED) ---
        with tabs[1]:
            st.subheader("🔒 Planetary Vault (AES Encryption)")
            with st.expander("➕ Store New Secret"):
                v_type = st.selectbox("Category", ["Password", "Bank Info", "Personal Note"])
                v_data = st.text_area("Secret Content")
                if st.button("Encrypt & Save"):
                    with open(VAULT_FILE, "a") as f: f.write(f"{v_type}|{encrypt(v_data)}|{datetime.now().strftime('%Y-%m-%d')}\n")
                    st.success("Secret secured in the vault!"); st.rerun()
            
            if os.path.exists(VAULT_FILE):
                with open(VAULT_FILE, "r") as f:
                    for idx, line in enumerate(f):
                        parts = line.strip().split("|")
                        if len(parts) >= 3:
                            st.markdown(f'<div class="card"><b>{parts[0]}</b> - Saved on {parts[2]}</div>', unsafe_allow_html=True)
                            c_v, c_d = st.columns([6, 1])
                            if c_v.checkbox("Reveal Content", key=f"rev_{idx}"): st.code(decrypt(parts[1]))
                            if c_d.button("🗑️", key=f"del_v_{idx}"):
                                lines = open(VAULT_FILE).readlines()
                                with open(VAULT_FILE, "w") as fw:
                                    for i, l in enumerate(lines):
                                        if i != idx: fw.write(l)
                                st.rerun()

        # --- TAB 3: MEDIA ---
        with tabs[2]:
            st.subheader("📂 Media & Cloud Files")
            up = st.file_uploader("Upload sensitive documents")
            if up:
                with open(os.path.join(UPLOAD_DIR, up.name), "wb") as f: f.write(up.getbuffer())
                st.success("File uploaded successfully."); st.rerun()
            
            for fn in os.listdir(UPLOAD_DIR):
                col_f1, col_f2 = st.columns([5, 1])
                col_f1.write(f"📄 {fn}")
                if col_f2.button("🗑️", key=f"f_del_{fn}"):
                    os.remove(os.path.join(UPLOAD_DIR, fn)); st.rerun()

        # --- TAB 4: JOBS ---
        with tabs[3]:
            st.subheader("📅 Master Daily Log")
            with st.form("job_form", clear_on_submit=True):
                job_desc = st.text_input("What's on the schedule today?")
                if st.form_submit_button("Log Task"):
                    with open(JOB_FILE, "a") as f: f.write(f"{datetime.now().strftime('%Y-%m-%d')}|{job_desc}\n")
                    st.rerun()
            
            if os.path.exists(JOB_FILE):
                j_df = pd.read_csv(JOB_FILE, sep="|", names=["Date", "Task"])
                for i, r in j_df.iterrows():
                    st.markdown(f"✅ **{r['Date']}**: {r['Task']}")

    else:
        st.info("প্রফেসর, সিকিউরিটি চ্যালেঞ্জটি এখনো পূর্ণ হয়নি। সাইডবারে আপনার প্রিয় হিরোর নাম লিখুন।")