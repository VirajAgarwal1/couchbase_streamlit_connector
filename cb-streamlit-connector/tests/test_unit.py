from cb_streamlit_connector.connector import *
import pytest
import os
from unittest.mock import MagicMock, patch

@pytest.fixture
def mock_connection():
    conn = CouchbaseConnector(
        "couchbase",
        CONNSTR= os.environ["CONNSTR"],
        USERNAME= os.environ["USERNAME"],
        PASSWORD= os.environ["PASSWORD"],
        BUCKET_NAME= os.environ["BUCKET_NAME"],
        SCOPE_NAME= os.environ["SCOPE_NAME"],
        COLLECTION_NAME= os.environ["COLLECTION_NAME"]
    )
    conn.cluster = MagicMock()
    conn.bucket = MagicMock()
    conn.scope = MagicMock()
    conn.collection = MagicMock()
    return conn

def test_set_bucket_scope_coll(mock_connection):
    """Test setting bucket, scope, and collection"""
    mock_connection.set_bucket_scope_coll("test_bucket", "test_scope", "test_collection")

    assert mock_connection.bucket_name == "test_bucket"
    assert mock_connection.scope_name == "test_scope"
    assert mock_connection.collection_name == "test_collection"
    assert mock_connection.bucket is not None
    assert mock_connection.scope is not None
    assert mock_connection.collection is not None

def test_insert_document(mock_connection):
    """Test inserting a document"""
    mock_connection.collection.insert = MagicMock(return_value="mock_insert_result")
    
    result = mock_connection.insert_document("doc1", {"name": "Alice"})
    assert result == "mock_insert_result"
    mock_connection.collection.insert.assert_called_once()

def test_get_document(mock_connection):
    """Test retrieving a document"""
    mock_result = MagicMock()
    mock_result.content_as = {dict:{"name": "Alice"}}
    
    mock_connection.collection.get = MagicMock(return_value=mock_result)
    result = mock_connection.get_document("doc1")

    assert result == {"name": "Alice"}
    mock_connection.collection.get.assert_called_once()

def test_replace_document(mock_connection):
    """Test replacing a document"""
    mock_connection.collection.replace = MagicMock(return_value="mock_replace_result")
    
    result = mock_connection.replace_document("doc1", {"name": "Alice", "age": 25})
    assert result == "mock_replace_result"
    mock_connection.collection.replace.assert_called_once()

def test_remove_document(mock_connection):
    """Test removing a document"""
    mock_connection.collection.remove = MagicMock(return_value="mock_remove_result")
    
    result = mock_connection.remove_document("doc1")
    assert result == "mock_remove_result"
    mock_connection.collection.remove.assert_called_once()

def test_query(mock_connection):
    """Test querying data"""
    mock_connection.cluster.query = MagicMock(return_value=["row1", "row2"])
    
    result = mock_connection.query("SELECT * FROM `test`")
    assert result == ["row1", "row2"]
    mock_connection.cluster.query.assert_called_once()
