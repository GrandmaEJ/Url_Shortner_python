from url_shortener.app import create_app 

app = create_app("development")

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8000)
