from flask import Flask, render_template_string, session, redirect, request
from database import execute_query
from auth import authenticate_user
import socket
import webbrowser

app = Flask(__name__)
app.secret_key = "smart_siem_super_secret_key"


# =========================
# LOGIN ROUTE
# =========================
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # 1️⃣ Hardcoded admin login (fallback/demo)
        if username == "admin" and password == "admin123":
            session["user"] = username
            return redirect("/dashboard")

        # 2️⃣ Database authentication
        user = authenticate_user(username, password)
        if user:
            session["user"] = user["username"]
            return redirect("/dashboard")

    return """
    <html>
    <head>
        <title>Smart SIEM Login</title>
        <style>
            body{
                background:#0f172a;
                font-family:Arial;
                color:white;
                display:flex;
                justify-content:center;
                align-items:center;
                height:100vh;
            }
            .box{
                background:#1e293b;
                padding:30px;
                border-radius:8px;
                width:280px;
            }
            input{
                width:100%;
                padding:8px;
                margin:10px 0;
                border:none;
                border-radius:4px;
            }
            button{
                width:100%;
                padding:8px;
                background:#38bdf8;
                border:none;
                border-radius:4px;
                cursor:pointer;
            }
        </style>
    </head>
    <body>
        <form method="POST" class="box">
            <h3>Smart SIEM Login</h3>
            <input name="username" placeholder="Username" required>
            <input name="password" type="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
    </body>
    </html>
    """


# =========================
# DASHBOARD ROUTE
# =========================
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/")

    logs = execute_query(
        "SELECT COUNT(*) as total FROM logs", fetch=True
    )[0]["total"]

    alerts = execute_query(
        "SELECT COUNT(*) as total FROM alerts", fetch=True
    )[0]["total"]

    recent_alerts = execute_query(
        "SELECT * FROM alerts ORDER BY created_at DESC LIMIT 10",
        fetch=True
    )

    grouped = execute_query(
        "SELECT alert_type, COUNT(*) as count FROM alerts GROUP BY alert_type",
        fetch=True
    )

    labels = [g["alert_type"] for g in grouped]
    values = [g["count"] for g in grouped]

    return render_template_string("""
    <html>
    <head>
        <title>Smart SIEM Dashboard</title>
        <meta http-equiv="refresh" content="5">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body{
                font-family:Arial;
                background:#0f172a;
                color:white;
                padding:20px;
            }
            .header{
                display:flex;
                justify-content:space-between;
                align-items:center;
            }
            .title{
                font-size:22px;
                font-weight:bold;
                color:#38bdf8;
            }
            .logout{
                font-size:12px;
                padding:5px 10px;
                background:#334155;
                border-radius:4px;
                text-decoration:none;
                color:white;
            }
            .stats{
                display:flex;
                gap:15px;
                margin:20px 0;
            }
            .card{
                background:#1e293b;
                padding:15px;
                border-radius:6px;
                flex:1;
                text-align:center;
                font-size:14px;
            }
            .chart-wrapper{
                max-width:600px;
                margin:30px auto;
            }
            table{
                width:100%;
                border-collapse:collapse;
                background:#1e293b;
                font-size:13px;
                margin-top:30px;
            }
            th, td{
                padding:8px;
                text-align:left;
            }
            th{
                background:#334155;
            }
            .HIGH{
                color:orange;
                font-weight:bold;
            }
            .CRITICAL{
                color:red;
                font-weight:bold;
            }
        </style>
    </head>
    <body>

        <div class="header">
            <div class="title">Smart SIEM Dashboard</div>
            <a class="logout" href="/logout">Logout</a>
        </div>

        <div class="stats">
            <div class="card">
                Logs<br>
                <b>{{ logs }}</b>
            </div>
            <div class="card">
                Alerts<br>
                <b>{{ alerts }}</b>
            </div>
        </div>

        <div class="chart-wrapper">
            <canvas id="chart"></canvas>
        </div>

        <table>
            <tr>
                <th>ID</th>
                <th>Type</th>
                <th>User</th>
                <th>IP</th>
                <th>Severity</th>
                <th>Time</th>
            </tr>
            {% for a in recent_alerts %}
            <tr>
                <td>{{ a.id }}</td>
                <td>{{ a.alert_type }}</td>
                <td>{{ a.username }}</td>
                <td>{{ a.ip_address }}</td>
                <td class="{{ a.severity }}">{{ a.severity }}</td>
                <td>{{ a.created_at }}</td>
            </tr>
            {% endfor %}
        </table>

        <script>
            new Chart(document.getElementById('chart'), {
                type:'bar',
                data:{
                    labels: {{ labels|safe }},
                    datasets:[{
                        data: {{ values|safe }},
                        backgroundColor:['orange','red']
                    }]
                },
                options:{
                    plugins:{ legend:{ display:false } }
                }
            });
        </script>

    </body>
    </html>
    """, logs=logs, alerts=alerts,
       recent_alerts=recent_alerts,
       labels=labels, values=values)


# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# =========================
# SAFE START
# =========================
if __name__ == "__main__":

    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()

    print(f"Starting dashboard on http://127.0.0.1:{port}")
    webbrowser.open(f"http://127.0.0.1:{port}")

    app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)

