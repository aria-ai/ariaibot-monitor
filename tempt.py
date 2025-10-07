#!/usr/bin/env python3
import http.server
import socketserver
import threading
import time
import urllib.request
import urllib.error
from datetime import datetime
import json


class HealthMonitor:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.health_history = []
        self.current_status = "Unknown"
        self.last_check = None
        self.monitoring = False

    def check_health(self):
        """Check the health of the target API"""
        try:
            with urllib.request.urlopen(self.url, timeout=10) as response:
                status_code = response.getcode()
                if status_code == 200:
                    status = "UP"
                    self.current_status = "UP"
                else:
                    status = "DOWN"
                    self.current_status = "DOWN"

        except urllib.error.URLError as e:
            status = "DOWN"
            self.current_status = "DOWN"
        except Exception as e:
            status = "DOWN"
            self.current_status = "DOWN"

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_check = timestamp

        # Store in history (keep last 100 records)
        self.health_history.append({"timestamp": timestamp, "status": status})

        if len(self.health_history) > 100:
            self.health_history.pop(0)

        print(f"[{timestamp}] {self.name} Health check: {status}")

    def start_monitoring(self):
        """Start the background monitoring thread"""
        if not self.monitoring:
            self.monitoring = True
            monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            monitor_thread.start()
            print(f"{self.name} health monitoring started")

    def _monitor_loop(self):
        """Background loop to check health every minute"""
        while self.monitoring:
            self.check_health()
            time.sleep(60)  # Wait 60 seconds

    def get_html_page(self):
        """Generate HTML page showing health status"""
        # Determine status color
        status_color = (
            "#28a745"
            if self.current_status == "UP"
            else "#dc3545" if self.current_status == "DOWN" else "#6c757d"
        )

        # Generate table rows
        table_rows = ""
        for record in reversed(self.health_history):  # Show newest first
            row_color = "#d4edda" if record["status"] == "UP" else "#f8d7da"
            table_rows += f"""
                <tr style="background-color: {row_color};">
                    <td>{record['timestamp']}</td>
                    <td><strong>{record['status']}</strong></td>
                </tr>
            """

        if not table_rows:
            table_rows = "<tr><td colspan='2'>No health checks performed yet</td></tr>"

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{self.name} Health Monitor</title>
            <meta http-equiv="refresh" content="30">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f8f9fa; }}
                .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .status-card {{ 
                    background-color: {status_color}; 
                    color: white; 
                    padding: 20px; 
                    border-radius: 5px; 
                    margin-bottom: 20px; 
                    text-align: center; 
                }}
                .status-card h1 {{ margin: 0; }}
                .status-card p {{ margin: 10px 0 0 0; opacity: 0.9; }}
                .refresh-btn {{ 
                    background-color: #007bff; 
                    color: white; 
                    border: none; 
                    padding: 10px 20px; 
                    border-radius: 5px; 
                    cursor: pointer; 
                    font-size: 16px; 
                    margin: 10px 0; 
                }}
                .refresh-btn:hover {{ background-color: #0056b3; }}
                .refresh-btn:disabled {{ background-color: #6c757d; cursor: not-allowed; }}
                .loading {{ display: none; color: #007bff; font-weight: bold; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th {{ background-color: #343a40; color: white; padding: 12px; text-align: left; }}
                td {{ padding: 12px; border-bottom: 1px solid #dee2e6; }}
                .info {{ color: #6c757d; font-size: 0.9em; margin-top: 20px; }}
            </style>
            <script>
                function triggerHealthCheck() {{
                    const button = document.getElementById('refreshBtn');
                    const loading = document.getElementById('loading');
                    
                    button.disabled = true;
                    button.textContent = 'Checking...';
                    loading.style.display = 'block';
                    
                    fetch(window.location.pathname + '/trigger', {{
                        method: 'POST',
                        headers: {{
                            'Content-Type': 'application/json',
                        }},
                    }})
                    .then(response => {{
                        if (response.ok) {{
                            setTimeout(() => {{
                                window.location.reload();
                            }}, 2000);
                        }} else {{
                            button.disabled = false;
                            button.textContent = 'Manual Health Check';
                            loading.style.display = 'none';
                            alert('Failed to trigger health check');
                        }}
                    }})
                    .catch(error => {{
                        button.disabled = false;
                        button.textContent = 'Manual Health Check';
                        loading.style.display = 'none';
                        alert('Error: ' + error.message);
                    }});
                }}
            </script>
        </head>
        <body>
            <div class="container">
                <div class="status-card">
                    <h1>{self.name} Status: {self.current_status}</h1>
                    <p>Last checked: {self.last_check or 'Never'}</p>
                    <button id="refreshBtn" class="refresh-btn" onclick="triggerHealthCheck()">Manual Health Check</button>
                    <div id="loading" class="loading">Performing health check...</div>
                </div>
                
                <h2>Health Check History</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Timestamp</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>
                
                <div class="info">
                    <p><strong>Monitoring:</strong> {self.url}</p>
                    <p><strong>Check Interval:</strong> Every 60 seconds</p>
                    <p><strong>Auto-refresh:</strong> This page refreshes every 30 seconds</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html


# Global monitors dictionary
monitors = {}


class HealthRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Root path - show list of monitors
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            
            links = "".join([
                f'<li><a href="/{path}">{monitor.name}</a> - <span style="color: {"green" if monitor.current_status == "UP" else "red"}">{monitor.current_status}</span></li>'
                for path, monitor in monitors.items()
            ])
            
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Health Monitor Dashboard</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f8f9fa; }}
                    .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                    h1 {{ color: #343a40; }}
                    ul {{ list-style: none; padding: 0; }}
                    li {{ padding: 15px; margin: 10px 0; background: #f8f9fa; border-radius: 5px; }}
                    a {{ text-decoration: none; color: #007bff; font-weight: bold; font-size: 18px; }}
                    a:hover {{ text-decoration: underline; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Health Monitor Dashboard</h1>
                    <ul>{links}</ul>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode("utf-8"))
            return
        
        # Check if path matches a monitor
        path_parts = self.path.strip('/').split('/')
        monitor_path = path_parts[0]
        
        if monitor_path in monitors:
            monitor = monitors[monitor_path]
            
            # Handle subpaths
            if len(path_parts) == 1:
                # Main monitor page
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                html_content = monitor.get_html_page()
                self.wfile.write(html_content.encode("utf-8"))
            elif len(path_parts) == 2 and path_parts[1] == "api":
                # JSON API endpoint
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                data = {
                    "name": monitor.name,
                    "current_status": monitor.current_status,
                    "last_check": monitor.last_check,
                    "history_count": len(monitor.health_history),
                }
                self.wfile.write(json.dumps(data).encode("utf-8"))
            else:
                self.send_error(404)
        else:
            self.send_error(404)

    def do_POST(self):
        path_parts = self.path.strip('/').split('/')
        
        if len(path_parts) == 2 and path_parts[1] == "trigger":
            monitor_path = path_parts[0]
            
            if monitor_path in monitors:
                monitor = monitors[monitor_path]
                try:
                    monitor.check_health()
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    response_data = {
                        "status": "success",
                        "message": "Health check completed",
                        "current_status": monitor.current_status,
                        "last_check": monitor.last_check,
                    }
                    self.wfile.write(json.dumps(response_data).encode("utf-8"))
                except Exception as e:
                    self.send_response(500)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    error_data = {
                        "status": "error",
                        "message": f"Health check failed: {str(e)}",
                    }
                    self.wfile.write(json.dumps(error_data).encode("utf-8"))
            else:
                self.send_error(404)
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        # Suppress default request logging
        pass


def main():
    global monitors
    
    # Configure monitors here
    monitors = {
        "ariaibot": HealthMonitor(
            "AriaAI Bot",
            "https://ariaibot-2693c651aa05.herokuapp.com/health"
        ),
        "traderforum": HealthMonitor(
            "Trader Forum",
            "https://traders-forum-backend.onrender.com/health/zz"
        ),
    }
    
    # Start all monitors
    for monitor in monitors.values():
        monitor.start_monitoring()

    # Start web server
    import os
    PORT = int(os.environ.get("PORT", 8000))

    with socketserver.TCPServer(("", PORT), HealthRequestHandler) as httpd:
        try:
            print(f"Health Monitor Server running on port {PORT}")
            print(f"Local access: http://localhost:{PORT}")
            print(f"Available monitors:")
            for path, monitor in monitors.items():
                print(f"  - /{path} ({monitor.name})")
            print("Press Ctrl+C to stop")
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down...")
            for monitor in monitors.values():
                monitor.monitoring = False
            httpd.shutdown()
            httpd.server_close()


if __name__ == "__main__":
    main()
