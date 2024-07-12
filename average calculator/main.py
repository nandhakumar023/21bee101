from config import app
from flask import request, jsonify
import requests

window_size = 10
window_prev = []
window_current = []

@app.route("/numbers/e", methods=["GET"])
def even():
    global window_size
    global window_prev
    global window_current 
    api_url = 'http://20.244.56.144/test/even'
    access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzIwNzY2NDczLCJpYXQiOjE3MjA3NjYxNzMsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6ImVkODcwODgzLThmOTMtNDg3YS1iNzZiLTBiNTA2OWJlN2E2ZiIsInN1YiI6Im5hbmRoYWt1bWFyMjMxMDIwMDNfYmVlMjVAbWVwY29lbmcuYWMuaW4ifSwiY29tcGFueU5hbWUiOiJNRVBDTyIsImNsaWVudElEIjoiZWQ4NzA4ODMtOGY5My00ODdhLWI3NmItMGI1MDY5YmU3YTZmIiwiY2xpZW50U2VjcmV0IjoidW9Pb1NOb3pEa2VIaHhGVyIsIm93bmVyTmFtZSI6Ik5hbmRoYSBLdW1hciBSIiwib3duZXJFbWFpbCI6Im5hbmRoYWt1bWFyMjMxMDIwMDNfYmVlMjVAbWVwY29lbmcuYWMuaW4iLCJyb2xsTm8iOiIyMWJlZTEwMSJ9.yutbOUN_Z6laj1yDOfgQUfTpLS18crIkyneVaTSVGOw"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    try:
        # response = requests.get(api_url, headers=headers)
        # print(f"Response content: {response.content}")
        try:
            # data = response.json()
            data  = {"numbers" : [6, 2, 8, 4, 34, 23, 78, 56, 24, 98, 34, 66]}
            given_numbers_tuple = tuple(data["numbers"])
            window_prev = window_current[:]
            if len(window_current) >= window_size:
                if len(given_numbers_tuple) > 10:
                    window_current = given_numbers_tuple[len(given_numbers_tuple) - 11:]
                else:
                    window_current = given_numbers_tuple[:]
            else:
                for i in range(len(given_numbers_tuple) - (window_size - len(window_current)), len(given_numbers_tuple)):
                    window_current.append(given_numbers_tuple[i])

            avg, sume = 0, 0
            for i in window_current:
                sume += i
            avg = sume / len(window_current)

            response_data = {
                "numbers" : data["numbers"],
                "windowPrevState" : window_prev,
                "windowCurrState" : window_current,
                "avg" : avg
            }

            return jsonify(response_data)
        except ValueError as e:
            return jsonify({'error': 'Invalid JSON response', 'message': str(e), 'response_content': response.text}), 500
    except requests.RequestException as e:
        return jsonify({'error': 'Request failed', 'message': str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True)