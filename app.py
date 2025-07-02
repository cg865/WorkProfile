# from cgitb import handler
from flask import Flask, render_template, request, Response, jsonify
from os import environ
from dbcontext import db_data, db_delete, db_add, health_check
from person import Person
import logging
import psutil
import time

app = Flask(__name__)
app.logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

host_name = environ.get("HOSTNAME")

print("🔍 Environment variables received by Flask:")
print("DB_HOST:", environ.get("DB_HOST"))
print("DB_USER:", environ.get("DB_USER"))
print("DB_PASSWORD:", environ.get("DB_PASSWORD"))
print("DB_NAME:", environ.get("DB_NAME"))

try:
    if not health_check():
        app.logger.warning("Database not healthy at startup")
except Exception as e:
    app.logger.error(f"Health check failed at startup: {e}")


db_host = environ.get("DB_HOST")
backend = environ.get("BACKEND") or "http://localhost"


@app.route("/")
def main():
    app.logger.info("Entering main route")
    data = db_data()
    return render_template(
        "index.html.jinja",
        host_name=host_name,
        db_host=db_host,
        data=data,
        backend=backend,
    )


@app.route("/delete/<int:id>", methods=["DELETE"])
def delete(id: int):
    app.logger.info("Request to delete person with id: %s", id)
    return db_delete(id)


@app.route("/add", methods=["PUT"])
def add():
    body = request.json
    if body is not None:
        app.logger.info("Request to add person with body: %s", body)
        person = Person(
            0,
            body["firstName"],
            body["lastName"],
            body["age"],
            body["address"],
            body["workplace"],
        )
        return db_add(person)

    app.logger.error("Request body is empty")
    return Response(status=404)


@app.route("/health")
def health():
    health_ok = True
    health_messages = []

    start = time.time()

    try:
        app.logger.info("Application is running")
        health_messages.append("Application: Healthy")

        # memory check
        mem = psutil.virtual_memory()
        health_messages.append(f"Memory usage: {mem.percent}%")

        if health_check():
            health_messages.append("Database: Healthy")
        else:
            app.logger.error("Database health check failed")
            health_messages.append("Database: Not Healthy")
            health_ok = False

    except Exception as e:
        app.logger.error(f"Application health check failed: {e}")
        health_messages.append("Application: Not Healthy")
        health_ok = False

    end = time.time()
    response_time = round(end - start, 4)
    health_messages.append(f"Response time: {response_time} seconds")

    response = {
        "status": "ok" if health_ok else "error",
        "messages": health_messages,
    }

    return jsonify(response), 200 


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
