import pytest
from base64 import b64encode
from flask import current_app, json, url_for
from http_status import HttpStatus
from models import db, PhotoCategory, Photo, User


TEST_USER_NAME = 'testuser'
TEST_USER_PASSWORD = 'T3s!p4s5w0RDd12#'
TEST_USER_EMAIL = "testemail@test.com"


def get_accept_content_type_headers():
    return {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }


def get_authentication_headers(username, password):
    authentication_headers = get_accept_content_type_headers()
    authentication_headers['Authorization'] = \
        'Basic ' + b64encode((username + ':' + password).encode('utf-8')).decode('utf-8')
    return authentication_headers


def test_request_without_authentication(client):
    """
    Ensure we cannot access a resource that requirest authentication without an appropriate authentication header
    """
    response = client.get(
        url_for('photo.photolistresource', _external=True),
        headers=get_accept_content_type_headers())
    assert response.status_code == HttpStatus.unauthorized_401.value
    


def create_user(client, name, email, password):
    url = url_for('photo.userlistresource', 
        _external=True)
    data = {'name': name, 'email':email, 'password': password}
    response = client.post(
        url, 
        headers=get_accept_content_type_headers(),
        data=json.dumps(data))
    return response



def create_photo_category(client, name):
    url = url_for('photo.photocategorylistresource', 
        _external=True)
    data = {'name': name}
    response = client.post(
        url, 
        headers=get_authentication_headers(TEST_USER_NAME, TEST_USER_PASSWORD),
        data=json.dumps(data))
    return response

def test_create_and_retrieve_photo_category(client):
    """Testing creation and retreival of a photo category"""
    #Create new user for test
    create_user_response = create_user(client, TEST_USER_NAME, TEST_USER_EMAIL, TEST_USER_PASSWORD,)
    assert create_user_response.status_code == HttpStatus.created_201.value
    photo_category_name = 'Management'
    post_response = create_photo_category(client, photo_category_name)
    assert post_response.status_code == HttpStatus.created_201.value
    assert PhotoCategory.query.count() == 1
    #Retreive and compare posted category name
    post_response_data = json.loads(post_response.get_data(as_text=True))
    assert post_response_data['name'] == photo_category_name
    photo_category_url = post_response_data['url']
    get_response = client.get(
        photo_category_url,
        headers=get_authentication_headers(TEST_USER_NAME, TEST_USER_PASSWORD))
    assert get_response.status_code == HttpStatus.ok_200.value
    get_response_data = json.loads(get_response.get_data(as_text=True))
    assert get_response_data['name'] == photo_category_name 


def test_create_duplicate_photo_category(client):
    create_user_response = create_user(client,TEST_USER_NAME,TEST_USER_EMAIL,TEST_USER_PASSWORD)
    assert create_user_response.status_code == HttpStatus.created_201.value
    photo_category_name = 'Management'
    post_response = create_photo_category(client,photo_category_name)
    assert post_response.status_code == HttpStatus.created_201.value
    assert PhotoCategory.query.count() == 1
    post_response_data = json.loads(post_response.get_data(as_text=True))
    assert post_response_data['name'] == photo_category_name
    second_post_response = create_photo_category(client,photo_category_name)
    assert second_post_response.status_code == HttpStatus.bad_request_400.value
    assert PhotoCategory.query.count() == 1


def test_retreive_photo_categories_list(client):
    """
    Ensure we can retrieve the notification categories list    """
    create_user_response = create_user(client,TEST_USER_NAME,TEST_USER_EMAIL,TEST_USER_PASSWORD)
    assert create_user_response.status_code == HttpStatus.created_201.value
    photo_category_name_1 = 'Error'
    post_response_1 = create_photo_category(client, photo_category_name_1)
    assert post_response_1.status_code, HttpStatus.created_201.value
    photo_category_name_2 = 'Warning'
    post_response_2 = create_photo_category(client, photo_category_name_2)
    assert post_response_2.status_code, HttpStatus.created_201.value
    url = url_for('photo.photocategorylistresource', _external=True)
    get_response = client.get(
        url,
        headers=get_authentication_headers(TEST_USER_NAME, TEST_USER_PASSWORD))
    assert get_response.status_code == HttpStatus.ok_200.value
    get_response_data = json.loads(get_response.get_data(as_text=True))
    assert len(get_response_data) == 2
    assert get_response_data[0]['name'] == photo_category_name_1
    assert get_response_data[1]['name'] == photo_category_name_2

    
