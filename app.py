from flask import Flask, jsonify
from flask_cors import CORS

import asyncio
from vix_index_futures import get_vix_and_vix_futures_prices
import nest_asyncio

nest_asyncio.apply()

app = Flask(__name__)
# THIS WAS ADDED TO ALLOW CORS FOR TEST PURPOSES!!! ON LOCALHOST!!! 
CORS(app, origins='http://localhost:3000')


@app.route('/vix-data')
def vix_data():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    vix_data_list = loop.run_until_complete(get_vix_and_vix_futures_prices())
    loop.close()
    return jsonify(vix_data_list)

if __name__ == '__main__':
    app.run(debug=True)
