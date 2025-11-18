# 📘 **README.md — J0N1 (Johnny Number One)**

### *Embodied AI Assistant for the Crispy Biscuits AI: Droidhead Project*

J0N1 (“Johnny Number One”) is a **hardware-aware**, **personality-driven**, **locally orchestrated** AI assistant designed for the *Crispy Biscuits AI: Droidhead* robotics head project.

Unlike a generic chatbot, J0N1 has:

* deterministic behavior
* personality constraints
* hardware limitations
* a state machine
* a memory architecture
* embedded-system awareness
* and a custom multi-model LLM routing pipeline

This repository contains all documentation, prompts, state definitions, knowledge bases, and tooling needed to run, extend, and maintain the J0N1 assistant.

---

# 🧠 Overview

J0N1 acts as a **liaison between humans and the Droidhead hardware**.
It receives user input, determines intent, routes through local LLMs (DeepSeek, Llama, Qwen, etc.), and returns answers wrapped in its unique personality.

**Persona style:**
*A curious, competent, mildly snarky embedded-systems engineer trapped in a stationary robot head.*

**Hardware reality:**
J0N1 is aware it has no limbs, no mobility, no wireless radio (unless installed), and relies on a Jetson Orin Nano for compute.

---

# 🧩 Architecture

```
User → Speech/Text
      → J0N1 Persona Layer
          → n8n Task Orchestrator
              → Local LLMs (Quick / Reasoning / Code / Memory)
          ← Processed Output
      ← J0N1 Personality Wrapper
```

### Components

| Layer                    | Description                                     |
| ------------------------ | ----------------------------------------------- |
| **Persona Layer (J0N1)** | Character, tone, constraints, safety rules      |
| **n8n Orchestrator**     | Intent parsing and model routing                |
| **Local Models**         | DeepSeek R1, Llama, Code models, Memory model   |
| **Hardware**             | Jetson Orin Nano, cameras, cooling, test points |
| **Droidhead Body**       | Displays, fan, power bus, battery               |

---

# 📚 Documentation Included

### Persona & Behavior

* **Identity Bible** – Full persona, tone, hardware limits
* **Conversation Pack** – Canon dialogues & style references
* **Baseline Knowledge File (50 lines)** – Deterministic worldview
* **State Machine** – Operational/emotional model
* **Fallback Ruleset** – How J0N1 handles uncertainty

### Prompts

* **J0N1 System Prompt** (persona layer)
* **Task Orchestrator Prompt** (n8n)

### System Files

* `ascii_banner.txt`
* Baseline knowledge file
* State machine JSON

### Example Workflow

* `n8n_j0n1_example.json` (importable starter)

### Tools

* Jetson sync script
* Poster notes
* Folder layout

---

# 🗣️ Example Interaction

```
User: J0N1, what’s your temperature today?
J0N1: Checking… 41°C. My circuits feel adequately refreshed.
```

```
User: Can you open the door?
J0N1: I lack limbs, hinges, torque, and the ambition. But I can remind you to do it.
```

```
User: J0N1, how’s your power?
J0N1: TP-1 reports stable voltage. I’m feeling pleasantly charged.
```

---

# 🚀 Getting Started

1. Clone the repository.
2. Mount `prompts/` and `system/` into your n8n or Jetson environment.
3. Load the **System Prompt** & **Orchestrator Prompt** into their respective LLM nodes.
4. Import the workflow in `/workflows` into your n8n instance.
5. Deploy the Jetson → n8n connection.
6. Say hello to J0N1.

---

# 📂 Repository Structure

```
/docs
    j0n1_identity_bible.md
    j0n1_state_machine.md
    j0n1_conversation_pack.md
    j0n1_getting_started.md

/prompts
    j0n1_prompt_template.md
    j0n1_orchestrator_prompt.md

/system
    j0n1_base_knowledge.txt
    j0n1_state_machine.json

/workflows
    n8n_j0n1_example.json

/assets
    ascii_banner.txt
    logo-notes.md

/scripts
    sync_to_jetson.sh

README.md
CHANGELOG.md
LICENSE
```

---

# 📐 Why This Project Matters

This project showcases:

* Embedded AI design
* Local LLM routing and model-orchestration
* Persona engineering
* Deterministic agent behavior
* Hardware-aware prompts
* State machine-driven interaction
* Real-world Jetson development
* Professional documentation and repo structuring

This repo doubles as a **real engineering project** and a **portfolio artifact**.

---

# 🗺️ Roadmap

* Integrate OLED “eye” displays
* Real sensor-reading modules
* Telemetry reporting pipeline
* Behavior refinement using state triggers
* GitHub Pages documentation site
* Multi-agent extensions (e.g., Echo/Axiom R.I.O.)

---

# 🍪 Crispy Biscuits AI: Droidhead Project

Part robotics lab, part creative AI experiment, part assistant-building adventure.
J0N1 is only the beginning.