def test_update_photo_category(client):   
    """
    Ensure we can update the name for an existing notification category
    """
    create_user_response = create_user(client, TEST_USER_NAME,TEST_USER_EMAIL,TEST_USER_PASSWORD)
    assert create_user_response.status_code == HttpStatus.created_201.value
    photo_category_name_1 = 'Food'
    post_response_1 = create_photo_category(client, photo_category_name_1)
    assert post_response_1.status_code == HttpStatus.created_201.value
    post_response_data_1 = json.loads(post_response_1.get_data(as_text=True))
    photo_category_url = post_response_data_1['url']
    photo_category_name_2 = 'Lockdown'
    data = {'name': photo_category_name_2}
    patch_response = client.patch(
        photo_category_url, 
        headers=get_authentication_headers(TEST_USER_NAME, TEST_USER_PASSWORD),
        data=json.dumps(data))
    assert patch_response.status_code == HttpStatus.ok_200.value
    get_response = client.get(
        photo_category_url,
        headers=get_authentication_headers(TEST_USER_NAME, TEST_USER_PASSWORD))
    assert get_response.status_code == HttpStatus.ok_200.value
    get_response_data = json.loads(get_response.get_data(as_text=True))
    assert get_response_data['name'] == photo_category_name_2 



def create_photo(client, link, description, photo_category):
    url = url_for('photo.photolistresource',
        _external=True)
    data = {'link':link, 'description':description, 'photo_category':photo_category}
    response = client.post(
        url,
        headers = get_authentication_headers(TEST_USER_NAME, TEST_USER_PASSWORD),
        data = json.dumps(data))
    return response



def test_create_and_retrieve_photo(client):
    """
    Ensure we can create a new notification and then retrieve it
    """
    create_user_response = create_user(client, TEST_USER_NAME,TEST_USER_EMAIL, TEST_USER_PASSWORD)
    assert create_user_response.status_code == HttpStatus.created_201.value
    photo_link ='pixabayphotos'
    photo_description = 'Laptop and computers'
    photo_category = 'Technology'
    post_response = create_photo(client, photo_link, photo_description, photo_category)
    assert post_response.status_code == HttpStatus.created_201.value
    assert Photo.query.count() == 1
    assert PhotoCategory.query.count() == 1
    post_response_data = json.loads(post_response.get_data(as_text=True))
    assert post_response_data['link'] == photo_link 
    new_photo_url = post_response_data['url']
    get_response = client.get(
        new_photo_url,
        headers=get_authentication_headers(TEST_USER_NAME, TEST_USER_PASSWORD))
    assert get_response.status_code == HttpStatus.ok_200.value
    get_response_data = json.loads(get_response.get_data(as_text=True))
    assert get_response_data['link'] == photo_link
    
    

def test_create_duplicated_photo(client):
    create_user_response = create_user(client, TEST_USER_NAME,TEST_USER_EMAIL,TEST_USER_PASSWORD)
    assert create_user_response.status_code == HttpStatus.created_201.value
    photo_link ='pixabayphotos'
    photo_description = 'Laptop and computers'
    photo_category = 'Technology'
    post_response = create_photo(client, photo_link, photo_description, photo_category)
    assert post_response.status_code == HttpStatus.created_201.value
    assert Photo.query.count() == 1
    post_response_data = json.loads(post_response.get_data(as_text=True))
    assert post_response_data['link'] == photo_link
    new_photo_url = post_response_data['url']
    get_response = client.get(
        new_photo_url,
        headers=get_authentication_headers(TEST_USER_NAME,TEST_USER_PASSWORD))
    assert get_response.status_code == HttpStatus.ok_200.value
    get_response_data = json.loads(get_response.get_data(as_text=True))
    assert get_response_data['link'] == photo_link 
    assert get_response_data['photo_category']['name'] == photo_category
    second_post_response = create_photo(client, photo_link, photo_description, photo_category)
    assert second_post_response.status_code == HttpStatus.bad_request_400.value
    assert Photo.query.count() == 1


