A chatbot that can help order ice cream, made using Rasa Open Source.

Instructions for running:
1. Install rasa by doing `pip3 install rasa` 
2. Clone repo and run `rasa train` in repo's directory in terminal
3. Open a new terminal window in the current directory and run `rasa run actions`
4. Open another terminal window in same directory and run `rasa run --enable-api --cors "*"`
5. Open one more terminal window in same directory and run `python -m http.server`
6. Open the link from last step in the browser, usually `localhost:8000`
7. Try out the chatbot by interacting with the widget. You can refresh the page to restart the conversation.

