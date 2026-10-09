# Deploying

## A. Demo (Streamlit Community Cloud) - synthetic data only
Push to GitHub; the app redeploys. This is a shared public host and its disk resets, so the audit trail and run
history will not survive restarts. Never load real client data here.

## B. Real client data: your own container in an India region
1. Create a small VM (AWS Mumbai `ap-south-1` or Azure Central India) or a container service.
2. `git clone` the repo, copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and fill it in.
3. `docker compose up -d` (data persists in the `archenex-data` volume; back it up).
4. Put it behind HTTPS (Caddy, nginx or the cloud load balancer) and restrict access to the client's network/VPN.
5. Create users with `python scripts/make_user_hash.py`.

## C. Scheduled monitoring
```
0 8 * * 1-5  cd /opt/archenex && docker compose run --rm archenex \
  python -m archenex.cli monitor --config connections.json --client "Client name" --send
```
Set `ARCHENEX_WEBHOOK` to a Slack/Teams incoming-webhook URL. Without `--send` it only prints (dry-run).
A disabled GitHub Actions example is in `.github/workflows/monitor.yml.disabled`; use it only for demos, as the
database does not persist between runs.
