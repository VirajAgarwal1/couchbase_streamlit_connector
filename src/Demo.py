import streamlit as st
from couchbase_streamlit_connector.connector import CouchbaseConnector

# Streamlit UI
st.title("Couchbase CRUD App")

# User input for credentials
st.sidebar.header("Enter Couchbase Credentials")
conn_str = st.sidebar.text_input("Connection String", "couchbases://your-cluster-url")
username = st.sidebar.text_input("Username", "admin")
password = st.sidebar.text_input("Password", type="password")
bucket_name = st.sidebar.text_input("Bucket Name", "default")
scope_name = st.sidebar.text_input("Scope Name", "_default")
collection_name = st.sidebar.text_input("Collection Name", "_default")

if st.sidebar.button("Connect"):
    try:
        connection = st.connection(
            "couchbase", 
            type=CouchbaseConnector, 
            CONNSTR=conn_str, 
            USERNAME=username, 
            PASSWORD=password,
            BUCKET_NAME=bucket_name, 
            SCOPE_NAME=scope_name, 
            COLLECTION_NAME=collection_name
        )
        st.session_state["connection"] = connection
        st.sidebar.success("Connected successfully!")
    except Exception as e:
        st.sidebar.error(f"Connection failed: {e}")

if "connection" in st.session_state:
    connection = st.session_state["connection"]
    
    st.header("Perform CRUD Operations")
    
    # Insert Document
    st.subheader("Insert a Document")
    doc_id = st.text_input("Document ID")
    doc_data = st.text_area("Document Data (JSON format)")
    if st.button("Insert Document"):
        try:
            connection.insert_document(doc_id, eval(doc_data))
            st.success("Document inserted successfully!")
        except Exception as e:
            st.error(f"Error: {e}")
    
    # Fetch Document
    st.subheader("Fetch a Document")
    fetch_id = st.text_input("Enter Document ID to Fetch")
    if st.button("Fetch Document"):
        try:
            doc = connection.get_document(fetch_id)
            st.json(doc)
        except Exception as e:
            st.error(f"Error: {e}")
    
    # Replace Document
    st.subheader("Replace a Document")
    replace_id = st.text_input("Document ID to Replace")
    new_data = st.text_area("New Document Data (JSON format)")
    if st.button("Replace Document"):
        try:
            connection.replace_document(replace_id, eval(new_data))
            st.success("Document replaced successfully!")
        except Exception as e:
            st.error(f"Error: {e}")
    
    # Delete Document
    st.subheader("Delete a Document")
    delete_id = st.text_input("Document ID to Delete")
    if st.button("Delete Document"):
        try:
            connection.remove_document(delete_id)
            st.success("Document deleted successfully!")
        except Exception as e:
            st.error(f"Error: {e}")
    
    # Query
    st.subheader("Run a Query")
    query = st.text_area("Enter N1QL Query")
    if st.button("Execute Query"):
        try:
            result = connection.query(query)
            st.json(result)
        except Exception as e:
            st.error(f"Error: {e}")
