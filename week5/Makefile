createcluster:
	gcloud container clusters create sd-concept-cluster --zone us-central1-a --machine-type n1-standard-8 --num-nodes 1 --service-account=sd-concept-service-account@sd-concept-project.iam.gserviceaccount.com
	#gcloud container node-pools create train-node-pool --cluster sd-concept-cluster --accelerator type=nvidia-tesla-a100,count=1 --machine-type a2-highgpu-1g --num-nodes 1 --enable-autoscaling --min-nodes 0 --max-nodes 3 --zone us-central1-a
	gcloud container node-pools create inference-node-pool --cluster sd-concept-cluster --accelerator type=nvidia-tesla-k80,count=1 --machine-type n1-standard-8 --num-nodes 1 --enable-autoscaling --min-nodes 1 --max-nodes 5 --zone us-central1-a --service-account=sd-concept-service-account@sd-concept-project.iam.gserviceaccount.com
	#gcloud container node-pools create inference-node-pool --cluster sd-concept-cluster --accelerator type=nvidia-tesla-p4,count=1 --machine-type n1-standard-8 --num-nodes 1 --enable-autoscaling --min-nodes 1 --max-nodes 5 --zone us-central1-a --service-account=sd-concept-service-account@sd-concept-project.iam.gserviceaccount.com
	gcloud container clusters get-credentials sd-concept-cluster --zone us-central1-a --project sd-concept-project
	kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/container-engine-accelerators/master/nvidia-driver-installer/cos/daemonset-preloaded.yaml
	kubectl get nodes
	#kubectl label nodes <your-node-name> type=streamlit-ui
	#kubectl label nodes <your-node-name> type=inference

deployall:
	cd src/inference-server && kubectl apply -f secret.yaml

deletecluster:
	gcloud container clusters delete sd-concept-cluster --zone us-central1-a

runallcontainers:
	cd src/streamlit-ui && make runimage && cd ../web-server && make runimage && cd ../inference-server && make runimage

stopallcontainers:
	docker ps -q | xargs docker stop

deletealldeploymets:
	kubectl delete all --all -n default


