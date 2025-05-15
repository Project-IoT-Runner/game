import adafruit_connection_manager
import wifi

import adafruit_requests

ID = 1

SSID = 'bauke-mbp'
PASSWORD = 'lekker-zwemmen'

URL = f'http://172.20.42.42:5173/api/device/{ID}/selected-sprite'

def get_sprite():
    # Initalize Wifi, Socket Pool, Request Session
    pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
    ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl_context)

    print(f"\nConnecting to {SSID}...")
    try:
        # Connect to the Wi-Fi network
        wifi.radio.connect(SSID, PASSWORD)
    except OSError as e:
        print(f"❌ OSError: {e}")
    print("✅ Wifi!")

    print(f" | GET Full Response Test: {URL}")
    with requests.get(URL) as response:
        print(f" | ✅ Unparsed Full JSON Response: {response.json()}")
        return response.json()
    print("-" * 80)

    print("Finished!")
    
def get_mock_sprite():
    return {'sprite': {'id': 2, 'name': 'Pikachu', 'pixels': [False, True, True, False, False, False, False, True, False, True, True, True, False, False, False, True, False, False, False, True, True, True, True, True, True, True, False, True, False, True, False, True, True, True, False, True, True, True, True, True, False, True, False, True, True, True, True, False, False, True, True, True, True, True, True, False, False, False, True, True, True, True, True, False]}}
