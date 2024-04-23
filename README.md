# Simple Flutter Web App 
### This is just a demonstration app to showcase a few functionalities of a web application



## web\_app
This directory contains the web application which was originally written in Flutter and was then compiled to html and javascript. If anyone is interested in the source code, feel free to reach out to me. The application is based on the app you build along with the [official beginner tutorial](https://codelabs.developers.google.com/codelabs/flutter-codelab-first#0) with some additional features illustrating API calls and database usage.

## python\_api
This directory contains two python scripts that create two different API's. The `my_api.py` file showcases a simple API with a database connection while the `my_model_api.py` file contains a connection to a [LLM](https://huggingface.co/KomeijiForce/bart-base-emojilm) (size of ~600 MB, so be warned) which will be run for 'good practice' inside a docker container.

## Usage
Make sure to install all dependencies with the `requirements.txt` inside the python\_api directory and to have docker installed.

1. To start the web app you simply start a web server inside the web\_app directory like
			
		python -m http.server 8888
		
2. To start the API of `my_api.py` you simply call the script, as the web server is defined in the main, eg.

		python my_api.py

3. To start the API of `my_model_api.py` you first need to build the docker container with

		docker build -t my_model_api . 

	and afterwards you can run it with


		docker run -p 4000:80 my_model_api
		
4. Lastly, if you didnt change any of the ports, you will find your web app hosted at 

		http://localhost:8888/