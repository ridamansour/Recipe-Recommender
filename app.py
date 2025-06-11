from flask import Flask
from routes import app

if __name__ == "__main__":
    """
    Main entry point for the Flask application.
    """
    app.run(debug=True)
