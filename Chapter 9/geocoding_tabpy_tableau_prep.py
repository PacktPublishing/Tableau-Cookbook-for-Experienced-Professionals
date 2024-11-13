import requests
import pandas as pd
import time

def geocode_address(df):
    lat = []
    lon = []
    confidence = []

    # OpenRouteService API key
    mykey = 'open-route-service-key'
    headers = {'Accept': 'application/json'}

    for i in df.index:
        try:
            # Build URL with structured parameters
            base_url = 'https://api.openrouteservice.org/geocode/search/structured'
            params = {
                'api_key': mykey,
                'address': df['address'][i].strip(),
                'country': df['country'][i].strip(),
                'postalcode': df['postcode'][i].strip(),
                'region': df['region'][i].strip(),
                'locality': df['locality'][i].strip(),
                'size': 1
            }

            # Make the API request
            geocode_result = requests.get(base_url, params=params, headers=headers)
            data = geocode_result.json()

            # Extract coordinates
            if 'features' in data and data['features']:
                coordinates = data['features'][0]['geometry']['coordinates']
                lt = coordinates[1]  # Latitude
                lg = coordinates[0]  # Longitude
                conf = data['features'][0]['properties'].get('confidence', 0)
            else:
                lt = 0
                lg = 0
                conf = 0

            confidence.append(conf)
            lat.append(lt)
            lon.append(lg)

            # Rate limiting - be nice to the API
            time.sleep(1)

        except Exception as e:
            print(f"Error processing address {df['address'][i]}: {str(e)}")
            confidence.append(0)
            lat.append(0)
            lon.append(0)

    # Create result dataframe
    result_df = pd.DataFrame({
        'address': df['address'],
        'confidence': confidence,
        'latitude': lat,
        'longitude': lon
    })

    return result_df

def get_output_schema():
    return pd.DataFrame({
        'address': prep_string(),
        'confidence': prep_decimal(),
        'latitude': prep_decimal(),
        'longitude': prep_decimal()
    })
