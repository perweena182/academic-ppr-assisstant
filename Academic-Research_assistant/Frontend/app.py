import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("Academic Research Paper Assistant")

menu = ["Search Papers", "Chat"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Search Papers":
    st.header("Search for Research Papers")
    topic = st.text_input("Enter Research Topic")
    if st.button("Search"):
        if topic.strip() == "":
            st.error("Please enter a valid topic.")
        else:
            with st.spinner("Searching for papers..."):
                response = requests.post(f"{API_URL}/search", json={"topic": topic})
                if response.status_code == 200:
                    papers = response.json().get("papers", [])
                    st.success(f"Found {len(papers)} papers.")
                    for paper in papers:
                        st.markdown(f"**{paper['title']}** ([Link]({paper['url']})) - Published on {paper['published']}")
                else:
                    st.error(f"Error fetching papers: {response.text}")

elif choice == "Chat":
    st.header("Chat with the Assistant")
    topic = st.text_input("Enter Research Topic for Chat")
    if topic:
        user_input = st.text_area("Enter your question or command:")
        if st.button("Send"):
            if user_input.strip() == "":
                st.error("Please enter a valid question or command.")
            else:
                with st.spinner("Processing..."):
                    # Determine the type of task based on user input
                    lower_input = user_input.lower()
                    if "summarize" in lower_input:
                       
                        task = "summarization"
                        payload = {"topic": topic}
                        endpoint = "/summarize"
                    elif "review" in lower_input or "future work" in lower_input:
                       

                        task = "review"
                        payload = {"topic": topic}
                        endpoint = "/generate_review"
                    else:
                        task = "qa"
                        payload = {"topic": topic, "query": user_input}

                    response = requests.post(f"{API_URL}{endpoint}", json=payload)
                    if response.status_code == 200:
                        if task == "summarization":
                            summary = response.json().get("summary", "No summary available.")
                            st.write("**Summary:**")
                            st.write(summary)
                        elif task == "review":
                            review = response.json().get("review", "No review available.")
                            st.write("**Review :**")
                            
                            st.write(review)
                        else:
                            answer = response.json().get("answer", "No answer available.")
                            st.write("**Answer:**")
                            st.write(answer)
                    else:
                        st.error(f"Error processing request: {response.text}")
