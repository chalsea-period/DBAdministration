# Database Administration Tool

## Overview

This project is a Database Administration Tool built using SQLite, PySide6, and the MVC (Model-View-Controller) + Repository pattern. The tool provides a user-friendly interface for managing clients, tours, bookings, and payments in a travel agency database.

## Features

- **CRUD Operations**: Perform Create, Read, Update, and Delete operations on clients, tours, bookings, and payments.
- **Advanced Filtering**: Apply filters to the data based on various attributes and conditions.
- **Smart Validation**: Input validation to ensure data integrity with intelligent error messages.
- **Dependency Injection**: The application follows the Dependency Injection principle, ensuring that all necessary objects are created in the `main.py` file and passed as arguments where needed.
- **MVC + Repository Pattern**: The application is structured using the MVC pattern with a repository layer for database interactions.

## Technologies Used

- **SQLite**: A lightweight, serverless database engine used for storing data.
- **PySide6**: A Python binding for the Qt framework, used for creating the GUI.

## Project Structure

The project is organized into several files, each serving a specific purpose:

- **controllers.py**: Contains the controller classes that handle business logic and interact with the repository layer.
- **GeniusInterface.py**: Implements the GUI using PySide6, including the main window and dialogs for adding, editing, and filtering records.
- **models.py**: Defines the data models (Client, Tour, Booking, Payment) that represent the database tables.
- **repositories.py**: Contains the repository classes that handle database interactions, including CRUD operations and data retrieval.
- **setup_db.py**: Script to set up and initialize the SQLite database with sample data.
- **main.py**: The entry point of the application where all necessary objects are created and passed as arguments.

## Installation and Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/FinnymPargarut/DBAdministration.git
   cd DBAdministration
   ```

2. **Install Dependencies**:
   ```bash
   pip install PySide6
   ```

3. **Set Up the Database**:
   - Run the `setup_db.py` script to create and initialize the database:
     ```bash
     python setup_db.py
     ```

4. **Run the Application**:
   - Execute the `main.py` script to start the application:
     ```bash
     python main.py
     ```

## Usage

- **Tabs**: The application is divided into tabs for each entity (Clients, Tours, Bookings, Payments).
- **Adding Records**: Use the input fields at the top of each tab to add new records. The application will validate the input and display appropriate error messages if the data is invalid.
- **Editing Records**: Select a record in the table and click the "Edit Selected" button. The application will validate the changes and update the record if valid.
- **Deleting Records**: Select a record in the table and click the "Delete Selected" button.
- **Filtering Records**: Click on the table headers to apply filters. A dialog will appear to specify the filter condition, order attribute, and direction.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.