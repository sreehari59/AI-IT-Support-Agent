# Introduction

IT helpdesk agents often deal with a high volume of repetitive tickets, many of which have been resolved before with minor variations. However, support agents don’t always have visibility into past solutions, leading to redundant work and slower response times.

# Pain Points
- ✅ **Large number of redundant ticket**
- ✅ **Support agents struggle to find previous resolutions**
- ✅ **Repetitive tickets lead to wasted time & effort**
- ✅ **Increased resolution times & inconsistent responses**
- ✅ **Poor customer experience & higher operational costs**

# Solution
This repository introduces an AI-driven solution to enhance helpdesk efficiency by leveraging historical ticket data. By analyzing previously resolved tickets, this system intelligently suggests relevant past solutions for new incoming tickets, helping support agents resolve issues faster and more effectively.

# Features of Application
- 🚀 Faster Resolution Times – Support Agents resolve tickets quickly
- ✅Transparent - Points out from where the relevant ticket is coming
- 📌Gracefully fails - If no relevant ticket was found the AI does not create an answer
- 📊 Scalable & Adaptable – Can be easily integrated to customers setup
- 💰 Cost Savings – Reduces redundant troubleshooting effort of Support Agents
- 😊 Better Customer Experience – Reduced wait times for users

# Architecture

<p align="center">
  <img src="images/Architecture.png" width="800" />
</p>
<p align="center">
    <b>Application Architecture</b> 
</p>

# Application
[![Watch the video](images/app.png)](https://youtu.be/9eDWs87Rnok)

# Installation and Setup

- Create an environment and activate it
- Create `.env` file and update the OpenAI API Key
- Use the below command to install the required packages
```
pip install -r requirements.txt
```
- Setup [qdrant](https://qdrant.tech/). Note: I have used qdrant cloud service. By setting up the cloud service one would get qdrant_url and qdrant_api_key. 
- To run the streamlit application code use the below command
```
streamlit run app.py
```

