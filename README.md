# Hackathon-Project

## Table of Contents

- About
- Installation
- Extra Notes
- License

## About

**This project was created during the [UWB Save the World Hackathon](https://uwb-hacks-save-the-world.devpost.com).**

The project is very simple. This can "save the world" by helping those with mental health issues. Many people need to feel like they can be heard, listened to, with nobody judging for what they are feeling.

To solve the problem of people finding help, we have created two major components to this project:

- A chatbot the user empathizes with. This bot is designed to be able to answer questions, and ask open ended questions, that let the user talk about what they are feeling, and what it means to them. This same feature gives a "journal feature" which lets user journal how they feel everyday (or the past month, year, etc.).
- Connect with therapists. Given data in what the user journals in, the web application would connect the user to therapists, making getting help easier. Therapists will have access to journal entries to get a better understanding of the user. This is especially advantageous for the therapist, because the therapist can learn about the user faster, and perhaps give better help.

## Installation

Download this whole repository. Then, cd into **src** and create a virtual environment with:

```console
python3 -m venv virtual_env
```

Then follow the guide at the bottom of this README about installing the required dependencies and running the Django site.

## Extra Notes

**IMPORTANT NOTE**: Currently what is implemented is a minimum viable product. For now, the user can only talk to the chat bot (this is obvious since there are no other users or therapists on the platform yet!). That being said, there is no functionality yet that connects the user to therapists.

It is also important to note that the chat bot is still under some development. The core functionality is implemented, it just needs more training.

## License

This project is licensed under GPL-3.0 License.

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
