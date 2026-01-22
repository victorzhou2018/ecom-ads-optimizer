#!/usr/bin/env python3
"""
EcomAds Optimizer – Main Entry Point (CLI Prototype)
Author: [Victor]
"""

import os
import yaml
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.oauth2 import GoogleAdsOAuthFlow
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

# Configuration
CONFIG_FILE = "config.yaml"
CREDENTIALS_FILE = "token.pickle"
SCOPES = ["https://www.googleapis.com/auth/adwords"]

def load_config():
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(
            f"Config file '{CONFIG_FILE}' not found. "
            f"Please copy 'config.example.yaml' to '{CONFIG_FILE}' and fill in your details."
        )
    with open(CONFIG_FILE, "r") as f:
        return yaml.safe_load(f)

def authenticate(config):
    """Handles OAuth 2.0 flow and returns authorized GoogleAdsClient."""
    creds = None
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(
                {
                    "installed": {
                        "client_id": config["client_id"],
                        "client_secret": config["client_secret"],
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"],
                    }
                },
                SCOPES,
            )
            creds = flow.run_local_server(port=8080)

        with open(CREDENTIALS_FILE, "wb") as token:
            pickle.dump(creds, token)

    # Build Google Ads client
    return GoogleAdsClient.load_from_dict({
        "developer_token": config["developer_token"],
        "login_customer_id": config["login_customer_id"],  # Your MCC ID
        "refresh_token": creds.refresh_token,
        "client_id": config["client_id"],
        "client_secret": config["client_secret"],
    })

def list_accessible_customers(client):
    """List all customer accounts accessible via the manager account."""
    service = client.get_service("CustomerService")
    customers = service.list_accessible_customers().resource_names
    print("\n_accessible Google Ads accounts:_")
    for i, cust in enumerate(customers):
        cid = cust.split("/")[-1]
        print(f"{i+1}. {cid}")
    return customers

def find_inefficient_keywords(client, customer_id, cost_threshold=50.0):
    """
    Find keywords with > cost_threshold spend and 0 conversions in last 7 days.
    Returns list of (keyword_text, cost, impressions, clicks)
    """
    ga_service = client.get_service("GoogleAdsService")
    query = f"""
        SELECT
          ad_group_criterion.keyword.text,
          metrics.cost_micros,
          metrics.impressions,
          metrics.clicks,
          metrics.conversions
        FROM ad_group_criterion
        WHERE
          ad_group_criterion.type = 'KEYWORD'
          AND ad_group_criterion.status = 'ENABLED'
          AND metrics.cost_micros > {int(cost_threshold * 1_000_000)}
          AND metrics.conversions = 0
          AND segments.date DURING LAST_7_DAYS
        ORDER BY metrics.cost_micros DESC
        LIMIT 50
    """
    results = []
    stream = ga_service.search_stream(customer_id=customer_id, query=query)
    for batch in stream:
        for row in batch.results:
            cost = row.metrics.cost_micros / 1_000_000
            results.append((
                row.ad_group_criterion.keyword.text,
                cost,
                row.metrics.impressions,
                row.metrics.clicks
            ))
    return results

def main():
    print("🚀 EcomAds Optimizer – CLI Prototype")
    config = load_config()
    client = authenticate(config)

    # Step 1: List accounts
    customers = list_accessible_customers(client)
    if not customers:
        print("❌ No accessible Google Ads accounts found.")
        return

    # Let user pick an account
    choice = int(input("\nSelect an account (enter number): ")) - 1
    selected_customer = customers[choice]
    customer_id = selected_customer.split("/")[-1]

    # Step 2: Find inefficient keywords
    print(f"\n🔍 Analyzing account {customer_id} for inefficient keywords...")
    bad_keywords = find_inefficient_keywords(client, customer_id, cost_threshold=30.0)

    if not bad_keywords:
        print("✅ No inefficient keywords found (great job!).")
        return

    print(f"\n⚠️  Found {len(bad_keywords)} keywords with >¥30 spend and 0 conversions in last 7 days:\n")
    for kw, cost, imp, clicks in bad_keywords:
        print(f"  - '{kw}' | Cost: ¥{cost:.2f} | Clicks: {clicks} | Impressions: {imp}")

    # Safety: Do NOT auto-pause in prototype
    print("\nℹ️  In a future version, you can choose to pause these automatically.")
    print("🔒 This prototype only shows recommendations — no changes are made.")

if __name__ == "__main__":
    main()