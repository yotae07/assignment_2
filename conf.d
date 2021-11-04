upstream fresh_code {
    ip_hash;
    server assignment_2_backend_1:8000; # 서버의 컨테이너 명
}

server {
    location / {
        proxy_pass http://fresh_code/;
    }

    listen 80;
    server_name localhost;
}