Build the notebook:
```
docker build --rm -t jupyter/opencv-notebook .
```

Run the notbook:
```
docker run -v /Users/eric/Projects/cv_ftc:/home/jovyan/work -d -p 8888:8888 jupyter/opencv-notebook
```

Check the token for the jupyter notebook
```
docker exec -it wonderful_galois jupyter notebook list
```

open the browser and type in http://localhost:8888/
# cv_frc
