import requests



class ApiHandler:
    def __init__(self):
        # Update this to your Laravel API endpoint
        self.api_endpoint = "http://127.0.0.1:8000/api"

    def send_shares(self, shares):
        # Send shares to Laravel API
        data_to_send = {"shares": shares}
        url = self.api_endpoint + "/save_shares"

        # Debugging: Print request details
        print(f"Sending POST request to: {url}")
        print(f"Request data: {data_to_send}")

        response = requests.post(url, json=data_to_send)

        # Debugging: Print response details
        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.text}")

        return response

    def get_shares(self):
        # Retrieve shares from Laravel API
        url = self.api_endpoint + "/getShares"

        # Debugging: Print request details
        print(f"Sending GET request to: {url}")

        response = requests.get(url)

        # Debugging: Print response details
        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.text}")

        return response

    def delete_shares(self):
        # Send request to delete shares from Laravel API
        url = self.api_endpoint + "/delete_shares"

        # Debugging: Print request details
        print(f"Sending DELETE request to: {url}")

        response = requests.delete(url)

        # Debugging: Print response details
        print(f"Response status code: {response.status_code}")

        return response

