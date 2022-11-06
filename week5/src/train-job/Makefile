buildimage:
	cp ../config.py . && docker build --progress=plain -t sd-concept-train-job:latest ./

pushimage:
	docker push gcr.io/sd-concept-project/sd-concept-train-job:latest

tagimage:
	docker image tag sd-concept-train-job:latest gcr.io/sd-concept-project/sd-concept-train-job:latest

runimage:
	docker run -d sd-concept-train-job:latest
