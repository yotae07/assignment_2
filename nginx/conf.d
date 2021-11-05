upstream django {
    server assignment_2_backend_1:8000;
    server localhost:8000;
    server 127.0.0.1:8000;
}


server {
    listen 80;
    location / {
        proxy_pass http://django:8000;
        proxy_redirect off;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_set_header  X-Real-IP   $remote_addr;
        proxy_redirect off;
    }
}