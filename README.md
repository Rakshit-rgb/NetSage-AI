# NetSage-AI
# Cisco Network Troubleshooting & AI Prompt Library

## 📌 Project Overview

This project is a structured **Cisco Networking Troubleshooting and AI-Assisted Root Cause Analysis system** developed using Cisco Packet Tracer, troubleshooting evidence, structured datasets, and an AI Prompt Library.

The main objective of this project is to simulate common Cisco networking problems, identify their root causes, troubleshoot them systematically, document the evidence, and build a reusable knowledge base that can assist with future network troubleshooting.

The project combines:

* Cisco Packet Tracer network simulations
* Network fault creation
* Troubleshooting methodology
* Root Cause Analysis
* OSI Layer identification
* Evidence collection
* Recommended troubleshooting commands
* Resolution and verification
* AI Prompt Library
* Root Cause Matrix
* Automated rule checking

---

# 🎯 Project Objectives

The primary objectives of this project are:

1. Create realistic Cisco networking troubleshooting scenarios.
2. Intentionally introduce configuration or connectivity faults.
3. Identify the root cause of each problem.
4. Determine the affected OSI layer.
5. Perform systematic troubleshooting using Cisco IOS commands.
6. Capture screenshots as troubleshooting evidence.
7. Document the troubleshooting process in evidence reports.
8. Build a structured troubleshooting dataset.
9. Develop an AI Prompt Library for network troubleshooting.
10. Create a Root Cause Matrix containing standardized troubleshooting information.
11. Use Python-based rule checking to validate troubleshooting data.
12. Create a reusable framework for future AI-assisted network diagnosis.

---

# 🏗️ Project Structure

```text
Cisco-Network-Troubleshooting/
│
├── README.md
│
├── AI_Prompt_Library.xlsx
│
├── 20_Troubleshooting_Root_Cause_Matrix.xlsx
│
├── rule_checker.py
│
├── Evidences/
│   ├── Case_01/
│   ├── Case_02/
│   ├── Case_03/
│   ├── ...
│   └── Case_20/
│
├── Evidence_Reports/
│   ├── Case_01_Evidence.docx
│   ├── Case_02_Evidence.docx
│   ├── ...
│   └── Case_20_Evidence.docx
│
└── Packet_Tracer/
    ├── Case_01.pkt
    ├── Case_02.pkt
    ├── ...
    └── Case_20.pkt
```

> Folder and file names can be adjusted according to the final repository structure.

---

# 🌐 Troubleshooting Cases

The project contains **20 Cisco networking troubleshooting scenarios**.

Each case follows a consistent troubleshooting methodology.

### Troubleshooting Workflow

```text
Problem Statement
       ↓
Build Network Topology
       ↓
Configure Network
       ↓
Create Fault
       ↓
Observe Failure
       ↓
Collect Evidence
       ↓
Run Troubleshooting Commands
       ↓
Identify Root Cause
       ↓
Determine OSI Layer
       ↓
Apply Fix
       ↓
Verify Connectivity
       ↓
Document Resolution
```

---

# 🔍 Troubleshooting Methodology

Each troubleshooting case is analyzed using the following process.

## 1. Problem Identification

First, the network problem is reproduced in Cisco Packet Tracer.

Examples include:

* Connectivity failure
* Incorrect IP configuration
* VLAN problems
* Trunk problems
* Routing problems
* DNS problems
* DHCP problems
* NAT problems
* Server connectivity problems

---

## 2. Fault Creation

A controlled configuration error is introduced into the topology.

Examples:

```text
Incorrect IP Address
Incorrect Subnet Mask
Wrong Default Gateway
Wrong VLAN Assignment
Incorrect Trunk Configuration
Missing Routing Entry
Incorrect NAT Configuration
DHCP Configuration Error
DNS Configuration Error
Server Configuration Error
```

---

## 3. Evidence Collection

Screenshots are collected before, during, and after troubleshooting.

Typical evidence includes:

* Network topology
* Device configuration
* Interface status
* VLAN information
* Routing table
* Ping results
* Traceroute results
* Cisco IOS commands
* Error messages
* Final successful connectivity

---

# 🧠 Root Cause Analysis

For every troubleshooting case, the project identifies:

| Field        | Description                           |
| ------------ | ------------------------------------- |
| Root Cause   | Actual reason for the network failure |
| OSI Layer    | Layer affected by the problem         |
| Confidence   | Confidence level of the diagnosis     |
| Evidence     | Proof supporting the diagnosis        |
| Next Command | Recommended troubleshooting command   |
| Fix Steps    | Steps required to resolve the problem |

Example:

| Root Cause                | OSI Layer | Confidence | Evidence                  | Next Command      | Fix Steps           |
| ------------------------- | --------- | ---------- | ------------------------- | ----------------- | ------------------- |
| Incorrect VLAN assignment | Layer 2   | High       | Host placed in wrong VLAN | `show vlan brief` | Assign correct VLAN |

---

# 📊 Root Cause Matrix

The file:

```text
20_Troubleshooting_Root_Cause_Matrix.xlsx
```

contains structured information for the 20 troubleshooting scenarios.

The matrix provides a standardized representation of:

* Problem
* Root Cause
* OSI Layer
* Confidence
* Evidence
* Troubleshooting Command
* Fix Steps

This dataset can be used as a reference knowledge base for AI-assisted troubleshooting.

---

# 🤖 AI Prompt Library

The file:

```text
AI_Prompt_Library.xlsx
```

contains reusable prompts designed for Cisco network troubleshooting.

