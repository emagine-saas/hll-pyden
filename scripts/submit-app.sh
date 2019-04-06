#!/usr/bin/env bash

token=$(curl -X GET -u ${SPLUNK_CREDS} --url https://api.splunk.com/2.0/rest/login/splunk | python -c 'import sys, json; print(json.load(sys.stdin)["data"]["token"])' "$i")
pyden_id=$(curl -X POST -H "Authorization: bearer $token" -H "Cache-Control: no-cache" -F "app_package=@$1.tgz" --url "https://appinspect.splunk.com/v1/app/validate" | python -c 'import sys, json; print(json.load(sys.stdin)["request_id"])' "$i")
pyden_status=true
#curl -X GET -H "Authorization: bearer $token" --url https://appinspect.splunk.com/v1/app/validate/status/${pyden_id}
while ${pyden_status}
do
    job_status=$(curl -X GET -H "Authorization: bearer $token" --url https://appinspect.splunk.com/v1/app/validate/status/${pyden_id} | python -c 'import sys, json; print(json.load(sys.stdin)["status"])' "$i")
    if [[ "$job_status" == "SUCCESS" ]] || [[ "$job_status" == "ERROR" ]]
    then
        pyden_status=false
    else
        sleep 5
    fi
done
curl -X GET -H "Authorization: bearer $token" -H "Cache-Control: no-cache" -H "Content-Type: text/html" --url https://appinspect.splunk.com/v1/app/report/${pyden_id} > $1.html
pyden_failures=$(curl -X GET -H "Authorization: bearer $token" -H "Cache-Control: no-cache" -H "Content-Type: application/json" --url https://appinspect.splunk.com/v1/app/report/${pyden_id} | python -c 'import sys, json; print(json.load(sys.stdin)["summary"]["failure"])' "$i")
if [[ ${pyden_failures} -gt 0 ]]
then
    echo "There were one or more failures for Pyden app"
fi
exit ${pyden_failures}