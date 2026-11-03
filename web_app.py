#!/usr/bin/env python3
"""Citizen-facing local web portal for the Integrated National Citizen Services Platform.

Run: python3 web_app.py
Open: http://127.0.0.1:8000
Academic prototype only: synthetic records, no government integration or authentication.
"""
from __future__ import annotations
import json
import re
import secrets
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "citizen_applications.json"

SERVICES = [
    {"id":"birth-certificate","name":"Birth Certificate","category":"Certificates","description":"Apply for a birth certificate or request a certified copy of an existing record.","time":"7–10 working days","documents":["Proof of birth","Parent or guardian identity proof","Address proof"],"icon":"BC"},
    {"id":"income-certificate","name":"Income Certificate","category":"Certificates","description":"Submit a request for an income certificate for education, benefits or official purposes.","time":"7–10 working days","documents":["Identity proof","Address proof","Income supporting document"],"icon":"IC"},
    {"id":"identity-update","name":"Identity Details Update","category":"Identity","description":"Request an update to basic identity or contact details in this demonstration workflow.","time":"5–7 working days","documents":["Identity proof","Supporting document for requested change"],"icon":"ID"},
    {"id":"grievance","name":"Public Grievance","category":"Grievances","description":"Register a civic-service grievance and receive a reference number for follow-up.","time":"3–5 working days for acknowledgement","documents":["Relevant service reference (if available)","Supporting evidence (optional)"],"icon":"GR"},
    {"id":"property-tax","name":"Property Tax Enquiry","category":"Tax","description":"Submit a property-tax enquiry or request a payment-status clarification.","time":"3–5 working days","documents":["Property or assessment reference","Applicant identity proof"],"icon":"TX"},
    {"id":"pension-enquiry","name":"Pension Enquiry","category":"Social Welfare","description":"Raise a pension-related enquiry for this academic service-platform prototype.","time":"5–7 working days","documents":["Pension reference (if available)","Identity proof"],"icon":"PE"},
]

PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#102b46"><title>CivicOne — Citizen Services</title>
<style>
:root{--navy:#102b46;--blue:#245d86;--teal:#0d8278;--ink:#172b3c;--muted:#657789;--line:#e4ebef;--bg:#f5f8fa;--white:#fff}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}
a{color:inherit;text-decoration:none}.wrap{width:min(1160px,calc(100% - 40px));margin:auto}
header{background:var(--navy);color:#fff}.top{height:76px;display:flex;align-items:center;justify-content:space-between}.logo{display:flex;align-items:center;gap:12px;font-weight:800;letter-spacing:.2px}.mark{width:38px;height:38px;border-radius:11px;background:#e6f4f2;color:var(--teal);display:grid;place-items:center;font-weight:900}.brand small{display:block;font-size:10px;color:#b8cad8;letter-spacing:1.5px;margin-top:3px}.nav{display:flex;gap:26px;color:#d9e5ee;font-size:13px}.nav a:hover{color:#fff}.hero{background:linear-gradient(115deg,#102b46 0%,#174c69 65%,#167e7a 130%);color:white;padding:58px 0 64px}.hero-grid{display:grid;grid-template-columns:1.4fr .6fr;align-items:center;gap:35px}.eyebrow{font-size:11px;letter-spacing:2px;text-transform:uppercase;color:#9bd5cf;font-weight:750}.hero h1{font-size:clamp(34px,5vw,54px);line-height:1.08;letter-spacing:-1.6px;margin:15px 0}.hero p{color:#d3e1e9;max-width:620px;line-height:1.7;margin:0 0 24px}.cta{display:inline-flex;background:#f3fbf9;color:#145c5b;border-radius:8px;padding:12px 17px;font-weight:750;font-size:13px}.hero-note{border:1px solid #ffffff35;background:#ffffff12;border-radius:16px;padding:23px}.hero-note strong{font-size:27px;display:block}.hero-note span{font-size:12px;color:#c8dce5;line-height:1.6}.main{padding:38px 0 70px}.section-head{display:flex;justify-content:space-between;align-items:end;gap:20px;margin:0 0 20px}.section-head h2{font-size:23px;margin:0 0 5px;letter-spacing:-.5px}.muted{color:var(--muted);font-size:13px}.services{display:grid;grid-template-columns:repeat(3,1fr);gap:15px}.service{background:#fff;border:1px solid var(--line);border-radius:13px;padding:19px;transition:.18s;box-shadow:0 4px 16px #19354a08}.service:hover{transform:translateY(-3px);box-shadow:0 12px 26px #19354a12;border-color:#bfd5df}.icon{width:40px;height:40px;border-radius:10px;background:#eaf4f4;color:#167b76;display:grid;place-items:center;font-size:11px;font-weight:850}.tag{font-size:10px;color:#167b76;font-weight:750;text-transform:uppercase;letter-spacing:1px;margin-top:17px}.service h3{font-size:16px;margin:7px 0}.service p{font-size:12px;color:var(--muted);line-height:1.6;min-height:58px}.service-foot{display:flex;justify-content:space-between;align-items:center;border-top:1px solid var(--line);padding-top:13px;font-size:11px;color:var(--muted)}.link{color:#176c78;font-weight:750;cursor:pointer;background:none;border:0;padding:0;font:inherit}.track{margin-top:38px;background:#fff;border:1px solid var(--line);border-radius:15px;padding:25px;display:grid;grid-template-columns:1fr 1fr;gap:28px;align-items:center}.track h2{margin:0 0 7px;font-size:21px}.track-form{display:flex;gap:8px}.track-form input,.field input,.field textarea,.field select{width:100%;border:1px solid #d8e2e8;border-radius:8px;padding:11px 12px;font:inherit;font-size:13px;background:#fff;color:var(--ink)}button{border:0;border-radius:8px;background:var(--teal);color:white;font-weight:750;padding:11px 16px;cursor:pointer;white-space:nowrap}.result{margin-top:12px;font-size:12px;line-height:1.6}.modal-back{position:fixed;inset:0;background:#0d2039a8;display:none;align-items:center;justify-content:center;padding:20px;z-index:5}.modal-back.open{display:flex}.modal{background:white;border-radius:16px;width:min(560px,100%);max-height:90vh;overflow:auto;padding:25px;box-shadow:0 25px 80px #071a2a55}.modal-head{display:flex;justify-content:space-between;align-items:start}.modal h2{margin:0 0 5px}.close{background:#edf2f5;color:#30485a;padding:7px 11px}.field{margin:13px 0}.field label{display:block;font-size:11px;font-weight:750;margin-bottom:6px;color:#43596a}.field textarea{min-height:88px;resize:vertical}.field small{display:block;color:var(--muted);font-size:10px;margin-top:5px}.docs{background:#f3f7f8;border-radius:9px;padding:12px 14px;font-size:12px;color:#536979;line-height:1.7}.success-box{background:#eaf7f2;border:1px solid #c8e9dc;color:#176347;border-radius:10px;padding:17px;margin-top:14px}.success-box strong{font-size:20px;display:block;margin:6px 0}.notice{font-size:11px;color:#748696;line-height:1.6;margin-top:18px}footer{background:#102b46;color:#b9cbd7;padding:25px 0;font-size:11px}.footer-row{display:flex;justify-content:space-between;gap:20px}.hidden{display:none!important}
@media(max-width:800px){.hero-grid{grid-template-columns:1fr}.hero-note{display:none}.services{grid-template-columns:repeat(2,1fr)}.track{grid-template-columns:1fr}.nav{gap:12px}}
@media(max-width:540px){.wrap{width:calc(100% - 28px)}.top{height:66px}.nav a:not(:last-child){display:none}.hero{padding:43px 0}.services{grid-template-columns:1fr}.section-head{display:block}.track-form{flex-direction:column}.footer-row{display:block}.footer-row span{display:block;margin-top:8px}}
</style></head><body>
<header><div class="wrap top"><a class="logo" href="/"><span class="mark">C</span><span class="brand">CivicOne<small>NATIONAL CITIZEN SERVICES</small></span></a><nav class="nav"><a href="#services">Services</a><a href="#track">Track application</a><a href="#about">About</a></nav></div></header>
<section class="hero"><div class="wrap hero-grid"><div><div class="eyebrow">One platform. Essential services.</div><h1>Public services,<br>made simpler.</h1><p>Explore citizen services, submit a request and keep track of your application from one place. A unified academic prototype for a more connected service experience.</p><a class="cta" href="#services">Explore services&nbsp; →</a></div><aside class="hero-note"><strong>One place to begin.</strong><span>Discover services, understand the documents you may need and get a reference number for every submitted application.</span></aside></div></section>
<main class="wrap main" id="services"><div class="section-head"><div><h2>Explore citizen services</h2><div class="muted">Choose a service to view its details and start an application.</div></div><div class="muted" id="serviceCount">Loading services…</div></div><div class="services" id="serviceGrid"></div>
<section class="track" id="track"><div><div class="eyebrow" style="color:#16827a">Application updates</div><h2>Track your application</h2><div class="muted">Enter the reference number received after submission.</div></div><div><form class="track-form" id="trackForm"><input id="reference" placeholder="e.g. CIV-2026-A1B2C3" required aria-label="Application reference"><button>Track status</button></form><div class="result" id="trackResult" aria-live="polite"></div></div></section>
<p class="notice" id="about">Academic demonstration only. This platform uses locally stored sample applications and is not connected to government databases, identity providers or payment gateways. Do not submit real personal or sensitive information.</p></main>
<footer><div class="wrap footer-row"><strong>CivicOne · Integrated National Citizen Services Platform</strong><span>Operating Systems PBL · Academic prototype · Group 66</span></div></footer>
<div class="modal-back" id="modal"><section class="modal" role="dialog" aria-modal="true" aria-labelledby="modalTitle"><div class="modal-head"><div><h2 id="modalTitle">Apply for a service</h2><div class="muted" id="modalSubtitle"></div></div><button class="close" id="closeModal" type="button">✕</button></div><div id="applyContent"><form id="applyForm"><input type="hidden" id="serviceId"><div class="docs" id="documents"></div><div class="field"><label for="applicant">Applicant name</label><input id="applicant" maxlength="70" required placeholder="Enter your name"></div><div class="field"><label for="email">Email address</label><input id="email" type="email" maxlength="120" required placeholder="name@example.com"></div><div class="field"><label for="mobile">Mobile number</label><input id="mobile" inputmode="numeric" pattern="[0-9]{10}" required placeholder="10-digit mobile number"><small>Use fictional details for this local demonstration.</small></div><div class="field"><label for="details">Application details</label><textarea id="details" maxlength="1000" required placeholder="Briefly describe your request…"></textarea></div><button type="submit">Submit application</button><div class="result" id="applyError"></div></form></div><div id="submitted" class="hidden"></div></section></div>
<script>
const $=id=>document.getElementById(id);let services=[];
function esc(v){return String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
async function request(url,options={}){const r=await fetch(url,{headers:{'Content-Type':'application/json'},...options});const d=await r.json();if(!r.ok)throw Error(d.error||'Something went wrong');return d}
function renderServices(){ $('serviceCount').textContent=services.length+' services available';$('serviceGrid').innerHTML=services.map(s=>`<article class="service"><div class="icon">${esc(s.icon)}</div><div class="tag">${esc(s.category)}</div><h3>${esc(s.name)}</h3><p>${esc(s.description)}</p><div class="service-foot"><span>Typical demo timeline: ${esc(s.time)}</span><button class="link" data-service="${esc(s.id)}">Apply →</button></div></article>`).join('');document.querySelectorAll('[data-service]').forEach(b=>b.addEventListener('click',()=>openApplication(b.dataset.service)))}
function openApplication(id){const s=services.find(x=>x.id===id);if(!s)return;$('modalTitle').textContent=s.name;$('modalSubtitle').textContent='New service application';$('serviceId').value=id;$('documents').innerHTML='<strong>Documents to prepare</strong><br>'+s.documents.map(esc).join('<br>');$('applyForm').reset();$('serviceId').value=id;$('applyContent').classList.remove('hidden');$('submitted').classList.add('hidden');$('modal').classList.add('open');$('applicant').focus()}
$('closeModal').addEventListener('click',()=>$('modal').classList.remove('open'));$('modal').addEventListener('click',e=>{if(e.target===$('modal'))$('modal').classList.remove('open')});document.addEventListener('keydown',e=>{if(e.key==='Escape')$('modal').classList.remove('open')});
$('applyForm').addEventListener('submit',async e=>{e.preventDefault();$('applyError').textContent='Submitting…';try{const d=await request('/api/applications',{method:'POST',body:JSON.stringify({service_id:$('serviceId').value,name:$('applicant').value,email:$('email').value,mobile:$('mobile').value,details:$('details').value})});$('applyContent').classList.add('hidden');$('submitted').classList.remove('hidden');$('submitted').innerHTML='<div class="success-box">Application submitted successfully.<strong>'+esc(d.application.reference)+'</strong><span>Keep this reference number to track your application. Current status: Submitted.</span></div><p class="muted">This reference is also saved in this browser for your convenience.</p><button id="done" type="button">Done</button>';$('done').addEventListener('click',()=>$('modal').classList.remove('open'));localStorage.setItem('civicone-last-reference',d.application.reference)}catch(err){$('applyError').textContent=err.message}});
$('trackForm').addEventListener('submit',async e=>{e.preventDefault();$('trackResult').textContent='Looking up application…';try{const d=await request('/api/applications/'+encodeURIComponent($('reference').value.trim()));$('trackResult').innerHTML='<div class="success-box"><b>'+esc(d.application.service)+'</b><br>Reference: '+esc(d.application.reference)+'<br>Status: <b>'+esc(d.application.status)+'</b><br>Submitted: '+esc(d.application.submitted_at)+'</div>'}catch(err){$('trackResult').textContent=err.message}});
const saved=localStorage.getItem('civicone-last-reference');if(saved)$('reference').value=saved;
request('/api/services').then(d=>{services=d.services;renderServices()}).catch(e=>$('serviceGrid').textContent=e.message);
</script></body></html>"""

def read_store():
    if not DATA_FILE.exists():
        return []
    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError("Application store is not a list")
        return data
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Unable to read application store: {exc}") from exc

def write_store(items):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    temp = DATA_FILE.with_suffix(".tmp")
    temp.write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding="utf-8")
    temp.replace(DATA_FILE)

def clean_text(value, label, limit):
    if not isinstance(value, str):
        raise ValueError(f"{label} is required")
    value = value.strip()
    if not value or len(value) > limit:
        raise ValueError(f"{label} must be between 1 and {limit} characters")
    return value

class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/":
            body = PAGE.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(body)
            return
        if path == "/api/services":
            return self.send_json(200, {"services": SERVICES})
        match = re.fullmatch(r"/api/applications/([A-Za-z0-9-]{6,40})", path)
        if match:
            try:
                app = next((x for x in read_store() if x["reference"].lower() == match.group(1).lower()), None)
            except ValueError as exc:
                return self.send_json(500, {"error": str(exc)})
            if not app:
                return self.send_json(404, {"error": "No application found for that reference number."})
            return self.send_json(200, {"application": {k: app[k] for k in ("reference", "service", "status", "submitted_at")}})
        return self.send_json(404, {"error": "Not found"})

    def do_POST(self):
        if urlparse(self.path).path != "/api/applications":
            return self.send_json(404, {"error": "Not found"})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 1 or length > 8192:
                raise ValueError("Invalid request size")
            data = json.loads(self.rfile.read(length).decode("utf-8"))
            if not isinstance(data, dict):
                raise ValueError("Request must be a JSON object")
            service = next((s for s in SERVICES if s["id"] == data.get("service_id")), None)
            if not service:
                raise ValueError("Select a valid service")
            name = clean_text(data.get("name"), "Applicant name", 70)
            email = clean_text(data.get("email"), "Email", 120)
            mobile = clean_text(data.get("mobile"), "Mobile number", 10)
            details = clean_text(data.get("details"), "Application details", 1000)
            if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
                raise ValueError("Enter a valid email address")
            if not re.fullmatch(r"[0-9]{10}", mobile):
                raise ValueError("Mobile number must contain exactly 10 digits")
            items = read_store()
            reference = "CIV-2026-" + secrets.token_hex(3).upper()
            app = {"reference": reference, "service_id": service["id"], "service": service["name"], "name": name, "email": email, "mobile": mobile, "details": details, "status": "Submitted", "submitted_at": datetime.now(timezone.utc).astimezone().strftime("%d %b %Y, %I:%M %p")}
            items.append(app)
            write_store(items)
            return self.send_json(201, {"application": {"reference": reference, "service": service["name"], "status": app["status"], "submitted_at": app["submitted_at"]}})
        except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            return self.send_json(400, {"error": str(exc)})

    def log_message(self, fmt, *args):
        print("[portal] %s %s" % (self.address_string(), fmt % args))

def create_server(host="127.0.0.1", port=8000):
    return ThreadingHTTPServer((host, port), Handler)

if __name__ == "__main__":
    server = create_server()
    print("CivicOne citizen services portal")
    print("Open http://127.0.0.1:8000 (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down…")
    finally:
        server.server_close()
