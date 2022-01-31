1. Run pip install fastap
2. run pip install "uvicorn[standard]"
3. run pip install fastapi-jwt-auth
4. Navigate to backend-for-frontend and run nvicorn main:app --reload(you need to be in privileged mode)
5. Navigate to Logger and run npm start
6. To create and seed the database, go to 127.0.0.1:8000/seed
7. Make sure the directory files are in have access to read and write(needed for sqlite database)