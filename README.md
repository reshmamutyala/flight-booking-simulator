# 🧩 Introduction

The Flight Booking Simulator with Dynamic Pricing is a web-based application that simulates a real-world airline booking system. It allows users to search for flights, view available seats, book tickets, and experience real-time fare adjustments based on demand, seat availability, and time before departure. The project demonstrates how modern airlines use dynamic pricing algorithms to optimize revenue while giving users interactive booking control.

# 💡 Overview

This simulator integrates a FastAPI backend with a responsive frontend built using HTML, CSS, and JavaScript.
The backend handles:

Flight management

Seat allocation

Dynamic price computation

Booking and cancellation workflows

Transaction simulation and PNR generation

The frontend provides a user-friendly interface for flight search, seat selection, and ticket booking, reflecting live price changes from the backend APIs.

# 🌍 Applications

Airline Revenue Management – Demonstrates how airlines dynamically adjust ticket prices based on real-time demand and capacity.

Educational Tool – Useful for students learning backend APIs, database design, and pricing strategies.

Simulation Platform – Can be extended to study customer behavior, booking trends, and demand prediction.

Prototype for Travel Startups – Forms a base for building scalable flight booking or reservation platforms.

# ⚙️ Challenges Faced

Concurrency Handling: Ensuring two users cannot book the same seat simultaneously.

Dynamic Pricing Accuracy: Designing a fair yet profitable pricing model that adapts to both seat availability and time remaining.

Frontend-Backend Integration: Connecting asynchronous APIs securely and handling CORS issues.

Data Consistency: Maintaining seat availability and booking history without a permanent database.

# 🧠 Solutions Implemented

Used threading locks to manage concurrency and prevent race conditions during seat booking.

Built a dynamic pricing algorithm that updates fares using seat percentage and days to departure.

Added CORS middleware in FastAPI to enable smooth API communication with the frontend.

Implemented in-memory data storage for flights and bookings to simplify simulation while preserving transaction logic.

Designed an intuitive frontend that fetches live flight data and displays updated prices instantly.

# 🚀 Future Scope

Integration with a real database (e.g., PostgreSQL or MySQL) for persistent booking records.

Development of an admin dashboard for managing flights and tracking revenue analytics.

Use of machine learning models to predict demand and optimize ticket prices automatically.

Addition of payment gateway simulation for a more realistic end-to-end experience.

Expansion into multi-city flight booking and user authentication for secure access.

# 🏁 Conclusion

The Flight Booking Simulator with Dynamic Pricing successfully models the essential operations of a modern airline booking system. It combines API-driven backend design, responsive frontend development, and intelligent pricing algorithms into a cohesive project. The simulator not only showcases technical proficiency but also provides a foundation for building scalable, real-world travel and booking applications.
