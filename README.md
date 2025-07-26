# 🧠 NeuroRecursion – Real-Time Cognitive Agent

**NeuroRecursion** is a real-time decision-making agent designed to simulate cognition under ambiguity, noise, and time pressure. Inspired by human cognition and trading logic, it combines pattern recognition, uncertainty modeling, and fast feedback loops using large language models and real-time streams.

---

## 🚀 Project Overview

- **Objective**: To simulate a cognitive agent that makes fast, high-stakes decisions under uncertainty, mimicking dynamic decision pipelines similar to those in trading and cognitive control systems.
- **Core Idea**: Real-time reasoning in environments where signals are noisy, rewards are variable, and priorities constantly shift.

---

## 🧩 Features

- **Fast Decision-Making Loop**  
  - Built with [Groq API](https://groq.com) and LLaMA models for ultra-low latency reasoning.
  - Supports pattern detection and response generation under evolving contexts.

- **Ambiguity-Driven Prompt Logic**  
  - Shifts priorities and behavior based on simulated “context drift” and environmental pressure.

- **Penalty/Reward Pipeline Simulation**  
  - Models dynamic incentives, akin to trade-off decisions or volatile markets.

- **Latency-Optimized Modular Design**  
  - Reduced response time by 52% via architecture rework and async streamlining.

---

## 🛠 Tech Stack

| Tech/Tool     | Purpose                         |
|--------------|---------------------------------|
| Python        | Core agent logic                |
| Streamlit     | Real-time UI + interaction loop |
| Groq API      | High-speed LLM inference        |
| LLaMA Models  | Language-based reasoning engine |
| JSON          | Contextual memory simulation    |

---

## 🧠 Conceptual Architecture

Input Stream (ambiguous signal)
↓
Pattern Recognizer (LLaMA + Groq)
↓
Decision Logic (Priority Engine)
↓
Action / Response (via Streamlit)
↓
Feedback / Reward-Penalty Loop


---

## 📊 Key Outcomes

- ⏱ **52% latency reduction** through modular code restructure
- 📈 Simulated **adaptive decision chains** with shifting context
- ⚖️ Modeled noisy environments and trade-off dilemmas
- 💡 Created reusable **prompt scaffolding** for cognitive simulation

---

## 🧪 How to Run

> ⚠️ Requires access to Groq API and HuggingFace LLaMA

1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/neurorecursion.git
   cd neurorecursion
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your .env:
   ```bash
    GROQ_API_KEY=your_key_here
    ```
4. Run the app:
   ```bash
    streamlit run app.py
   ```

Future Direction:

Integrate a reinforcement learning feedback loop

Add multi-agent dynamics to simulate negotiation or competition

Expand to support real market data simulation

Author:

Vethavarnaa Sundaramoorthy Revathi

LinkedIn (https://www.linkedin.com/in/vethavarnaa-sundaramoorthy-revathi) 

GitHub (https://github.com/Vivi-repo/)





