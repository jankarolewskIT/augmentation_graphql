<h1>This is a new version of the augmentation project, which aims to better understand GraphQL</hq>

<h3>In order to use application fallow this guide lines</h3>

<ol>
  <li>Clone this repository --- git clone (this repo url)</li>
  <li>Type docker-compose up while you are in Project main directory</li>
  <h4>App is up and running, however you also would want to migarte data to Postgres DB</h4>
  <li>Enter yout container --- docker exec -it (container ID)</li>
  <li>Inside your conatiner migrate data --- python manage.py migarte</li>
  <h4>Prepare test cases</h4>
  <li>type: python images/loaders/image_loader.py</li>
  <li>type: python images/loaders/image_loader.py</li>
  <h3>Make tests</h3>
  <li>type python manage.py test</li>
  <h2>You are good to go! Go to: <strong>http://0.0.0.0:8000/graphql/</strong> and try my app by yourself</h2>
</ol>
