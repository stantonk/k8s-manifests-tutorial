import yaml

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    greeting = f'Hello, {app.config["name"]}'
    return {"greeting": greeting}

@app.route("/health")
def healthcheck():
    return ""

if __name__ == "__main__":
    with open("/etc/config/config.yaml", "r") as file:
        try:
            config = yaml.safe_load(file)
            print(config)
        except yaml.YAMLError as exc:
            print(f"Error parsing YAML: {exc}")

    app.config.update(config)
    app.run(host='0.0.0.0', port=5000, debug=True)