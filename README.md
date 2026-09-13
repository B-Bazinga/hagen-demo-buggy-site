# QuickNotes (demo site)

A tiny Flask notes app used as the "buggy" target for a Hagen self-healing
incident-response demo.

## Run

```
pip install -r requirements.txt
python app.py
```

Serves on port 3000. `/health` returns 200 when healthy.

## The bug

`/admin/restart` is meant to let an operator restart the service with a
secret token: `/admin/restart?token=<ADMIN_TOKEN>`. A logic bug in the
auth check also treats a *missing* token as authorized, so simply visiting
`/admin/restart` with no token crashes the process.
