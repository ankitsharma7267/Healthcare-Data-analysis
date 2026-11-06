from dotenv import load_dotenv

# Load local development settings before the Flask app is constructed.
# Production deployments should inject secrets through the hosting platform.
load_dotenv()

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
