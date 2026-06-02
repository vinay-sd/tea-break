import subprocess, base64

nginx_conf = b"""server {
    listen 80;
    listen [::]:80;
    server_name crm.socialdrishti.com;

    location /.well-known/acme-challenge/ {
        root /var/www/crm;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;

    server_name crm.socialdrishti.com;

    ssl_certificate /etc/letsencrypt/live/crm.socialdrishti.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/crm.socialdrishti.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384';
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    root /var/www/crm;
    index index.php index.html;

    location = /break {
        return 301 /break/;
    }

    location /break/ {
        include fastcgi_params;
        fastcgi_pass 127.0.0.1:16000;
        fastcgi_param SCRIPT_FILENAME /var/www/tea-break/index.php;
        fastcgi_param REQUEST_URI /;
        fastcgi_param DOCUMENT_URI /;
        fastcgi_param SCRIPT_NAME /index.php;
        fastcgi_param HTTPS on;
    }

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~* ^/app/(config|data|auth)/ {
        deny all;
        return 403;
    }

    location ~* \\.(json|sql|log|env|ini|sh|py)$ {
        deny all;
        return 403;
    }

    location ~ \\.php$ {
        include fastcgi_params;
        fastcgi_pass 127.0.0.1:18000;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param HTTPS on;
    }

    location ~ /\\.(?!well-known).* {
        deny all;
    }
}
"""

encoded = base64.b64encode(nginx_conf).decode()
cmd = (
    f'su deploy -s /bin/bash -c "'
    f'printf \\"%s\\" \\"{encoded}\\" | base64 -d > /tmp/crm.conf && '
    f'sudo cp /tmp/crm.conf /etc/nginx/sites-enabled/hello-world-1234.conf && '
    f'sudo nginx -t 2>&1 | tail -2 && '
    f'sudo systemctl reload nginx && '
    f'echo DONE'
    f'"'
)
result = subprocess.run(['python', 'ssh_helper.py', 'exec', cmd], capture_output=True, text=True)
print("OUT:", result.stdout)
print("ERR:", result.stderr[-500:])



