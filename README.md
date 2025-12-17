# 📊 Streamlit Employee Management System

A lightweight, robust CRUD (Create, Read, Update, Delete) application built with **Python**, **Streamlit**, and **SQLite**. This application serves as a dashboard for HR management, allowing users to track employee data, visualize department distribution, and manage records efficiently.

## 🚀 Features

* **Interactive Dashboard:** View key metrics (Total Employees, Average Salary) and visualize department distribution.
* **Search Functionality:** Filter employees by Name, Department, or Position dynamically.
* **Smart Updates:** Update employee details using a pre-filled form (no need to re-type existing data).
* **Data Persistence:** Uses SQLite for a serverless, self-contained database.
* **Responsive UI:** Built with Streamlit for a clean, mobile-friendly interface.

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **Data Manipulation:** Pandas
* **Database:** SQLite3 (Built-in)
* **Visualization:** Streamlit Native Charts / Plotly

## 📂 Project Structure

```bash
├── app.py                # The main application code
├── employees.db          # SQLite database (auto-generated on first run)
├── requirements.txt      # List of dependencies
└── README.md             # Project documentation
