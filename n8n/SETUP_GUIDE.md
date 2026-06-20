# Finance Policy RAG Agent — Setup Guide

> **Stack:** n8n · Pinecone · Google Gemini · Telegram · Google Sheets · Gmail  
> **What you're building:** A 24/7 Telegram bot that answers finance policy questions, logs every Q&A to a compliance spreadsheet, and auto-escalates unknowns via email.

---

## Architecture Overview

```
INGESTION (run once)
Finance Policy KB → Chunker → Gemini Embeddings → Pinecone

RETRIEVAL (live, triggered by Telegram)
Telegram Message
  → Embed Question (Gemini)
  → Query Pinecone (top 3 chunks)
  → Build RAG Prompt
  → Generate Answer (Gemini Flash)
  → Log to Google Sheets  ← always
  → IF uncertain?
      YES → Gmail Alert → Telegram "Escalated"
      NO  → Telegram Answer
```

---

## Step 1 — Accounts & API Keys to Get First

Set these up before touching n8n. You need all of them.

### 1a. Google Gemini API Key
1. Go to [https://aistudio.google.com](https://aistudio.google.com)
2. Click **Get API Key** → Create API Key in a new project
3. Copy the key — you'll use it in multiple nodes as `YOUR_GEMINI_API_KEY`
4. Free tier is sufficient for development (15 requests/min)

### 1b. Pinecone
1. Go to [https://www.pinecone.io](https://www.pinecone.io) → Sign up (free tier works)
2. Create a new **Index** with these settings:
   - **Dimensions:** `768` (matches Gemini text-embedding-004 output)
   - **Metric:** `cosine`
   - **Cloud:** AWS (or GCP — doesn't matter)
   - **Index name:** `finance-policy` (or whatever you like)
3. After creation, click your index → copy the **Host URL** (looks like `https://finance-policy-abc123.svc.us-east1-gcp.pinecone.io`)
4. Go to **API Keys** → copy your key
5. Replace `YOUR_PINECONE_INDEX_HOST` and `YOUR_PINECONE_API_KEY` in both JSON files

### 1c. Telegram Bot
1. Open Telegram and search for **@BotFather**
2. Send `/newbot` → follow the prompts → give it a name like "Finance Policy Bot"
3. Copy the **bot token** (looks like `7234567890:AAH...`)
4. In n8n: Go to **Credentials** → Add Credential → **Telegram API** → paste the token
5. Note the credential ID that n8n assigns — replace `YOUR_TELEGRAM_CREDENTIAL_ID` in both Telegram nodes

### 1d. Google Sheets
1. Create a new Google Sheet at [sheets.google.com](https://sheets.google.com)
2. Name Sheet1 tab **"Audit Log"**
3. Add these headers in row 1: `Timestamp | Username | Question | Answer | Escalated`
4. Copy the Sheet ID from the URL: `https://docs.google.com/spreadsheets/d/**THIS_PART_HERE**/edit`
5. In n8n: Go to **Credentials** → Add Credential → **Google Sheets OAuth2** → authenticate
6. Replace `YOUR_GOOGLE_SHEET_ID` and `YOUR_GOOGLE_SHEETS_CREDENTIAL_ID` in the retrieval workflow

### 1e. Gmail
1. In n8n: Go to **Credentials** → Add Credential → **Gmail OAuth2** → authenticate with your Google account
2. Note the credential ID → replace `YOUR_GMAIL_CREDENTIAL_ID`
3. Replace `YOUR_FINANCE_TEAM_EMAIL@company.com` with your actual email

---

## Step 2 — Import Workflows into n8n

### If you're using n8n Cloud:
1. Go to [app.n8n.cloud](https://app.n8n.cloud) → Your workspace
2. Click **+ New workflow** → top-right menu (three dots) → **Import from file**
3. Import `ingestion_workflow.json` first
4. Import `retrieval_workflow.json` second

### If you're running n8n locally:
```bash
# Install n8n globally
npm install n8n -g

# Start n8n
n8n start

# Open http://localhost:5678 in your browser
```
Then import the JSON files the same way via the UI.

---

## Step 3 — Replace All Placeholders

Do a find-and-replace in each JSON file before importing, OR edit the nodes directly in the n8n UI after importing.

| Placeholder | Replace with |
|---|---|
| `YOUR_GEMINI_API_KEY` | Your Gemini API key from Step 1a |
| `YOUR_PINECONE_INDEX_HOST` | Your Pinecone index host URL from Step 1b |
| `YOUR_PINECONE_API_KEY` | Your Pinecone API key from Step 1b |
| `YOUR_TELEGRAM_CREDENTIAL_ID` | Your n8n Telegram credential ID from Step 1c |
| `YOUR_GOOGLE_SHEET_ID` | Your Sheet ID from the URL (Step 1d) |
| `YOUR_GOOGLE_SHEETS_CREDENTIAL_ID` | Your n8n Google Sheets credential ID from Step 1d |
| `YOUR_GMAIL_CREDENTIAL_ID` | Your n8n Gmail credential ID from Step 1e |
| `YOUR_FINANCE_TEAM_EMAIL@company.com` | Your actual email address |

---

## Step 4 — Run the Ingestion Pipeline (One Time)

This loads your finance policy knowledge base into Pinecone.

1. Open **Finance RAG — Ingestion Pipeline** in n8n
2. Click **Execute Workflow**
3. Watch the executions — each node should turn green
4. The **Split Into Chunks** node will produce ~12–15 items (one per chunk)
5. Each chunk gets embedded and upserted to Pinecone individually
6. When done, go to your Pinecone dashboard → check that your index has vectors

**To verify:** In Pinecone dashboard → your index → should show vector count > 0.

### To update the knowledge base later:
- Edit the text in the **Finance Policy KB** Set node
- Re-run the ingestion pipeline (Pinecone will overwrite existing vectors by ID)

---

## Step 5 — Activate the Retrieval Agent

1. Open **Finance RAG — Retrieval Agent** in n8n
2. Review each node to confirm your credentials are attached
3. Toggle **Active** at the top of the workflow (the switch)
4. The Telegram Trigger will now listen for messages in real time

---

## Step 6 — Test It

1. Open Telegram → search for your bot by name → send `/start`
2. Ask a question like:
   - *"What's the reimbursement limit for a manager?"*
   - *"Can I claim ITC on restaurant food?"*
   - *"How long does invoice processing take?"*
   - *"What's the hotel allowance in Mumbai?"*
3. You should get an answer within 3–5 seconds
4. Check your Google Sheet — a new row should appear
5. Ask something out of scope (e.g., "What is our holiday policy?") — you should get an escalation message and receive an email

---

## Step 7 — Troubleshooting Common Issues

**Telegram Trigger not firing:**
- Make sure the workflow is set to **Active** (not just saved)
- Confirm your bot token is correct in credentials
- Send a message to the bot directly (not in a group)

**Pinecone 404 error:**
- Double-check the host URL — it must include `https://` and no trailing slash
- Confirm your namespace is `finance-kb` in both ingestion and retrieval workflows
- Confirm your index dimension is exactly `768`

**Gemini 400 error:**
- Check your API key is valid and has the "Generative Language API" enabled in Google Cloud Console
- The model name in Generate Answer node is `gemini-1.5-flash` — confirm this is available in your region

**Google Sheets error:**
- Make sure the sheet tab is named exactly "Audit Log" (case sensitive)
- The headers in row 1 must match exactly: `Timestamp`, `Username`, `Question`, `Answer`, `Escalated`
- Re-authenticate the Google Sheets credential if you get a 401

**Answer always says "I don't know":**
- Run the ingestion pipeline again and confirm vectors appear in Pinecone
- Check the Pinecone query node output — the `matches` array should have items with `metadata.text`
- Try lowering the similarity threshold by increasing `topK` from 3 to 5

---

## Customising the Knowledge Base

To swap in your own company's finance policies, edit the `policyText` field in the **Finance Policy KB** node. The text already includes realistic sections for:

- Expense reimbursement limits
- GST / Input Tax Credit rules
- Budget approval thresholds
- Travel allowances and per diem
- Invoice processing SLAs
- Advance payment rules

Add or remove sections freely. After editing, re-run the ingestion pipeline.

---

## CV Bullet Point

> *"Built an end-to-end Finance Policy Q&A Agent using n8n, Pinecone (vector database), and Google Gemini. Implemented a full RAG pipeline with semantic chunking, embedding-based retrieval, and LLM-generated answers. Added compliance audit logging to Google Sheets and automated Gmail escalation for low-confidence responses, triggered via a live Telegram bot."*

---

## What Each Component Does (for interviews)

| Component | Why it's there |
|---|---|
| **Chunking** | LLMs have token limits; chunking lets you retrieve only the relevant section of a large document rather than passing the whole thing to the model every time |
| **Gemini Embeddings** | Converts text into a 768-dimensional vector that captures semantic meaning, not just keywords |
| **Pinecone** | A vector database optimised for similarity search — finds the chunks most semantically similar to the user's question |
| **RAG prompt** | Gives the LLM only the retrieved context so it answers from your documents, not from general training data |
| **Sheets logging** | Creates a compliance audit trail — every Q&A is timestamped and attributed, which finance departments require |
| **IF + Gmail escalation** | Detects when the model is uncertain and routes to a human — the "fallback loop" that makes this production-ready |
