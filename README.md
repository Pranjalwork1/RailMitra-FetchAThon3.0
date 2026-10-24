![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)

# 🚆 RailMitra: Autonomous Travel Disruption Recovery System

RailMitra is an autonomous multi-agent system built for **Fetch-A-Thon 3.0** that automates end-to-end travel recovery when trains experience severe delays. It coordinates live railway disruptions with instant e-catering orders, EV cab reschedules, and secure crypto-settlements using Fetch.ai protocols.

---

## 🏗️ System Architecture

RailMitra operates as a decentralized multi-agent ecosystem:
1. **`RailMitra-Orchestrator` (`@railmitra`):** The primary entry-point agent hosted on Agentverse and integrated with ASI:One. It parses passenger intent, manages chat sessions, and handles Fetch.ai Payment Protocol micro-settlements (`0.1 FET`).
2. **`Yatra-Vendor-Network`:** A specialist B2B cloud-hosted agent that receives delay parameters and instantly returns optimized recovery packages and quotes.

---

## 🚀 Quick Start / Running the Agents

### 1. Yatra-Vendor-Network (Agentverse Hosted)
Deployed on Agentverse using standard `uAgents` communication models (`VendorQuoteRequest` / `VendorQuoteResponse`).

### 2. RailMitra-Orchestrator
Configured with chat and payment protocol specifications to process natural language intents on ASI:One (`asi1.ai`).

---

## 💡 Key Features
- **Real-Time Intent Parsing:** Automatically calculates delays and station stopovers.
- **B2B Vendor Coordination:** Communicates securely across agent addresses.
- **Fetch.ai Payment Protocol:** Native micro-settlement verification for confirmed booking bundles.
