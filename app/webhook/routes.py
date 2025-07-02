from flask import Blueprint, request, jsonify, render_template
from datetime import datetime
from app.extensions import mongo


webhook = Blueprint("Webhook", __name__, url_prefix="/webhook")


@webhook.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@webhook.route("/receiver", methods=["POST"])
def receiver():
    print("Headers: ", request.headers)
    print("Payload: ", request.json)
    event = request.headers.get("X-GitHub-Event")
    payload = request.json

    data = {
        "author": "",
        "action": "",
        "from_branch": "",
        "to_branch": "",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "request_id": "",
    }

    if event == "push":
        data["action"] = "PUSH"
        data["author"] = payload["pusher"]["name"]
        data["from_branch"] = ""
        data["to_branch"] = payload["ref"].split("/")[-1]
        data["request_id"] = payload["head_commit"]["id"]

    elif event == "pull_request":
        pr = payload["pull_request"]
        data["author"] = pr["user"]["login"]
        data["from_branch"] = pr["head"]["ref"]
        data["to_branch"] = pr["base"]["ref"]
        data["request_id"] = str(pr["id"])

        if pr["merged"]:
            data["action"] = "MERGE"
        else:
            data["action"] = "PULL_REQUEST"

    else:
        return jsonify({"msg": "Unhandled event"}), 400

    mongo.db.events.insert_one(data)
    return jsonify({"msg": "Event stored"}), 200


@webhook.route("/logs", methods=["GET"])
def get_logs():
    events = list(mongo.db.events.find({}, {"_id": 0}))
    return jsonify(events), 200
