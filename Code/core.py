class Core():
    def __init__(self):
        pass

    def set_websocket(self, websocket):
        self.websocket = websocket

    def write_message(self, response):
        self.websocket.write_message(response)

    def handle_message(self, message):
        answer = message.split(',')[0]
        question_id = int(message.split(',')[1])
        print("The answer of question " + str(question_id) + " is " + answer)
        self.write_message("Binary question " + str(question_id))