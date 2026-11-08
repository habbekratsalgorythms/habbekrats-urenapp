# Windows-only, non-admin, read-only GPU and ComfyUI diagnostics for Klyptiq.
# NO INSTALLS; NO downloaded models; NO network beyond a localhost request.
# NOTHING is transmitted automatically to GitHub or ChatGPT.
$ErrorActionPreference = "Stop"
Write-Host "KLYPTIQ VIDEO GPU CHECK — nothing will be installed" -ForegroundColor Cyan
$gpuName="";$memory="";$driver="";$gpuOk=$false
try {
  $gpuRaw = (& nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader 2>$null | Select-Object -First 1).Trim()
  $gpuParts = $gpuRaw.Split(",")
  if ($gpuParts.Count -ge 3) {
    $gpuName=$gpuParts[0].Trim()
    $memory=$gpuParts[1].Trim()
    $driver=$gpuParts[2].Trim()
    if ($memory -match '(\d+)') { $gpuOk=[int]$Matches[1] -ge 7600 }
  }
} catch {
  Write-Warning "nvidia-smi missing or inaccessible; NVIDIA driver/GPU must be checked locally."
}
$disk = Get-PSDrive -Name C -ErrorAction SilentlyContinue
$freeGib = if ($disk) {[math]::Round($disk.Free/1GB,1)} else {$null}
$comfyOk=$false
try {
  $answer=Invoke-RestMethod -Uri "http://127.0.0.1:8188/system_stats" -Method Get -TimeoutSec 2 -ErrorAction Stop
  $comfyOk=($null -ne $answer)
} catch {}
$report=[ordered]@{
  captured_date_utc=(Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
  operating_system="Windows"
  graphics_card=$gpuName
  graphics_memory=$memory
  driver_version=$driver
  disk_C_free_gib=$freeGib
  comfyui_local_available=$comfyOk
  nvidia_8gb_class=$gpuOk
  wan_inference_executed=$false
  remote_computer_access_enabled=$false
  notes="Read-only diagnostic; no files or personal data shared automatically"
}
Write-Host ("Graphics: {0} | VRAM: {1} | driver: {2}" -f $gpuName,$memory,$driver)
Write-Host ("Free C: space: {0} GiB | local ComfyUI running: {1}" -f $freeGib,$comfyOk)
Write-Host ("8GB-class NVIDIA detected: {0}" -f $gpuOk)
if (-not $gpuOk) { Write-Warning "GPU cannot be confirmed as 8 GB class. Stop model download until checked." }
if ($null -ne $freeGib -and $freeGib -lt 30) { Write-Warning "Less than 30 GiB free on C:. Choose another model storage drive or free up space." }
Write-Host "No installation, firewall, account or port setting was changed." -ForegroundColor Green
$report | ConvertTo-Json -Depth 3
