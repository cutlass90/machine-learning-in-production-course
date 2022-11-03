buildimage:
	docker build --progress=plain -t sd-concept-inference:latest ./

pushimage:
	docker push gcr.io/sd-concept-project/sd-concept-inference:latest

tagimage:
	docker image tag sd-concept-inference:latest gcr.io/sd-concept-project/sd-concept-inference:latest

runimage:
	docker run -d sd-concept-inference:latest

runimagedebug:
	docker run --rm -it -p 8283:8283 --gpus all -v /home/nazar/machine-learning-in-production-course/week5/src/inference-server:/workspace/src/weights sd-concept-inference:latest /bin/bash

deploy:
	kubectl apply -f deployment.yaml