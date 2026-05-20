def execute_publish_job_preview(job: dict, registry=None) -> dict:
    channel = job.get("channel")
    payload = job.get("payload", {})

    if not channel:
        return {
            "ok": False,
            "status": "failed_preview",
            "error": "missing_channel"
        }

    if not payload:
        return {
            "ok": False,
            "status": "failed_preview",
            "error": "missing_payload"
        }

    if registry:
        adapter = registry.get(channel)
        if adapter and hasattr(adapter, "execute_publish_preview"):
            return adapter.execute_publish_preview(job)

    return {
        "ok": False,
        "status": "failed_preview",
        "channel": channel,
        "message": f"{channel} API adapter not connected yet"
    }


def execute_publish_job_live(job: dict, registry=None) -> dict:
    channel = job.get("channel")
    payload = job.get("payload", {})

    if not channel:
        return {
            "ok": False,
            "status": "failed_live",
            "error": "missing_channel"
        }

    if not payload:
        return {
            "ok": False,
            "status": "failed_live",
            "error": "missing_payload"
        }

    if not registry:
        return {
            "ok": False,
            "status": "failed_live",
            "channel": channel,
            "message": "missing_registry"
        }

    adapter = registry.get(channel)

    if not adapter:
        return {
            "ok": False,
            "status": "failed_live",
            "channel": channel,
            "message": f"{channel} adapter not registered"
        }

    status = adapter.status()

    if not status.get("enabled"):
        return {
            "ok": False,
            "status": "blocked_live",
            "channel": channel,
            "message": f"{channel} adapter not ready for live",
            "adapter_status": status
        }

    result = adapter.publish(payload)

    if result.get("ok"):
        return {
            **result,
            "status": "created_live_draft",
            "channel": channel
        }

    return {
        **result,
        "status": "failed_live",
        "channel": channel
    }

