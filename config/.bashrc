alias coconut="source /home/salvacarrion/Coconut/venv-coconut/bin/activate && cd /home/salvacarrion/Coconut/mycoconut"

pullrepo(){
        sudo rm -r /home/salvacarrion/Coconut/mycoconut/
        cd /home/salvacarrion/Coconut/
        git clone https://github.com/salvacarrion/mycoconut.git
        coconut
}

runcoconut() {
        coconut
        python manage.py runserver 0.0.0.0:8000
}

reloadsupervisor(){
    sudo cp /home/salvacarrion/Coconut/mycoconut/config/supervisor.conf /etc/supervisor/conf.d/supervisor.conf
    sudo supervisorctl reread
    sudo supervisorctl update
    sudo supervisorctl restart all
}

rebootcoconut(){
        sudo chmod u+x ~/Coconut/mycoconut/config/gunicorn_start.sh
        sudo service nginx reload
        reloadsupervisor
}

copynginx(){
        sudo cp /home/salvacarrion/Coconut/mycoconut/config/coconut.nginxconf /etc/nginx/sites-available
}