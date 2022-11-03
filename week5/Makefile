createcluster:
	gcloud container clusters create sd-concept-cluster --zone us-central1-a --machine-type e2-medium --num-nodes 1 --service-account=sd-concept-service-account@sd-concept-project.iam.gserviceaccount.com
	#gcloud container node-pools create train-node-pool --cluster sd-concept-cluster --accelerator type=nvidia-tesla-a100,count=1 --machine-type a2-highgpu-1g --num-nodes 1 --enable-autoscaling --min-nodes 0 --max-nodes 3 --zone us-central1-a
	gcloud container node-pools create inference-node-pool --cluster sd-concept-cluster --machine-type n1-standard-8 --num-nodes 1 --enable-autoscaling --min-nodes 1 --max-nodes 5 --zone us-central1-a
	gcloud container clusters get-credentials sd-concept-cluster --zone us-central1-a --project sd-concept-project
	kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/container-engine-accelerators/master/nvidia-driver-installer/cos/daemonset-preloaded.yaml
	kubectl get nodes --show-labels
	#kubectl label nodes <your-node-name> type=streamlit-ui
	#kubectl label nodes <your-node-name> type=inference

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