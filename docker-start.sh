#!/bin/bash

# BAYKAR İHA Docker Başlatma Scripti
# Kullanım: ./docker-start.sh [build|start|stop|restart|logs|shell|clean]

set -e

PROJECT_NAME="baykar-iha"
IMAGE_NAME="baykar-iha-detection:latest"
CONTAINER_NAME="iha-detection-system"

# Renkler
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonksiyonlar
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker yüklü değil!"
        exit 1
    fi
    print_success "Docker bulundu"
}

check_nvidia_docker() {
    if ! docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi &> /dev/null; then
        print_warning "NVIDIA Docker runtime bulunamadı. GPU desteği olmayabilir."
    else
        print_success "NVIDIA Docker runtime bulundu"
    fi
}

build_image() {
    print_info "Docker image oluşturuluyor..."
    docker build -t $IMAGE_NAME .
    print_success "Image oluşturuldu: $IMAGE_NAME"
}

start_container() {
    print_info "Container başlatılıyor..."
    
    # Eski container varsa durdur
    if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
        print_warning "Eski container bulundu, durduruluyor..."
        docker stop $CONTAINER_NAME 2>/dev/null || true
        docker rm $CONTAINER_NAME 2>/dev/null || true
    fi
    
    # Yeni container başlat
    docker run -d \
        --name $CONTAINER_NAME \
        --gpus all \
        -v "$(pwd)/models:/app/models" \
        -v "$(pwd)/data:/app/data" \
        -v "$(pwd)/outputs:/app/outputs" \
        -v "$(pwd)/runs:/app/runs" \
        -v "$(pwd)/logs:/app/logs" \
        -p 8000:8000 \
        --restart unless-stopped \
        $IMAGE_NAME
    
    print_success "Container başlatıldı: $CONTAINER_NAME"
    print_info "Logları görmek için: docker logs -f $CONTAINER_NAME"
}

stop_container() {
    print_info "Container durduruluyor..."
    docker stop $CONTAINER_NAME 2>/dev/null || true
    docker rm $CONTAINER_NAME 2>/dev/null || true
    print_success "Container durduruldu"
}

restart_container() {
    stop_container
    start_container
}

show_logs() {
    print_info "Container logları (Çıkmak için Ctrl+C)..."
    docker logs -f $CONTAINER_NAME
}

open_shell() {
    print_info "Container shell açılıyor..."
    docker exec -it $CONTAINER_NAME bash
}

clean_all() {
    print_warning "Tüm container ve image'lar silinecek!"
    read -p "Devam etmek istiyor musunuz? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        stop_container
        docker rmi $IMAGE_NAME 2>/dev/null || true
        print_success "Temizlik tamamlandı"
    else
        print_info "İptal edildi"
    fi
}

show_status() {
    print_info "Container durumu:"
    docker ps -a --filter name=$CONTAINER_NAME --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    
    if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
        echo ""
        print_info "GPU durumu:"
        docker exec $CONTAINER_NAME nvidia-smi --query-gpu=index,name,memory.used,memory.total --format=csv,noheader
    fi
}

show_help() {
    cat << EOF
🚁 BAYKAR İHA Docker Yönetim Scripti

Kullanım: $0 [komut]

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
  $0 build && $0 start    # Image oluştur ve başlat
  $0 logs                 # Logları izle
  $0 shell                # Container içine gir

EOF
}

# Ana program
main() {
    check_docker
    
    case "${1:-help}" in
        build)
            check_nvidia_docker
            build_image
            ;;
        start)
            start_container
            ;;
        stop)
            stop_container
            ;;
        restart)
            restart_container
            ;;
        logs)
            show_logs
            ;;
        shell)
            open_shell
            ;;
        status)
            show_status
            ;;
        clean)
            clean_all
            ;;
        help|*)
            show_help
            ;;
    esac
}

main "$@"
