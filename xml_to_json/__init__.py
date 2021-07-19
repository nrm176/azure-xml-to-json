import logging
import requests
import azure.functions as func
import json
import xmltodict
import os


def send_request(name, address):
    # 法人番号API 名前から検索
    # GET https://api.houjin-bangou.nta.go.jp/4/name

    try:
        response = requests.get(
            url="https://api.houjin-bangou.nta.go.jp/4/name",
            params={
                "id": os.environ.get('TAX_API_APP_ID'),
                "name": name,
                "address": address,
                "type": "12",
                "mode": "2",
            },
        )

        data_dict = xmltodict.parse(response.content)
        json_data = json.dumps(data_dict)

        print('Response HTTP Response Body: {content}'.format(
            content=json_data))
        return json_data
    except requests.exceptions.RequestException:
        raise


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    address = req.params.get('address')
    if name and address:
        try:
            res_json = send_request(name, address)
        except ValueError:
            pass
        return func.HttpResponse(
            res_json,
            mimetype="application/json",
            status_code=200
        )
    return func.HttpResponse(
        status_code=505,
        body={'error':'please set both name and address.'}
    )
