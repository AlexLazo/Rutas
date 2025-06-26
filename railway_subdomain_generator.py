#!/usr/bin/env python

"""
Railway Subdomain Generator
--------------------------
This script will set up your app to work with multiple potential subdomains
to increase the chance of bypassing corporate firewalls.

Usage:
1. Deploy this file alongside your main app
2. Add it to your Procfile or railway.json to run it
3. It will create multiple subdomains pointing to your app
"""

import os
import requests
import time
import json

def get_railway_token():
    """Get Railway token from environment"""
    return os.environ.get('RAILWAY_TOKEN')

def create_custom_subdomain(token, project_id, subdomain):
    """Create a custom subdomain for a Railway project"""
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'projectId': project_id,
        'subdomain': subdomain
    }
    
    response = requests.post(
        'https://backboard.railway.app/api/projects/domains',
        headers=headers,
        json=data
    )
    
    return response.json()

def generate_subdomains(base_name):
    """Generate variations of subdomains that might bypass filters"""
    variations = [
        f"{base_name}",
        f"{base_name}-app",
        f"{base_name}-internal",
        f"{base_name}-system",
        f"{base_name}-corp",
        f"{base_name}-secure",
        f"internal-{base_name}",
        f"secure-{base_name}",
        f"app-{base_name}",
        f"sys-{base_name}",
        f"{base_name}-portal"
    ]
    
    return variations

def main():
    print("🔄 Configuring alternative subdomains for access...")
    
    token = get_railway_token()
    if not token:
        print("❌ No RAILWAY_TOKEN found in environment variables")
        return
    
    # Get project ID from environment
    project_id = os.environ.get('RAILWAY_PROJECT_ID')
    if not project_id:
        print("❌ No RAILWAY_PROJECT_ID found in environment variables")
        return
    
    # Base name for your app
    base_name = "rutas"  # Change this to your preferred base name
    
    # Generate subdomain variations
    subdomains = generate_subdomains(base_name)
    
    successful = []
    failed = []
    
    # Try to create each subdomain
    for subdomain in subdomains:
        try:
            result = create_custom_subdomain(token, project_id, subdomain)
            if 'error' in result:
                print(f"⚠️ Failed to create subdomain {subdomain}: {result['error']}")
                failed.append(subdomain)
            else:
                print(f"✅ Created subdomain: {subdomain}")
                successful.append(subdomain)
                # Don't flood the API
                time.sleep(1)
        except Exception as e:
            print(f"❌ Error creating subdomain {subdomain}: {str(e)}")
            failed.append(subdomain)
    
    # Write results to a file
    with open('subdomain_results.json', 'w') as f:
        json.dump({
            'successful': successful,
            'failed': failed,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }, f, indent=2)
    
    print(f"✅ Created {len(successful)} subdomains successfully")
    print(f"⚠️ Failed to create {len(failed)} subdomains")
    print("📄 Results saved to subdomain_results.json")

if __name__ == "__main__":
    main()