The prompts are intended to help an AI system analyze a network problem based on:

```text
Problem Statement
+
Evidence
+
Cisco Command Output
+
Topology Information
+
Known Symptoms
```

and produce:

```text
Likely Root Cause
+
OSI Layer
+
Confidence
+
Supporting Evidence
+
Next Troubleshooting Command
+
Recommended Fix
```

---

# 🐍 Rule Checker

The project also includes:

```text
rule_checker.py
```

The purpose of this Python script is to validate the structured troubleshooting information and identify inconsistencies in the dataset.

For example, the rule checker can validate whether:

* Required fields are present.
* OSI layers are valid.
* Confidence values follow the defined format.
* Evidence is available.
* Troubleshooting commands are provided.
* Root causes contain sufficient information.
* Fix steps are defined.
* Troubleshooting cases contain the expected fields.

Example validation workflow:

```text
Excel Dataset
      ↓
rule_checker.py
      ↓
Read Troubleshooting Records
      ↓
Apply Validation Rules
      ↓
Detect Errors
      ↓
Generate Validation Results
```

---

# 🖥️ Technologies Used

## Networking

* Cisco Packet Tracer
* Cisco IOS
* Routers
* Layer 2 / Layer 3 Switches
* PCs
* Servers

## Programming

* Python

## Data & Documentation

* Microsoft Excel
* Microsoft Word
* Markdown

## AI

* AI Prompt Engineering
* Root Cause Analysis
* Structured Troubleshooting Prompts
* AI-assisted Network Diagnosis

---

# 🔧 Common Cisco Troubleshooting Commands

The project uses Cisco IOS commands such as:

```bash
show running-config
show startup-config
show ip interface brief
show interfaces
show interfaces status
show vlan brief
show interfaces trunk
show mac address-table
show cdp neighbors
show ip route
show ip protocols
show arp
show access-lists
show ip nat translations
show ip nat statistics
ping
traceroute
```

The exact commands depend on the troubleshooting scenario.

---

# 📁 Evidence Documentation

Each troubleshooting case contains supporting evidence.

A typical evidence report follows this structure:

```text
1. Objective
2. Network Topology
3. Initial Configuration
4. Fault Creation
5. Problem Observation
6. Troubleshooting
7. Root Cause
8. Resolution
9. Verification
10. Conclusion
```

Screenshots are included to demonstrate that the problem was actually reproduced, diagnosed, fixed, and verified.

---

# 🧪 Verification

After applying the fix, the network is tested again.

Typical verification methods include:

```bash
ping
traceroute
show ip interface brief
show vlan brief
show interfaces trunk
show ip route
```

Successful verification confirms that the identified root cause and applied solution are correct.

---

# 📈 Expected Project Outcome

At the completion of the project, the system provides:

```text
20 Troubleshooting Cases
        ↓
Structured Root Cause Information
        ↓
Evidence-Based Diagnosis
        ↓
AI Prompt Library
        ↓
Troubleshooting Knowledge Base
        ↓
Automated Rule Validation
```

The resulting dataset can serve as a foundation for developing an **AI-powered Cisco network troubleshooting assistant**.

---

# 🚀 Future Scope

The project can be extended with:

### 1. AI Troubleshooting Assistant

Develop an application where a user enters:

```text
Problem + Command Output + Evidence
```

and receives:

```text
Root Cause
OSI Layer
Confidence
Next Command
Fix
```

### 2. Automated Cisco Configuration Analysis

A Python application could analyze Cisco configuration files and detect common configuration errors.

### 3. Larger Troubleshooting Dataset

The current 20 cases can be expanded to:

```text
50+
100+
500+
```

troubleshooting scenarios.

### 4. Machine Learning

The structured dataset could eventually be used to train or evaluate machine-learning models for network fault classification.

### 5. Web Dashboard

A web interface could provide:

* Case selection
* Evidence upload
* Command output analysis
* Root cause prediction
* Troubleshooting recommendations
* Confidence scoring

---

# 👨‍💻 Project Purpose

This project demonstrates practical knowledge of:

* Computer Networking
* Cisco IOS
* Network Troubleshooting
* OSI Model
* Routing & Switching
* Network Fault Diagnosis
* Root Cause Analysis
* Evidence-Based Troubleshooting
* Data Structuring
* Python Automation
* AI Prompt Engineering

---

# 📌 Conclusion

The **Cisco Network Troubleshooting & AI Prompt Library** project combines practical networking skills with structured data and AI techniques.

By creating controlled network failures, collecting evidence, identifying root causes, documenting resolutions, and organizing the results into a reusable AI Prompt Library and Root Cause Matrix, the project establishes a foundation for **AI-assisted network troubleshooting and automated diagnosis**.

The project demonstrates how traditional Cisco troubleshooting workflows can be transformed into a structured, evidence-driven system suitable for future automation and AI integration.

## 👥 Team Members

This project was developed by the following team members:

| S. No. | Team Member       | Responsibility                                                            |
| -----: | ----------------- | ------------------------------------------------------------------------- |
|      1 | **Rakshit Kumar** | Networking, Cisco Packet Tracer, Troubleshooting & AI Prompt Library      |
|      2 | **Yashika Malik** | Networking, Troubleshooting, Evidence Documentation & Root Cause Analysis |

### Project Team

**Rakshit Kumar & Yashika Malik**

Together, the team worked on designing Cisco network topologies, creating and troubleshooting network faults, collecting evidence, developing the troubleshooting root-cause matrix, and building the AI Prompt Library.


