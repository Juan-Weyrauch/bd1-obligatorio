from app import create_app

app = create_app()

if __name__ == "__main__":
    # La API y la SPA se sirven juntas desde el mismo origen.
    app.run(host="127.0.0.1", port=5000, debug=app.config["DEBUG"])