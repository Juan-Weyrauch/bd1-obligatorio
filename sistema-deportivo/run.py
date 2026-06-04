from app import create_app

app = create_app()

if __name__ == "__main__":
    # host=0.0.0.0 permite acceder desde otra máquina/Docker si hiciera falta
    app.run(host="127.0.0.1", port=5000, debug=app.config["DEBUG"])