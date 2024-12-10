import os
import streamlit as st
from search import SearchEngine

def main():
    # Set up the Streamlit page
    st.set_page_config(page_title="2049", page_icon="🔍", layout="centered", initial_sidebar_state="auto")

    # Add white background and theme styles
    st.markdown(
        """
        <style>
        body {
            background-color: white;
            color: black;
        }
        .main {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .query-input {
            width: 60%;
        }
        .examples {
            display: flex;
            flex-direction: row;
            justify-content: center;
            gap: 15px;
            margin-top: 5px; /* Moved up */
        }
        .example-button {
            background-color: transparent;
            border: 2px solid #1E90FF;
            border-radius: 10px;
            padding: 5px 15px;
            cursor: pointer;
            text-align: center;
            color: #1E90FF;
        }
        .example-button:hover {
            background-color: #ADD8E6;
        }
        .search-button {
            background-color: #1E90FF;
            color: white;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            border-radius: 10px;
        }
        .search-button:hover {
            background-color: #1560BD;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Title
    st.markdown(
        """<h1 style='text-align: center;'>Orbit.2049""",
        unsafe_allow_html=True,
    )

    # Create an instance of the Search class
    search_engine = SearchEngine()

    # Input for search query
    query = st.text_input("", placeholder="What would you like to know?", key="query", label_visibility="collapsed")

    # Centering the button
    col1, col2, col3 = st.columns([3, 1, 3])
    with col2:
        search_pressed = st.button("Search", key="search", use_container_width=True)

    # If search button is clicked or query is not empty
    if search_pressed or query:
        if query:
            # Show loading spinner
            with st.spinner("Searching and analyzing results..."):
                # Perform the search
                result = search_engine.perform_search(query)

            # Display the answer
            st.subheader("Answer")
            st.write(result["answer"])

            # Display sources
            if result["sources"]:
                st.subheader("Sources")
                for source in result["sources"]:
                    if source["url"]:
                        st.markdown(f"- [{source['title']}]({source['url']})")
                    else:
                        st.markdown(f"- {source['title']}")

    # Examples section
    st.markdown("<div style='text-align: center; margin-top: 20px;'><h3>Examples</h3></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class='examples' style='justify-content: center;'>
            <div class='example-button' onclick="document.getElementById('query').value='Best honeymoon locations?';">Best honeymoon locations?</div>
            <div class='example-button' onclick="document.getElementById('query').value='How does GPT work?';">How does GPT work?</div>
            <div class='example-button' onclick="document.getElementById('query').value='Who’s the director of Anora?';">Who’s the director of Anora?</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Required dependencies
if __name__ == "__main__":
    main()