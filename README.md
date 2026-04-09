#for offline > this is bad, but if u can run this it much easiler to test(I use python 11, and python 12 is bugged)

pip install --no-cache-dir -r requirements.txt

uvicorn app.main:app --reload

for docker > env god

docker build -t sign-language-game .

docker run -p 8000:8000 sign-language-game