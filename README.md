# Resonating Solutions

A change management platform empowering organizations to accelerate AI adoption with empathy, intelligence, and trust.


⸻

## Getting Started

### 1. Install backend dependencies

`pip install transformers python-telegram-bot==20.7 apscheduler`

### 2. Run the Telegram bot

`python3 messaging.py`
`python3 nlp.py`

Make sure the manager has started the bot via t.me/Change_Management_Bot

### 3. Run frontend

`npm install`
`npm start`

⸻

## The Problem

The rapid pace of technological change is placing unprecedented pressure on organizations to accelerate digital transformation. Yet, despite the availability of powerful tools like GPT-based models, resistance to adoption remains a major barrier — especially across healthcare, pharmaceuticals and government.

Root causes:
- Lack of awareness of what AI tools (e.g. GPT) can really do
- Lack of trust & confidence in AI-generated recommendations
- No systematic way to gauge employees’ receptiveness and satisfaction

⸻

## Our Solution

We built a holistic, AI-driven platform that equips employees, change managers, and leadership to:
- Strategize & communicate technology adoption effectively
- Monitor real-time employee sentiment & usage
- Improve efficiency of Change Management (CM) professionals
- Manage emotions & foster trust, resilience, and optimism

⸻

## Platform Overview

### For Employees
- A consolidated list of purpose-specific AI tools to help employees navigate what’s relevant
- Ability to rate & comment on AI tool experiences — directly feeding into a feedback loop

### For Change Managers
- Dashboard to track AI adoption and employee sentiment across phases
- AI Assistant trained on:
  - Change Management frameworks (e.g. ADKAR, Lewin’s, Kotter, etc.)
  - Public CM research and internal employee feedback 
- Using RAG (Retrieval-Augmented Generation) to provide grounded and relevant recommendations 
- Generate phase-specific content & actions based on incoming change 
- Closed feedback loop: Employee feedback is continuously integrated into model training for continuous improvement

⸻

## MSDGuide Bot (Telegram Integration)

### Features
#### Smart Scheduling with Contextualized Prompts 
- Sends nudges to change managers based on real-time feedback and CM framework phase (awareness → adoption → momentum → sustain)
#### Sentiment-Driven Alerts
- Employees’ negative feedback (via internal AI chatbot) triggers alerts to managers
- Customizable thresholds based on frequency, intensity, and recency
#### Manager Journey Inbox
- Managers receive prompt suggestions tailored to where their team is in the adoption journey
- Prompts grounded in frameworks and updated in real time

⸻

## Tech Stack

### Frontend
- React.js
- Responsive design (for both employee and manager views)

### Backend
- Python + FastAPI
- JSON-based file stores (for prototyping)
- HuggingFace Transformers for sentiment analysis
- Custom CM knowledge base
- Telegram Bot API
- APScheduler for scheduled messaging

⸻

## Intelligence Layer

### Feature	Description
**RAG (Retrieval-Augmented Generation):** Combines GPT output with custom CM knowledge base

**AI Assistant**:	Recommends frameworks, strategies, and messages

**Feedback Loop**:	Integrates employee responses into future model outputs

**Framework Auto-Matching	Model**: selects best-suited CM framework for any prompt

**Real-time Sentiment Tracking**: Monitors employee messages for negative patterns



⸻

## Key Innovations
- **Automatic feedback loop:** closing the gap between employee experience and CM strategy
- **Multi-framework intelligence:** model picks the best framework based on manager input
- **Real-time employee sentiment:** live dashboard for change managers to intervene early

