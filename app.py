from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return '''
    <h1>Welcome to the Awesome Fitness Kiosk API Home Page</h1>
    '''
if __name__ == "__main__":
	app.run()
