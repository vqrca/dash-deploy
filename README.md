Commands to build and deploy the application
```
gcloud builds submit --tag gcr.io/plotly-dash-414917/dash-heart-disease  --project=plotly-dash-414917

gcloud run deploy --image gcr.io/plotly-dash-414917/dash-heart-disease --platform managed  --project=plotly-dash-414917 --allow-unauthenticated
```
