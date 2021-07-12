### Loads the environment configuration into the Windows environment
$json = "environment.json"
$settings = Get-Content -Raw -Path $json | ConvertFrom-Json

$env:FLASK_APP=$settings.FLASK_APP
$env:SECRET=$settings.SECRET
$env:DATABASE_URI=$settings.DATABASE_URI