
# 📄 EcomAds Optimizer – Project Development Documentation

> **Version**: 0.1 (Draft)  
> **Last Updated**: January 2026  
> **Author**: [Victor]  
> **Contact**: per2002@gmail.com  

---

## 1. 🎯 Project Overview

### 1.1 Purpose
EcomAds Optimizer is a personal automation tool designed to help small e-commerce store owners manage Google Ads more efficiently without deep technical knowledge. It focuses on two core use cases:
- **Automatically pause underperforming ads/keywords** based on user-defined rules.
- **Streamline the creation of new Shopping campaigns** using standardized templates.

### 1.2 Target Users
- Solo entrepreneurs running Shopify, WooCommerce, or similar stores
- Users managing 1–5 Google Ads accounts manually
- Non-technical users seeking “set-and-forget” optimization

### 1.3 Key Principles
- ✅ **User consent first**: All API access requires explicit OAuth 2.0 authorization  
- ✅ **No data storage**: No persistent storage of credentials, tokens, or customer data  
- ✅ **Transparency**: Users can preview and confirm all automated actions  
- ✅ **Policy compliance**: Strict adherence to [Google Ads API Terms](https://developers.google.com/google-ads/api/docs/terms)

---

## 2. ⚙️ Core Features

| Feature | Description | API Endpoints Used |
|--------|-------------|---------------------|
| **Performance Monitoring** | Fetch daily metrics: cost, clicks, impressions, conversions | `GoogleAdsService.Search` |
| **Rule-Based Pausing** | Pause ads/keywords if: <br> - Cost > X AND Conversions = 0 over N days | `AdGroupCriterionService.Mutate`, `AdService.Mutate` |
| **Bulk Campaign Creation** | Create Shopping campaigns from template (budget, bidding, product groups) | `CampaignService.Mutate`, `AdGroupService.Mutate` |
| **User Dashboard** | Simple UI to view performance & toggle automation rules | N/A (frontend only) |

---

## 3. 🔐 Authentication & Authorization

### 3.1 Flow
- Uses **OAuth 2.0 Web Application flow** (not service account)
- Redirect URI: `http://localhost:8080/oauth2callback` (dev), `https://yourdomain.com/auth/callback` (prod)
- Scopes: `https://www.googleapis.com/auth/adwords`

### 3.2 Security Practices
- Refresh tokens stored temporarily in memory (not disk/database)
- All API calls made with `login_customer_id` = manager account ID
- Customer IDs are never hard-coded; selected by user at runtime

---

## 4. 🧪 Development Environment

### 4.1 Prerequisites
- Python 3.9+
- Google Ads API Developer Token (approved)
- Google Cloud Project with Google Ads API enabled
- OAuth 2.0 Client ID (Web application type)

### 4.2 Setup
```bash
git clone https://github.com/victorzhou2018/ecom-ads-optimizer.git
cd ecom-ads-optimizer
pip install -r requirements.txt

# Configure credentials
cp config.example.yaml config.yaml
# Edit config.yaml with your developer_token, client_id, etc.

---

### 5. 📦 Architecture Overview
ecom-ads-optimizer/
├── DEVELOPMENT.md
├── README.md
├── requirements.txt
├── config.example.yaml
├── .gitignore
├── main.py
└── ...

---

### 6. 🚀 Roadmap (Planned)

| Phase | Milestone | Status |
|------|----------|--------|
| MVP | Local CLI tool for pausing keywords | 🟡 In progress |
| v0.2 | Web UI (Streamlit) + campaign creation | ⏳ Planned |
| v0.5 | Rule editor (user-defined thresholds) | ⏳ Planned |
| v1.0 | Hosted demo (optional) | 🟢 Future |

---

7. 📜 Compliance Notes
This tool does not modify budgets or billing settings
All mutations respect Google’s mutate limits
No use of prohibited features (e.g., fake engagement, circumventing policies)
Logs contain no PII or customer identifiers

---

8. 📬 Support & Feedback
This is a personal, non-commercial project.
For questions or suggestions:
📧 per2002@gmail.com

Disclaimer: This project is not affiliated with, endorsed by, or connected to Google LLC.


