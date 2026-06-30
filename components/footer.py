from version import VERSION, VERSION_DATE
import streamlit as st

def render_footer():
    st.divider()
    st.caption(f"v{VERSION} · {VERSION_DATE}", text_alignment='center')
    st.caption(f"[GitHub](https://github.com/AAubin/stay-and-charge) - [AAubin](https://github.com/AAubin/)", text_alignment='center')
    