"""
Day 20 - Job Alert Scraper (Streamlit Web UI)
Wraps job_scraper.py's fetch functions in a simple web interface.
Same logic as the CLI version (Day 19) - just a browser UI on top.

Usage:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd

from job_scraper import fetch_remoteok, fetch_remotive


# ---------- Page setup ----------
st.set_page_config(page_title="Job Alert Scraper", page_icon="🔎")

st.title("🔎 Job Alert Scraper")
st.write("Search RemoteOK + Remotive for remote jobs matching a keyword.")


# ---------- Input ----------
keyword = st.text_input("Enter a job keyword", placeholder="e.g. python, react, data analyst")

col1, col2 = st.columns(2)
with col1:
    limit = st.number_input("Max results (0 = no limit)", min_value=0, value=0, step=5)
with col2:
    search_clicked = st.button("Search", type="primary")


# ---------- Search logic ----------
if search_clicked:
    if not keyword.strip():
        st.warning("Please enter a keyword first.")
    else:
        with st.spinner(f"Searching for '{keyword}' jobs..."):
            try:
                remoteok_jobs = fetch_remoteok(keyword)
            except Exception as e:
                st.error(f"RemoteOK fetch failed: {e}")
                remoteok_jobs = []

            try:
                remotive_jobs = fetch_remotive(keyword)
            except Exception as e:
                st.error(f"Remotive fetch failed: {e}")
                remotive_jobs = []

        all_jobs = remoteok_jobs + remotive_jobs

        if limit > 0:
            all_jobs = all_jobs[:limit]

        # ---------- Results ----------
        if not all_jobs:
            st.info("No matching jobs found. Try a different keyword.")
        else:
            st.success(f"Found {len(all_jobs)} matching job(s)")

            df = pd.DataFrame(all_jobs)

            # Make the URL clickable inside the table
            st.dataframe(
                df,
                column_config={
                    "url": st.column_config.LinkColumn("Apply Link")
                },
                use_container_width=True,
                hide_index=True,
            )

            # Download button - lets a client/user export results themselves
            csv_data = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download results as CSV",
                data=csv_data,
                file_name=f"jobs_{keyword.replace(' ', '_')}.csv",
                mime="text/csv",
            )
else:
    st.caption("Enter a keyword above and hit Search to get started.")