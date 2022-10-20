createcluster:
	gcloud container clusters create sd-concept-cluster --zone us-central1-a --accelerator type=nvidia-tesla-a100,count=1 --machine-type a2-highgpu-1g --num-nodes 1
	gcloud container clusters get-credentials sd-concept-cluster --zone us-central1-a --project sd-concept-project
	kubectl get nodes #just to watch that nodes were created
	kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/container-engine-accelerators/master/nvidia-driver-installer/cos/daemonset-preloaded.yaml
	kubectl get pods -A #just to watch that nvidiia driver installator pod  was created

deploy:
	kubectl apply -f deployment.yaml

deletecluster:
	gcloud container clusters delete sd-concept-cluster --zone us-central1-a

build:
	docker build --progress=plain -t sd-concept:latest ./

runimage:
	docker run -p 1234:1234 --gpus all -d sd-concept:latest

pushimage:
	docker push gcr.io/sd-concept-project/sd-concept:latest

runimagedebug:
	docker run -p 1234:1234 --gpus all -it -v /home/nazar/machine_learning_in_production_course/week5/weights:/workspace/src/weights sd-concept:latest /bin/bash