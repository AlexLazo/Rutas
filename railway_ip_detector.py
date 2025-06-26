#!/usr/bin/env python

"""
Railway IP Detector
-------------------
This script retrieves the IP address of your deployed Railway app
so you can access it directly by IP instead of domain name.

Usage:
1. Deploy this file to Railway
2. Access the /get_ip endpoint
3. Note the IP address displayed
4. Try accessing your app via http://[IP_ADDRESS]:PORT
"""

import socket
import requests
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/get_ip')
def get_ip():
    # Method 1: Socket
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
    except:
        ip_address = "Unable to get hostname IP"
    
    # Method 2: External service
    try:
        external_ip = requests.get('https://api.ipify.org').text
    except:
        external_ip = "Unable to get external IP"
    
    # Method 3: Request headers
    from flask import request
    headers = dict(request.headers)
    
    return jsonify({
        'hostname': hostname,
        'hostname_ip': ip_address,
        'external_ip': external_ip,
        'headers': headers,
        'note': "Try accessing your app directly via these IPs instead of domain"
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
