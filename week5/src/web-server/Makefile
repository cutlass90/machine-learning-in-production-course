buildimage:
	cp ../config.py . && docker build --progress=plain -t sd-concept-web-server:latest ./

pushimage:
	docker push gcr.io/sd-concept-project/sd-concept-web-server:latest

tagimage:
	docker image tag sd-concept-web-server:latest gcr.io/sd-concept-project/sd-concept-web-server:latest

runimage:
	docker run -d -p 8000:8000 -v /home/nazar/machine-learning-in-production-course/week5/src/secrets:/code/secrets sd-concept-web-server:latest

runimagedebug:
	docker run --rm -it -v /home/nazar/machine-learning-in-production-course/week5/src/secrets:/code/secrets sd-concept-web-server:latest

deploy:
	kubectl apply -f deployment.yaml