Questo script è un punto di partenza per esportare dashboard Databricks come HTML e pubblicarli su GitHub Pages.

Istruzioni:
1) Aggiungi i seguenti secrets al repository (Settings -> Secrets -> Actions):
   - DATABRICKS_DASHBOARD_URLS : una lista di URL separati da virgola dei dashboard Databricks da esportare (es. https://<workspace>#/sql/dashboards/123)
   - DATABRICKS_TOKEN : il tuo Personal Access Token Databricks
   - (opzionale) DATABRICKS_HOST : host del workspace, se serve

2) Verifica che gli URL forniti restituiscano HTML quando richiesti con il token (alcune configurazioni Databricks potrebbero richiedere altre modalità di autenticazione o non permettere l'export diretto).

3) Modifica `.github/scripts/export_dashboards.py` per usare l'API di Databricks corretta se necessario (il codice attuale fa una GET sull'URL fornito).

4) Il workflow `.github/workflows/databricks-export.yml` esegue lo script e pubblica la directory `./docs` su GitHub Pages automaticamente ogni ora (cron) e manualmente (workflow_dispatch).
