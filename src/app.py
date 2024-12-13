import streamlit as st
from search import SearchEngine

def main():
    # Set up the Streamlit page
    st.set_page_config(page_title="2049", page_icon="🔍", layout="centered", initial_sidebar_state="auto")
    
    # Custom CSS to center content, add button hover effect, and style input
    st.markdown("""
    <style>
    .reportview-container .main .block-container {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    /* Style for the input */
    .stTextInput > div > div > input {
        text-align: left;
        border-color: #1E90FF;
    }
    .stTextInput > div > div > input::placeholder {
        text-align: left;
    }
    /* Style for the Search button */
    .stButton > button {
        display: block;
        margin: 0 auto;
    }
    /* Button hover effect */
    .stButton > button:hover {
        border-color: #1E90FF !important;
        color: #1E90FF !important;
    }
    /* Title alignment */
    h1 {
        text-align: left;
        width: 100%;
    }
    /* Added centered text above input with spacing */
    .centered-text {
        text-align: center;
        font-size: 1.3rem;
        margin-top: 2rem;  /* Add top margin */
    }
    </style>
    """, unsafe_allow_html=True)

    search_engine = SearchEngine()

    # Left-aligned title
    st.markdown(
        """<h1>Orbit.<span style='color: #1E90FF;'>2049</span></h1>""",
        unsafe_allow_html=True,
    )

    # Add centered text above input
    st.markdown(
        """<div class="centered-text">What would you like to know?</div>""",
        unsafe_allow_html=True,
    )

    # Input for search query with centered placeholder
    query = st.text_input("", placeholder="Ask Anything...", 
                           key="search_query")
                           
    # Search button
    if st.button("Search"): 
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
            else:
                print("No sources found..")

    st.session_state.search_performed = False
    # Examples section
    st.markdown("<br><br>", unsafe_allow_html=True)
    col4, col5, col6 = st.columns(3)
    with col4:
        if st.button("How did Alfred Hitchcock build suspense in his movies?"):
            query = 'How did Alfred Hitchcock build suspense in his movies?'
            st.session_state.search_performed = True
    with col5:
        if st.button("What are the main challenges in developing general AI?"):
            query = 'What are the main challenges in developing general AI?'
            st.session_state.search_performed = True
    with col6:
        if st.button("How do glaciers contribute to global sea levels?"):
            query = 'How do glaciers contribute to global sea levels?'
            st.session_state.search_performed = True

    if st.session_state.get('search_performed', True):
        if query:
            # Show loading spinner
            with st.spinner("Searching and analyzing results.."):
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
            else:
                print("No sources found.")


# Required dependencies
if __name__ == "__main__":
    main()