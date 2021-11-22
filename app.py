import os

from flaskr import app, db

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=os.getenv("PORT") or 5000)
