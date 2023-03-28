echo $1
sudo chmod 777 -R OJ/database
git add .
git commit -m $1
git push -u origin master