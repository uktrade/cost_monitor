# Cost Monitor 

#### Purpose is to update Cost Forcasting dashboard for
- AWS
- HEROKU

### Environment Variables

    ```bash
    export DEBUG=True
    export SECRET_KEY=<django-secret-key>
    export ALLOWED_HOSTS='localhost,127.0.0.1
    export HEROKU_API_KEY=<heroku-api-key>
    export HEROKU_SITE=https://api.heroku.com
    export GECKO_TOKEN='<gecko API token>'
    export AWS_ACCESS_KEY_ID='<aws access key id>'
    export AWS_SECRET_KEY='<aws secret key>'
    export AWS_ACCESS_KEY_ID='<Billing account access key>'
    export AWS_SECRET_ACCESS_KEY='<Billing account secret key>'
    export GDS_SITE=https://admin.london.cloud.service.gov.uk/login
    export GDS_LOGIN_SITE=https://login.london.cloud.service.gov.uk
    export GDS_USER=<webuser>
    export GDS_USER_PASS=<webuser password>
    ```

### Command
```bash
$python manage.py run_reports
```