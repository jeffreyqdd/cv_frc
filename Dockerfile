FROM jupyter/datascience-notebook

# install in the default python3 environment
RUN pip install 'opencv-python==4.2.0.32'
