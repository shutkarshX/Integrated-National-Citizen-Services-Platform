#!/usr/bin/env python3
"""Local browser interface integrating the Phase 1 service scheduler.

Run from the repository root:
  python3 web_app.py
Then open http://127.0.0.1:8001. Uses only the Python standard library.
This is a local academic prototype with synthetic records, not a public service.
"""
from __future__ import annotations
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
import sys

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "web_requests.json"
PHASE1_SRC = ROOT / "phase-1" / "src"
if str(PHASE1_SRC) not in sys.path:
    sys.path.insert(0, str(PHASE1_SRC))

# Phase 2 tests may already have imported citizen_os as a namespace package.
# Add the Phase 1 package directory explicitly in that case; fresh processes
# also discover Phase 2 modules through the extended Phase 1 package path.
import citizen_os
PHASE1_PACKAGE = str(PHASE1_SRC / "citizen_os")
if PHASE1_PACKAGE not in citizen_os.__path__:
    citizen_os.__path__.append(PHASE1_PACKAGE)

from citizen_os.models import ServiceProcess
from citizen_os.scheduler import fcfs, sjf, priority, round_robin

ALGORITHMS = {"fcfs": fcfs, "sjf": sjf, "priority": priority, "rr": round_robin}

INDEX = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Citizen Services | Operations Console</title>
<style>
:root{--ink:#182536;--muted:#64748b;--line:#e4eaf1;--paper:#f5f7fb;--blue:#2457a7;--navy:#12233d;--green:#16845b}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px Inter,system-ui,Arial,sans-serif}
.top{background:var(--navy);color:white;padding:22px max(5vw,24px);display:flex;justify-content:space-between;align-items:center;gap:18px}
.brand{font-weight:750;letter-spacing:.2px;font-size:18px}.sub{color:#c3d0e2;font-size:12px;margin-top:5px}.badge{border:1px solid #526780;border-radius:30px;padding:7px 12px;font-size:11px;color:#d9e5f3}
main{max-width:1120px;margin:30px auto;padding:0 22px}.intro{display:flex;justify-content:space-between;align-items:end;gap:16px;margin-bottom:22px}h1{font-size:28px;margin:0 0 6px}.muted{color:var(--muted)}
.grid{display:grid;grid-template-columns:340px 1fr;gap:20px}.card{background:white;border:1px solid var(--line);border-radius:15px;padding:20px;box-shadow:0 5px 18px #172b4d08}
h2{font-size:16px;margin:0 0 16px}.field{margin:12px 0}label{display:block;font-size:12px;font-weight:650;color:#42536a;margin-bottom:6px}
input,select{width:100%;border:1px solid #d8e0ea;border-radius:8px;padding:10px 11px;font:inherit;background:white;color:var(--ink)}
button{border:0;border-radius:8px;padding:10px 14px;background:var(--blue);color:white;font-weight:650;cursor:pointer}button.secondary{background:#eaf0f8;color:#25436b}button:disabled{opacity:.5;cursor:not-allowed}
.row{display:flex;gap:9px;align-items:center;flex-wrap:wrap}.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:14px}.stat{background:#f7f9fc;border:1px solid var(--line);border-radius:10px;padding:12px}.stat b{display:block;font-size:22px}.stat span{font-size:11px;color:var(--muted)}
table{width:100%;border-collapse:collapse;font-size:13px}th,td{text-align:left;padding:11px 8px;border-bottom:1px solid var(--line)}th{color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.4px}
.pill{display:inline-block;padding:4px 8px;border-radius:20px;background:#e8f5ef;color:#16714e;font-size:11px;font-weight:700}.empty{text-align:center;color:var(--muted);padding:28px}
.timeline{display:flex;gap:4px;flex-wrap:wrap;margin-top:12px}.segment{background:#e8effa;border:1px solid #cbd9ed;border-radius:7px;padding:8px 10px;font-size:12px}.notice{margin-top:14px;padding:11px;border-radius:9px;background:#f0f5fb;color:#53657d;font-size:12px}
.error{color:#b42318;font-size:12px;margin-top:8px}.success{color:var(--green);font-size:12px;margin-top:8px}.footer{margin:22px 0;color:#8290a3;font-size:11px;text-align:center}
@media(max-width:800px){.grid{grid-template-columns:1fr}.intro{display:block}.stats{grid-template-columns:repeat(3,1fr)}}@media(max-width:480px){.stats{grid-template-columns:1fr 1fr}.top{align-items:flex-start;flex-direction:column}}
</style></head><body>
<header class="top"><div><div class="brand">CIVIC / OPERATIONS</div><div class="sub">Integrated National Citizen Services Platform · Academic prototype</div></div><div class="badge">LOCAL DEMO · SYNTHETIC DATA</div></header>
<main><div class="intro"><div><h1>Service operations</h1><div class="muted">Register sample service requests and simulate their CPU scheduling.</div></div><div class="muted" id="clock"></div></div>
<div class="grid"><section class="card"><h2>New service request</h2><form id="requestForm">
<div class="field"><label for="citizen">Citizen name</label><input id="citizen" required maxlength="60" placeholder="e.g. Asha Verma"></div>
<div class="field"><label for="service">Service category</label><select id="service"><option>Certificate services</option><option>Identity services</option><option>Grievance redressal</option><option>Tax services</option></select></div>
<div class="field"><label for="burst">Estimated CPU burst (units)</label><input id="burst" type="number" min="1" max="1000" value="4" required></div>
<div class="field"><label for="arrival">Arrival time</label><input id="arrival" type="number" min="0" max="10000" value="0" required></div>
<div class="field"><label for="priority">Priority (1 = highest)</label><input id="priority" type="number" min="1" max="10" value="2" required></div>
<button type="submit">Add request</button><div id="formMessage" aria-live="polite"></div></form>
<div class="notice">Requests are stored locally in a JSON file. Use fictional names only; this prototype has no authentication or external-service connection.</div></section>
<section><div class="card"><div class="row" style="justify-content:space-between"><h2>Request queue</h2><div class="row"><select id="algorithm" aria-label="Scheduling algorithm"><option value="fcfs">FCFS</option><option value="sjf">SJF (non-preemptive)</option><option value="priority">Priority (non-preemptive)</option><option value="rr">Round Robin</option></select><button id="runSchedule">Run schedule</button></div></div>
<div class="stats"><div class="stat"><b id="total">0</b><span>Total requests</span></div><div class="stat"><b id="avgWait">—</b><span>Average waiting</span></div><div class="stat"><b id="avgTurn">—</b><span>Average turnaround</span></div></div>
<div style="overflow-x:auto"><table><thead><tr><th>PID</th><th>Citizen</th><th>Service</th><th>Burst</th><th>Arrival</th><th>State</th></tr></thead><tbody id="requests"></tbody></table></div><div id="empty" class="empty">No requests yet. Add a synthetic request to begin.</div>
<div id="scheduleResult" hidden><h2 style="margin-top:20px">Schedule result</h2><div id="algorithmName" class="muted"></div><div class="timeline" id="timeline"></div><div style="overflow-x:auto;margin-top:12px"><table><thead><tr><th>PID</th><th>Start</th><th>Finish</th><th>Waiting</th><th>Turnaround</th></tr></thead><tbody id="scheduled"></tbody></table></div></div>
<div id="scheduleMessage" aria-live="polite"></div></div></section></div>
<div class="footer">Operating Systems PBL · Modules 1–4 teaching prototype · No real government records or services</div></main>
<script>
const $=id=>document.getElementById(id);
async function api(url,opts={}){const r=await fetch(url,{headers:{"Content-Type":"application/json"},...opts});const d=await r.json();if(!r.ok)throw Error(d.error||"Request failed");return d}
function esc(s){return String(s).replace(/[&<>"\x27]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","\x27":"&#39;"}[c]))}
async function load(){const d=await api("/api/requests");$("total").textContent=d.requests.length;$("requests").innerHTML=d.requests.map(x=>`<tr><td>${x.pid}</td><td>${esc(x.citizen)}</td><td>${esc(x.service)}</td><td>${x.burst}</td><td>${x.arrival}</td><td><span class="pill">READY</span></td></tr>`).join("");$("empty").hidden=d.requests.length>0}
$("requestForm").addEventListener("submit",async e=>{e.preventDefault();$("formMessage").textContent="";try{const d=await api("/api/requests",{method:"POST",body:JSON.stringify({citizen:$("citizen").value,service:$("service").value,burst:Number($("burst").value),arrival:Number($("arrival").value),priority:Number($("priority").value)})});$("formMessage").className="success";$("formMessage").textContent=`Request PID ${d.request.pid} saved.`;$("citizen").value="";await load()}catch(err){$("formMessage").className="error";$("formMessage").textContent=err.message}});
$("runSchedule").addEventListener("click",async()=>{try{const d=await api("/api/schedule",{method:"POST",body:JSON.stringify({algorithm:$("algorithm").value})});$("avgWait").textContent=d.average_waiting.toFixed(2);$("avgTurn").textContent=d.average_turnaround.toFixed(2);$("algorithmName").textContent=d.algorithm;$("timeline").innerHTML=d.timeline.map(x=>`<span class="segment">P${x.pid} · ${x.start}–${x.finish}</span>`).join("");$("scheduled").innerHTML=d.processes.map(x=>`<tr><td>${x.pid}</td><td>${x.start}</td><td>${x.finish}</td><td>${x.waiting}</td><td>${x.turnaround}</td></tr>`).join("");$("scheduleResult").hidden=false;$("scheduleMessage").className="success";$("scheduleMessage").textContent="Schedule simulation completed."}catch(err){$("scheduleMessage").className="error";$("scheduleMessage").textContent=err.message}});
$("clock").textContent=new Date().toLocaleString();load().catch(e=>$("scheduleMessage").textContent=e.message);
</script></body></html>"""

def load_requests():
    if not DATA_FILE.exists():
        return []
    try:
        payload = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        if not isinstance(payload, list):
            raise ValueError("Stored request data must be a JSON list")
        return payload
    except (json.JSONDecodeError, OSError) as exc:
        raise ValueError(f"Cannot read request store: {exc}") from exc

def save_requests(requests):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    temporary = DATA_FILE.with_suffix(".tmp")
    temporary.write_text(json.dumps(requests, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(DATA_FILE)

class Handler(BaseHTTPRequestHandler):
    def _send(self, status, payload, content_type="application/json; charset=utf-8"):
        body = payload.encode("utf-8") if isinstance(payload, str) else json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/":
            return self._send(200, INDEX, "text/html; charset=utf-8")
        if path == "/api/requests":
            try:
                return self._send(200, {"requests": load_requests()})
            except ValueError as exc:
                return self._send(500, {"error": str(exc)})
        return self._send(404, {"error": "Not found"})

    def do_POST(self):
        path = urlparse(self.path).path
        if path not in {"/api/requests", "/api/schedule"}:
            return self._send(404, {"error": "Not found"})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 1 or length > 16_384:
                raise ValueError("Request body must be between 1 and 16384 bytes")
            data = json.loads(self.rfile.read(length).decode("utf-8"))
            if not isinstance(data, dict):
                raise ValueError("JSON body must be an object")
            if path == "/api/requests":
                return self._add_request(data)
            return self._schedule(data)
        except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            return self._send(400, {"error": str(exc)})

    def _add_request(self, data):
        citizen = str(data.get("citizen", "")).strip()
        service = str(data.get("service", "")).strip()
        if not citizen or len(citizen) > 60:
            raise ValueError("Citizen name is required and must be at most 60 characters")
        allowed = {"Certificate services", "Identity services", "Grievance redressal", "Tax services"}
        if service not in allowed:
            raise ValueError("Choose a supported service category")
        burst, arrival, prio = data.get("burst"), data.get("arrival"), data.get("priority", 1)
        if any(isinstance(v, bool) or not isinstance(v, int) for v in (burst, arrival, prio)):
            raise ValueError("Burst, arrival and priority must be integers")
        if not 1 <= burst <= 1000 or not 0 <= arrival <= 10000 or not 1 <= prio <= 10:
            raise ValueError("Burst must be 1–1000, arrival 0–10000 and priority 1–10")
        requests = load_requests()
        pid = max((int(x["pid"]) for x in requests), default=100) + 1
        item = {"pid": pid, "citizen": citizen, "service": service, "burst": burst, "arrival": arrival, "priority": prio}
        requests.append(item)
        save_requests(requests)
        return self._send(201, {"request": item})

    def _schedule(self, data):
        algorithm = data.get("algorithm", "fcfs")
        if algorithm not in ALGORITHMS:
            raise ValueError("Algorithm must be fcfs, sjf, priority or rr")
        requests = load_requests()
        if not requests:
            raise ValueError("Add at least one service request before scheduling")
        processes = [ServiceProcess(x["pid"], x["citizen"], x["service"], x["burst"], x["arrival"], x["priority"]) for x in requests]
        result = ALGORITHMS[algorithm](processes)
        timeline = [{"pid": pid, "start": start, "finish": finish} for pid, start, finish in result.timeline]
        rows = [{"pid": p.pid, "citizen": p.citizen_name, "service": p.service_name, "start": p.start_time, "finish": p.completion_time, "waiting": p.waiting_time, "turnaround": p.turnaround_time} for p in result.processes]
        return self._send(200, {"algorithm": result.algorithm, "average_waiting": result.average_waiting_time, "average_turnaround": result.average_turnaround_time, "timeline": timeline, "processes": rows})

    def log_message(self, fmt, *args):
        print(f"[web] {self.address_string()} {fmt % args}")

def create_server(host="127.0.0.1", port=8001):
    return ThreadingHTTPServer((host, port), Handler)

if __name__ == "__main__":
    server = create_server()
    print("Integrated National Citizen Services Platform")
    print("Open http://127.0.0.1:8000 in your browser (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        server.server_close()