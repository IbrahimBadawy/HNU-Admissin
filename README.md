# hnu-admission


requests

pip install virtualenv
virtualenv venv
venv\scripts\activate

pip install -r requirements.txt
pip freeze > requirements.txt  
cd backend

python manage.py collectstatic
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser


venv\scripts\activate cd backend

python manage.py makemigrations
python manage.py migrate
daphne -b admission.hnu.edu.eg -p 8000 hnu_addmission.asgi:application

cd hnu-admission
cd frontend
npm run dev

npm install 



git add .
git commit -m "تعديلات من السيرفر"
git push origin main



git clone https://github.com/IbrahimBadawy/HNU-Admissin.git .
git pull origin main