def test_update_photo(client):
    create_user_response = create_user(client, TEST_USER_NAME,TEST_USER_EMAIL, TEST_USER_PASSWORD)
    assert create_user_response.status_code == HttpStatus.created_201.value
    photo_link ='pixabayphotos'
    photo_description = 'Laptop and computers'
    photo_category = 'Technology'
    post_response = create_photo(client, photo_link, photo_description, photo_category)
    assert post_response.status_code == HttpStatus.created_201.value
    post_response_data = json.loads(post_response.get_data(as_text=True))
    photo_url = post_response_data['url']
    photo_description = 'Laptop and computers'
    photo_category = 'Technology'
    data = {'description':photo_description, 'photo_category':photo_category}
    patch_response = client.patch(
        photo_url, 
        headers=get_authentication_headers(TEST_USER_NAME, TEST_USER_PASSWORD),
        data=json.dumps(data))
    assert patch_response.status_code == HttpStatus.ok_200.value
    get_response = client.get(
        photo_url,
        headers=get_authentication_headers(TEST_USER_NAME, TEST_USER_PASSWORD))
    assert get_response.status_code == HttpStatus.ok_200.value
    get_response_data = json.loads(get_response.get_data(as_text=True))
    assert get_response_data['description'] == photo_description 




def test_retrieve_photo_list(client):
    create_user_response = create_user(client, TEST_USER_NAME,TEST_USER_EMAIL, TEST_USER_PASSWORD)
    assert create_user_response.status_code == HttpStatus.created_201.value
    photo_link ='pixabayphotos'
    photo_description = 'Laptop and computers'
    photo_category = 'Technology'
    post_response = create_photo(client, photo_link, photo_description, photo_category)
    assert post_response.status_code == HttpStatus.created_201.value
    post_response_data = json.loads(post_response.get_data(as_text=True))
    assert Photo.query.count() == 1
    photo_link_2 ='canadiantravel'
    photo_description_2 = 'Living in Canada'
    photo_category_2 = 'Travel'
    post_response = create_photo(client, photo_link_2, photo_description_2, photo_category_2)
    assert post_response.status_code == HttpStatus.created_201.value
    assert Photo.query.count() == 2
    get_first_page_url = url_for('photo.photolistresource', _external=True)
    get_first_page_response = client.get(
        get_first_page_url,
        headers=get_authentication_headers(TEST_USER_NAME, TEST_USER_PASSWORD))
    assert get_first_page_response.status_code == HttpStatus.ok_200.value
    get_first_page_response_data = json.loads(get_first_page_response.get_data(as_text=True))
    assert get_first_page_response_data['count'] == 2
    assert get_first_page_response_data['previous'] is None
    assert get_first_page_response_data['next'] is None
    assert get_first_page_response_data['results'] is not None
    assert len(get_first_page_response_data['results']) == 2
    assert get_first_page_response_data['results'][0]['link'] == photo_link
    assert get_first_page_response_data['results'][1]['link'] == photo_link_2
    get_second_page_url = url_for('photo.photolistresource', page=2)
    get_second_page_response = client.get(
        get_second_page_url,
        headers=get_authentication_headers(TEST_USER_NAME, TEST_USER_PASSWORD))
    assert get_second_page_response.status_code == HttpStatus.ok_200.value
    get_second_page_response_data = json.loads(get_second_page_response.get_data(as_text=True))
    assert get_second_page_response_data['previous'] is not None
    assert get_second_page_response_data['previous'] == url_for('photo.photolistresource', page=1)
    assert get_second_page_response_data['next'] is None
    assert get_second_page_response_data['results'] is not None
    assert len(get_second_page_response_data['results']) == 0



def test_create_and_retrieve_user(client):
    new_user_name = TEST_USER_NAME
    new_user_email = TEST_USER_EMAIL
    new_user_password = TEST_USER_PASSWORD
    post_response = create_user(client, new_user_name, new_user_email, new_user_password)
    assert post_response.status_code == HttpStatus.created_201.value
    assert User.query.count() == 1
    post_response_data = json.loads(post_response.get_data(as_text=True))
    assert post_response_data['name'] == new_user_name
    new_user_url = post_response_data['url']
    get_response = client.get(
        new_user_url,
        headers=get_authentication_headers(new_user_name, new_user_password))
    assert get_response.status_code == HttpStatus.ok_200.value
    get_response_data = json.loads(get_response.get_data(as_text=True))
    assert get_response_data['name'] == new_user_name
