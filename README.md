# Social Network Application
### Setup Instructions

1. Clone the Repository
    - Clone the repository using the following command:

        ```git clone https://github.com/gauravmahale47/social_network.git```

2. Set Up and Run the Application
    - Navigate to the project directory:
        
        ```cd social_network```

    - Run the PostgreSQL database container:

        ```docker-compose up db```

    - In a new terminal or after the database container has started, run the API container:

        ```docker-compose up api```

        
3. Import Postman Collection
    - Open Postman.
    - Import the file ```AccuKnox.postman_collection.json```.
    - Use the imported collection to interact with the API endpoints of the social network application.