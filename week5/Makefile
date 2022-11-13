createcluster:
	gcloud container clusters create sd-concept-cluster --zone us-central1-a --machine-type n1-standard-8 --num-nodes 1 --service-account=sd-concept-service-account@sd-concept-project.iam.gserviceaccount.com
	gcloud container node-pools create train-node-pool     --cluster sd-concept-cluster --accelerator type=nvidia-tesla-a100,count=1 --machine-type a2-highgpu-1g --num-nodes 1 --enable-autoscaling --min-nodes 0 --max-nodes 3 --zone us-central1-a --service-account=sd-concept-service-account@sd-concept-project.iam.gserviceaccount.com --preemptible
	gcloud container node-pools create inference-node-pool --cluster sd-concept-cluster --accelerator type=nvidia-tesla-p4,count=1   --machine-type n1-standard-8 --num-nodes 1 --enable-autoscaling --min-nodes 1 --max-nodes 2 --zone us-central1-a --service-account=sd-concept-service-account@sd-concept-project.iam.gserviceaccount.com --preemptible
	gcloud container clusters get-credentials sd-concept-cluster --zone us-central1-a --project sd-concept-project
	kubectl get nodes
	#kubectl label nodes <your-node-name> type=streamlit-ui
	#kubectl label nodes <your-node-name> type=inference
	#kubectl label nodes <your-node-name> type=train

deployall:
	kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/container-engine-accelerators/master/nvidia-driver-installer/cos/daemonset-preloaded.yaml
	kubectl apply -f https://github.com/kedacore/keda/releases/download/v2.8.0/keda-2.8.0.yaml
	cd yamls && kubectl apply -f secret.yaml
	cd yamls && kubectl apply -f redis-deployment.yaml
	cd yamls && kubectl apply -f configmap.yaml && kubectl apply -f streamlit-ui-deployment.yaml
	cd yamls && kubectl apply -f web-server-deployment.yaml
	cd yamls && kubectl apply -f inference-server-deployment.yaml
	cd yamls && kubectl apply -f train-server-deployment.yaml
	cd yamls && kubectl apply -f inference-autoscaler.yaml
	cd yamls && kubectl apply -f train-autoscaler.yaml

deletecluster:
	gcloud container clusters delete sd-concept-cluster --zone us-central1-a

runallcontainers:
	docker run -p 6379:6379 -d redis
	cd src/web-server && make runimage
	cd src/streamlit-ui && make runimage
	cd src/inference-server && make runimage
	cd src/train-server && make runimage


stopallcontainers:
	docker ps -q | xargs docker stop

deletealldeploymets:
	kubectl delete all --all -n default

buildall:
	cd src/inference-server && make buildimage
	cd src/streamlit-ui     && make buildimage
	cd src/web-server       && make buildimage
	cd src/train-server     && make buildimage

pushall:
	cd src/inference-server && make tagimage && make pushimage
	cd src/streamlit-ui     && make tagimage && make pushimage
	cd src/web-server       && make tagimage && make pushimage
	cd src/train-server     && make tagimage && make pushimage


