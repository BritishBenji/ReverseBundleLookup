from flask import Flask, request, render_template
import requests
from google_play_scraper import app as google_app_scraper, exceptions as google_exceptions

app = Flask(__name__)
# Landing Page
@app.route('/', methods=['GET'])
def landing():
    return render_template('landing.html')

# Apple Part
@app.route('/apple', methods=['GET', 'POST'])
def apple_lookup():
    if request.method == 'POST':
        bundle_id = request.form['bundle_id']
        api_url = f"http://itunes.apple.com/lookup?bundleId={bundle_id}"
        
        try:
            response = requests.get(api_url)
            response.raise_for_status() 
            data = response.json()

            # Check if any results were returned
            if data['resultCount'] > 0:
                app_info = data['results'][0]
                # Extract and prepare the data to be displayed
                return render_template(
                    'apple_lookup.html',
                    app_name=app_info.get('trackName', 'N/A'),
                    developer=app_info.get('artistName', 'N/A'),
                    artwork=app_info.get('artworkUrl512', 'https://placehold.co/512x512/dcdcdc/000000?text=No+Image'),
                    price=app_info.get('formattedPrice', 'N/A'),
                    description=app_info.get('description', 'No description available.'),
                    app_url=app_info.get('trackViewUrl', '#')
                )
            else:
                # No app found for the given bundle ID
                return render_template('apple_lookup.html', error=f"No app found for Bundle ID: {bundle_id}")

        except requests.exceptions.RequestException as e:
            # Handle API request errors
            return render_template('apple_lookup.html', error=f"An error occurred while fetching data from Apple: {e}")
        except ValueError:
            # Handle JSON decoding errors
            return render_template('apple_lookup.html', error="Error parsing JSON response from Apple API.")

    # If the request is a GET, just show the empty form
    return render_template('apple_lookup.html')


# Google Part
@app.route('/google', methods=['GET', 'POST'])
def google_lookup():
    if request.method == 'POST':
        bundle_id = request.form['bundle_id']
        try:
            # Use the google-play-scraper library to get app info
            app_info = google_app_scraper(bundle_id, lang='en', country='us')
            
            # Extract and prepare the data from the scraper result
            return render_template(
                'google_lookup.html',
                app_name=app_info.get('title', 'N/A'),
                developer=app_info.get('developer', 'N/A'),
                artwork=app_info.get('icon', 'https://placehold.co/512x512/dcdcdc/000000?text=No+Image'),
                price=app_info.get('price', 'N/A'),
                description=app_info.get('description', 'No description available.'),
                app_url=app_info.get('url', '#')
            )
        except google_exceptions.NotFoundError:
            # Handle cases where the app is not found on the Play Store
            return render_template('google_lookup.html', error=f"No app found for Package Name: {bundle_id}")
        except Exception as e:
            # Catch any other general errors from the scraper
            return render_template('google_lookup.html', error=f"An error occurred while fetching data from Google Play: {e}")

    # If the request is a GET, just show the empty form
    return render_template('google_lookup.html')

if __name__ == '__main__':
    app.run(debug=True)
