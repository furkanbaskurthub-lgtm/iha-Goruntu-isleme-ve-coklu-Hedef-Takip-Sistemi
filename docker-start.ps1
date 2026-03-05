# BAYKAR İHA Docker Başlatma Scripti (Windows PowerShell)
# Kullanım: .\docker-start.ps1 [build|start|stop|restart|logs|shell|clean|status]

param(
    [Parameter(Position=0)]
    [ValidateSet('build','start','stop','restart','logs','shell','clean','status','help')]
    [string]$Command = 'help'
)

$ProjectName = "baykar-iha"
$ImageName = "baykar-iha-detection:latest"
$ContainerName = "iha-detection-system"

# Renkli çıktı fonksiyonları
function Write-Info {
    param([string]$Message)
    Write-Host "ℹ️  $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠️  $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

# Docker kontrolü
function Test-Docker {
    try {
        docker --version | Out-Null
        Write-Success "Docker bulundu"
        return $true
    }
    catch {
        Write-Error "Docker yüklü değil veya çalışmıyor!"
        return $false
    }
}

# NVIDIA Docker kontrolü
function Test-NvidiaDocker {
    try {
        docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi 2>&1 | Out-Null
        Write-Success "NVIDIA Docker runtime bulundu"
        return $true
    }
    catch {
        Write-Warning "NVIDIA Docker runtime bulunamadı. GPU desteği olmayabilir."
        return $false
    }
}

# Image oluştur
function Build-Image {
    Write-Info "Docker image oluşturuluyor..."
    docker build -t $ImageName .
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Image oluşturuldu: $ImageName"
    }
    else {
        Write-Error "Image oluşturma başarısız!"
    }
}

# Container başlat
function Start-Container {
    Write-Info "Container başlatılıyor..."
    
    # Eski container varsa durdur
    $existing = docker ps -aq -f name=$ContainerName
    if ($existing) {
        Write-Warning "Eski container bulundu, durduruluyor..."
        docker stop $ContainerName 2>$null
        docker rm $ContainerName 2>$null
    }
    
    # Yeni container başlat
    $currentDir = Get-Location
    docker run -d `
        --name $ContainerName `
        --gpus all `
        -v "${currentDir}/models:/app/models" `
        -v "${currentDir}/data:/app/data" `
        -v "${currentDir}/outputs:/app/outputs" `
        -v "${currentDir}/runs:/app/runs" `
        -v "${currentDir}/logs:/app/logs" `
        -p 8000:8000 `
        --restart unless-stopped `
        $ImageName
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Container başlatıldı: $ContainerName"
        Write-Info "Logları görmek için: docker logs -f $ContainerName"
    }
    else {
        Write-Error "Container başlatma başarısız!"
    }
}

# Container durdur
function Stop-Container {
    Write-Info "Container durduruluyor..."
    docker stop $ContainerName 2>$null
    docker rm $ContainerName 2>$null
    Write-Success "Container durduruldu"
}

# Container yeniden başlat
function Restart-Container {
    Stop-Container
    Start-Container
}

# Logları göster
function Show-Logs {
    Write-Info "Container logları (Çıkmak için Ctrl+C)..."
    docker logs -f $ContainerName
}

# Shell aç
function Open-Shell {
    Write-Info "Container shell açılıyor..."
    docker exec -it $ContainerName bash
}

# Temizlik
function Clean-All {
    Write-Warning "Tüm container ve image'lar silinecek!"
    $response = Read-Host "Devam etmek istiyor musunuz? (y/N)"
    if ($response -eq 'y' -or $response -eq 'Y') {
        Stop-Container
        docker rmi $ImageName 2>$null
        Write-Success "Temizlik tamamlandı"
    }
    else {
        Write-Info "İptal edildi"
    }
}

# Durum göster
function Show-Status {
    Write-Info "Container durumu:"
    docker ps -a --filter name=$ContainerName --format "table {{.Names}}`t{{.Status}}`t{{.Ports}}"
    
    $running = docker ps -q -f name=$ContainerName
    if ($running) {
        Write-Host ""
        Write-Info "GPU durumu:"
        docker exec $ContainerName nvidia-smi --query-gpu=index,name,memory.used,memory.total --format=csv,noheader
    }
}

# Yardım
function Show-Help {
    Write-Host @"
🚁 BAYKAR İHA Docker Yönetim Scripti (Windows)

Kullanım: .\docker-start.ps1 [komut]

Komutlar:
  build       Docker image oluştur
  start       Container'ı başlat
  stop        Container'ı durdur
  restart     Container'ı yeniden başlat
  logs        Container loglarını göster
  shell       Container içine bash ile gir
  status      Container durumunu göster
  clean       Tüm container ve image'ları sil
  help        Bu yardım mesajını göster

Örnekler:
  .\docker-start.ps1 build
  .\docker-start.ps1 start
  .\docker-start.ps1 logs
  .\docker-start.ps1 shell

"@
}

# Ana program
if (-not (Test-Docker)) {
    exit 1
}

switch ($Command) {
    'build' {
        Test-NvidiaDocker
        Build-Image
    }
    'start' {
        Start-Container
    }
    'stop' {
        Stop-Container
    }
    'restart' {
        Restart-Container
    }
    'logs' {
        Show-Logs
    }
    'shell' {
        Open-Shell
    }
    'status' {
        Show-Status
    }
    'clean' {
        Clean-All
    }
    'help' {
        Show-Help
    }
    default {
        Show-Help
    }
}
