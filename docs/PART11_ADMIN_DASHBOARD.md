# Part 11 — Admin Dashboard

Adds a safe-by-default admin dashboard layer.

## Endpoints

- `GET /dashboard` — static HTML operations console
- `GET /dashboard/status` — module and autonomy status
- `GET /dashboard/metrics` — current operational metrics
- `PUT /dashboard/controls` — update autonomy controls

## Safety Rules

- Autonomous execution is disabled by default.
- Dry-run mode is enabled by default.
- Emergency stop always forces autonomy off.

This module is designed to connect to persistent storage in the final integration build.
