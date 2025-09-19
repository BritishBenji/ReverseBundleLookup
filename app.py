from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        bundle_id = request.form['bundle_id']
        api_url = f"http://itunes.apple.com/lookup?bundleId={bundle_id}"

        try:
            response = requests.get(api_url)
            # Raise an exception for bad status codes
            response.raise_for_status() 
            data = response.json()

            # Check for results
            if data['resultCount'] > 0:
                app_info = data['results'][0]
                # Extract and prep the data
                return render_template(
                    'index.html',
                    app_name=app_info.get('trackName', 'N/A'),
                    developer=app_info.get('artistName', 'N/A'),
                    artwork=app_info.get('artworkUrl512', 'https://placehold.co/512x512/dcdcdc/000000?text=No+Image'),
                    price=app_info.get('formattedPrice', 'N/A'),
                    description=app_info.get('description', 'No description available.'),
                    app_url=app_info.get('trackViewUrl', '#')
                )
            else:
                # No app found for the bundle ID
                return render_template('index.html', error=f"No app found for Bundle ID: {bundle_id}")

        except requests.exceptions.RequestException as e:
            # Request Errors
            return render_template('index.html', error=f"An error occurred while fetching data: {e}")
        except ValueError:
            # JSON Errors
            return render_template('index.html', error="Error parsing JSON response from API.")
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)