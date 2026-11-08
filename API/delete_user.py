from data import API
import requests

def delete_user(accessToken):
    requests.post(
                API.DELETE_USER,
                headers= {"Authorization": accessToken}
            )