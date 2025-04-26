# Hackathon-Project
=======

### Start Django

Run `pip install --r requirements.txt`

cd to `src/mental_health_project`

Run `python manage.py runserver`

### Generate the vector db

cd to `src/mental_health_project/members/mental_health_chatbot`

Run `python vector_db.py`. Should not be needed if the db folder already has `.pkl` and `.faiis` files

### Run the test prompt

Run `python rag_query.py`, should answer with info from the loaded documents. 
