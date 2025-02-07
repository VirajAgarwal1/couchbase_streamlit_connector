from cb_streamlit_connector.connector import CouchbaseConnector
import streamlit as st

import os

from couchbase.exceptions import DocumentNotFoundException
from couchbase.logic.n1ql import QueryStatus

import pytest
import unittest
from unittest.mock import MagicMock, patch

# TODO: Add the test_query_consistency        

@pytest.fixture
@patch('couchbase.cluster.Cluster')
def connection(mock_Cluster):
    
    mock_cluster_object = MagicMock()
    mock_cluster_object.wait_until_ready = MagicMock(return_value=True)
    mock_cluster_object.bucket = MagicMock(return_value=MagicMock())
    mock_cluster_object.scope = MagicMock(return_value=MagicMock())
    mock_cluster_object.collection = MagicMock(return_value=MagicMock())
    mock_Cluster.return_value = mock_cluster_object
    
    connection = st.connection(
        "couchbase", 
        type=CouchbaseConnector, 
        CONNSTR= "CONNSTR",
        USERNAME= "USERNAME",
        PASSWORD= "PASSWORD",
        BUCKET_NAME= "BUCKET_NAME",
        SCOPE_NAME= "SCOPE_NAME",
        COLLECTION_NAME= "COLLECTION_NAME"
    )
    
    # for test_create
    mock_cluster_object.collection.insert = MagicMock(return_value="mock_insert_result")
    
    # for test_read
    mock_get_result = MagicMock()
    mock_get_result.content_as = {dict: "mock_get_result"}
    mock_cluster_object.collection.get = MagicMock(return_value=mock_get_result)
    
    # for test_update
    mock_cluster_object.collection.replace = MagicMock(return_value="mock_replace_result")
    
    # for test_delete
    mock_cluster_object.collection.remove = MagicMock(return_value="mock_remove_result")
    
    # for test_query
    mock_cluster_object.query = MagicMock(return_value="mock_query_result")
    
    return connection
    
def test_create(connection):
    """Test the successful creation of an airline"""
    # airline_data = {
    #     "name": "Sample Airline",
    #     "iata": "SAL",
    #     "icao": "SALL",
    #     "callsign": "SAM",
    #     "country": "Sample Country",
    # }
    # document_id = "airline_test_insert"
    # try:
    #     connection.collection.remove(document_id)
    # except DocumentNotFoundException:
    #     pass
    # response = connection.insert_document(document_id, airline_data)
    # assert response.key == document_id

    # # Check document stored in DB is same as sent & clean up
    # doc_in_db = connection.get_document(document_id)
    # assert doc_in_db == airline_data
    # connection.remove_document(document_id)
    
    assert connection.insert_document("doc1", {"name": "Alice"}) == "mock_insert_result"
    # connection.collection.insert.assert_called_once()
            
def test_read(connection):
    """Test the reading of an airline"""
    # airline_data = {
    #     "name": "Sample Airline",
    #     "iata": "SAL",
    #     "icao": "SALL",
    #     "callsign": "SAM",
    #     "country": "Sample Country",
    # }
    # document_id = "airline_test_read"
    # try:
    #     connection.collection.remove(document_id)
    # except DocumentNotFoundException:
    #     pass
    # response = connection.insert_document(document_id, airline_data)

    # response = connection.get_document(document_id)
    # assert response == airline_data

    # connection.remove_document(document_id)
    assert connection.get_document("doc1") == "mock_get_result"
    # connection.collection.get.assert_called_once()
    
def test_update(connection):
    """Test updating an existing airline"""
    # airline_data = {
    #     "name": "Sample Airline",
    #     "iata": "SAL",
    #     "icao": "SALL",
    #     "callsign": "SAM",
    #     "country": "Sample Country",
    # }
    # document_id = "airline_test_update"
    # try:
    #     connection.collection.remove(document_id)
    # except DocumentNotFoundException:
    #     pass
    # response = connection.insert_document(document_id, airline_data)

    # updated_airline_data = {
    #     "name": "Updated Airline",
    #     "iata": "SAL",
    #     "icao": "SALL",
    #     "callsign": "SAM",
    #     "country": "Updated Country",
    # }

    # response = connection.replace_document(document_id, updated_airline_data)
    # assert response.key == document_id
    # response = connection.get_document(document_id)
    # assert response == updated_airline_data

    # connection.remove_document(document_id)
    assert connection.replace_document("doc1", {"name": "Alice", "age": 25}) == "mock_replace_result"
    # connection.collection.replace.assert_called_once()
    
def test_delete(connection):
    """Test deleting an existing airline"""
    # airline_data = {
    #     "name": "Sample Airline",
    #     "iata": "SAL",
    #     "icao": "SALL",
    #     "callsign": "SAM",
    #     "country": "Sample Country",
    # }
    # document_id = "airline_test_delete"
    # try:
    #     connection.collection.remove(document_id)
    # except DocumentNotFoundException:
    #     pass
    # response = connection.insert_document(document_id, airline_data)

    # response = connection.remove_document(document_id)
    # assert response.key == document_id
    assert connection.remove_document("doc1") == "mock_remove_result"
    # connection.collection.remove.assert_called_once()
    
def test_query(connection):
    """Test the destination airports from an airline"""
    # query = """
    #     SELECT * FROM `travel-sample`.`inventory`.`airline`
    #     WHERE type = "airline"
    #     AND country = "United States"
    #     LIMIT 5;
    # """
    # result = connection.query(query)
    # data = []
    # for row in result.rows():
    #     data.append(row)
    # assert result.metadata().status() == QueryStatus.SUCCESS
    assert connection.query("SELECT * FROM `test`") == "mock_query_result"
    # connection.cluster.query.assert_called_once()
