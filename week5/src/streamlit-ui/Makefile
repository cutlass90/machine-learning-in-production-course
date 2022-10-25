build:
	docker build --progress=plain -t sd-concept-ui:latest ./

pushimage:
	docker push gcr.io/sd-concept-project/sd-concept-ui:latest

tagimage:
	docker image tag sd-concept-ui:latest gcr.io/sd-concept-project/sd-concept-ui:latest

runimage:
	docker run -p 8501:8501 -d sd-concept-ui:latest

runui:
	streamlit run streamlit_ui.py --server.maxUploadSize 3000

deploy:
	kubectl apply -f deployment.yaml