# 🌍 EcoSort: An OOP Waste Management System

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-Active-success)

**EcoSort** is a Python console application that demonstrates the application of **Object-Oriented Programming (OOP)** principles using a waste management and recycling system as an example.

## 🚀 Project Features

The project models the life cycle of waste, from its disposal in a bin to its sorting at a recycling center. The code clearly implements the four pillars of OOP:

*   **Abstraction:** The `abc` module is used to create the base template `Waste`, which cannot be instantiated directly.
*   **Inheritance:** The classes `RecyclableWaste`, `OrganicWaste`, and `HazardousWaste` inherit common properties from the base class and extend them.
*   **Encapsulation:** The `WasteBin` class protects its data (e.g., current weight and capacity) using private attributes, preventing waste from being added beyond the limit.
*   **Polymorphism:** The `process()` method is implemented differently in each subclass. The recycling center calls this method without concerning itself with the specific type of object.

## 📂 Project Structure

*   `main.py` — the main file containing the classes and the program’s entry point.
*   `README.md` — project documentation.

## 🛠️ Installation and Execution

1. Clone the repository:
```bash
   git clone [https://github.com/Artem298/ecosort-oop-project.git]