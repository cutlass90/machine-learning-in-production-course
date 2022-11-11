buildimage:
	cp ../config.py . && docker build --progress=plain -t sd-concept-train:latest ./

pushimage:
	docker push gcr.io/sd-concept-project/sd-concept-train:latest

tagimage:
	docker image tag sd-concept-train:latest gcr.io/sd-concept-project/sd-concept-train:latest

runimage:
	docker run -d --gpus all -v /home/nazar/machine-learning-in-production-course/week5/src/secrets:/workspace/src/secrets sd-concept-train:latest