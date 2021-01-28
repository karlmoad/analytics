import yaml
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import sample_reader
import os
import json

def main(config):
    endpoint = config["azure"]["endpoint"]
    key = config["azure"]["key"]

    print("Endpoint: " + endpoint)

    client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
        api_version="v3.1-preview.3")

    #documents = [
    #    {"id":"1", "language":"en" ,"text":"Subject is taking 100mg of ibuprofen twice daily"},
    #]

    # load sample documents from docs folder
    path = os.path.join(os.curdir, 'docs')
    reader = sample_reader.SampleReader(path)
    documents = reader.process()

    poller = client.begin_analyze_healthcare(documents, show_stats=True)
    result = poller.result()

    print("Results of Healthcare Analysis:")
    rez = []
    for idx, doc in enumerate(result):
        rezd = {"id": doc.id, "entities": [], "relations": []}
        for entity in doc.entities:
            e = {
                "entity": entity.text,
                "category": entity.category,
                "subcategory": entity.subcategory,
                "offset": entity.offset,
                "score": entity.confidence_score,
            }
            rezd["entities"].append(e)

        for relation in doc.relations:
            r = {
                "source": relation.source.text,
                "target": relation.target.text,
                "type": relation.relation_type,
                "is_bidirectional": relation.is_bidirectional
            }
            rezd["relations"].append(r)
        rez.append(rezd)

    # write output

    outputFile = os.path.join(os.curdir, "dumps", "out.json")
    with open(outputFile, 'w') as out:
        json.dump(rez, out)

if __name__ == '__main__':
    with open("config.yaml","r") as yamlfile:
        cfg = yaml.safe_load(yamlfile)
    main(cfg)