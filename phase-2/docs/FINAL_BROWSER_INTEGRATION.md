# Citizen Portal and OS Lab Browser Applications

The repository has two distinct browser experiences. The citizen-facing portal is the main website; the scheduling interface is a separate academic OS demonstration.

## Citizen-facing portal

From the repository root:

```bash
python3 web_app.py
```

Open `http://127.0.0.1:8000`.

The portal provides a sample service catalogue, service-specific application forms, input validation, generated application references, local JSON persistence and status lookup. It stores data in `data/citizen_applications.json`. Newly submitted applications receive the initial status **Submitted**.

Automated HTTP tests:

```bash
PYTHONPATH=. python3 -m unittest discover -s phase-2/tests -p 'test_citizen_portal.py' -v
```

Manual acceptance: open the portal, select a service, submit fictional applicant details, note the generated reference, refresh the page and use the reference in the tracking form. Verify invalid mobile/email input and an unknown reference. For the admin flow, sign in at `/admin`, update the submitted application's status and confirm the new status through citizen tracking.

## OS scheduling lab

Run separately:

```bash
python3 os_lab_app.py
```

Open `http://127.0.0.1:8001`. This teaching interface demonstrates process scheduling using synthetic service requests. It is not the citizen portal and citizens do not choose CPU scheduling algorithms when applying for services.

Automated HTTP tests:

```bash
PYTHONPATH=. python3 -m unittest discover -s phase-2/tests -p 'test_web_integration.py' -v
```

## Administrator workflow

The citizen portal has a separate local administrator dashboard at `http://127.0.0.1:8000/admin`. Set `CIVICONE_ADMIN_PASSWORD` before starting `web_app.py`. The dashboard requires a signed-in session and supports listing, searching and filtering submitted applications, viewing their details, and changing a demo application's status among `Submitted`, `Under Review`, `Approved` and `Rejected`. Status changes and a simple history are stored in the same local JSON file. The owner manually verified submission, admin status update and citizen tracking of the updated status for a synthetic application.

## Limitations

Both browser experiences are local academic prototypes bound to loopback. Neither is an official government service. CivicOne's admin login is a local demonstration mechanism, not production-grade authentication or authorization. There is no government database or identity-provider integration, payment processing, real document verification, notifications or live service fulfilment. Use fictional records only. Citizen status lookup deliberately returns no applicant contact information.

Capture screenshots from the actual browser after running the acceptance steps. Do not treat mock data or illustrative screens as evidence of a live government integration.
