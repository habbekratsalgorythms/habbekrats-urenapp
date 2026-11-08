# Read-only Windows GPU and locally installed ComfyUI diagnostics.
# Does not install models, download files, open ports, or transmit data.
$ErrorActionPreference = "Stop"
Write-Host "KLYPTIQ LOCAL VIDEO CHECK — read-only" -ForegroundColor Cyan
$gpuName=""; $memory=""; $driver=""; $gpuOk=$false
try {
  $gpuRaw = (& nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader 2>$null | Select-Object -First 1).Trim()
  $parts = $gpuRaw.Split(",")
  if ($parts.Count -ge 3) {
    $gpuName=$parts[0].Trim()
    $memory=$parts[1].Trim()
    $driver=$parts[2].Trim()
    if ($memory -match '(\d+)') { $gpuOk=[int]$Matches[1] -ge 7600 }
  }
} catch {
  Write-Warning "Cannot read NVIDIA GPU data. Verify ComfyUI is using NVIDIA CUDA."
}
# D: is the requested model/output storage; C: can still hold application caches.
$storage = [ordered]@{}
foreach ($letter in @("D","C")) {
  $disk = Get-PSDrive -Name $letter -ErrorAction SilentlyContinue
  $storage[$letter] = if ($disk) {[math]::Round($disk.Free/1GB,1)} else {$null}
}
# Desktop commonly uses 8000, portable 8188; Desktop may choose another port
# if occupied. Probe these known loopback addresses ONLY; no network exposure.
$foundPort=$null
$comfyDevice=$null
foreach ($port in @(8000,8188,8189,8190)) {
  try {
    $answer=Invoke-RestMethod -Uri ("http://127.0.0.1:{0}/system_stats" -f $port) -Method Get -TimeoutSec 2 -ErrorAction Stop
    if ($answer -and $answer.system) {
      $foundPort=$port
      $comfyDevice=@($answer.devices | ForEach-Object { $_.name }) -join "; "
      break
    }
  } catch {}
}
$report=[ordered]@{
  graphics_card=$gpuName
  graphics_memory=$memory
  driver_version=$driver
  disk_free_gib=$storage
  comfyui_local_available=($null -ne $foundPort)
  comfyui_local_port=$foundPort
  comfyui_device=$comfyDevice
  gpu_8gb_class=$gpuOk
  wan_inference_executed=$false
  remote_access_enabled=$false
  data_transmitted_externally=$false
}
Write-Host ("GPU: {0} / {1} / driver {2}" -f $gpuName,$memory,$driver)
Write-Host ("Free space: D: {0} GiB, C: {1} GiB" -f $storage["D"],$storage["C"])
if ($foundPort) {
  Write-Host ("ComfyUI local API responds at 127.0.0.1:{0}" -f $foundPort) -ForegroundColor Green
  Write-Host ("ComfyUI reports: {0}" -f $comfyDevice)
} else {
  Write-Warning "No local API responded on common ports. Open ComfyUI Desktop completely and check Settings -> Server Config for its active port."
}
Write-Host "No installation, model download, network sharing, or account setting was changed."
$report | ConvertTo-Json -Depth 5
