import numpy as np
import pandas as pd
import time
import yaml
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

def main(config):
    endpoint = config["azure"]["endpoint"]
    key = config["azure"]["key"]

    print("Endpoint: " + endpoint)

    client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
        api_version="v3.1-preview.3")

    documents = [
        {"id":"1", "language":"en" ,"text":"Subject is taking 100mg of ibuprofen twice daily"},
    ]

    #documents = ["Subject is taking 100mg of ibuprofen twice daily"]

    poller = client.begin_analyze_healthcare(documents, show_stats=True)
    result = poller.result()

    docs = [doc for doc in result if not doc.is_error]

    print("Results of Healthcare Analysis:")
    for idx, doc in enumerate(docs):
        print(doc)
        for entity in doc.entities:
            print("Entity: {}".format(entity.text))
            print("...Category: {}".format(entity.category))
            print("...Subcategory: {}".format(entity.subcategory))
            print("...Offset: {}".format(entity.offset))
            print("...Confidence score: {}".format(entity.confidence_score))
            if entity.links is not None:
                print("...Links:")
                for link in entity.links:
                    print("......ID: {}".format(link.id))
                    print("......Data source: {}".format(link.data_source))
        for relation in doc.relations:
            print("Relation:")
            print("...Source: {}".format(relation.source.text))
            print("...Target: {}".format(relation.target.text))
            print("...Type: {}".format(relation.relation_type))
            print("...Bidirectional: {}".format(relation.is_bidirectional))
        print("------------------------------------------")

if __name__ == '__main__':
    with open("config.yaml","r") as yamlfile:
        cfg = yaml.safe_load(yamlfile)
    main(cfg)