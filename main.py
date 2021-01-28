import yaml
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import sample_reader
import sample_formatter
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

    # load sample documents from docs folder
    path = os.path.join(os.curdir, 'docs')
    reader = sample_reader.SampleReader(path)
    documents = reader.process()

    print("Documents [{}]".format(len(documents)))

    # --------------------------------------------------------------------
    # per Microsoft documentation concerning document size a data limits
    # [https://docs.microsoft.com/en-us/azure/cognitive-services/text-analytics/concepts/data-limits?tabs=version-3]
    # size of individual document can not exceed 5,120 characters and
    #   the max number of docs to send per request is 10/1000 web vs container
    # to accommodate larger documents and adhere to the request batch size each documents will be sent individually
    #    with larger documents being broken into multiple sub documents
    # Note: Larger documents will utilize an a split at 4000 characters per block adn will seek to
    #   identify end of current sentence contexts within the same block
    # --------------------------------------------------------------------

    formatter = sample_formatter.SampleFormatter(limit=4000, noexceed=5100)

    for d in documents:
        print("Document:{} Size:{}".format(d["name"], len(d["text"])))
        prepared = formatter.prepare(document=d)
        for item in prepared:
            print("Id:{} Size:{}".format(item["id"], len(item["text"])))








    # poller = client.begin_analyze_healthcare(documents, show_stats=True)
    # result = poller.result()
    #
    # print("Results of Healthcare Analysis:")
    # rez = []
    # docs = [doc for doc in result if not doc.is_error]
    # for idx, doc in enumerate(docs):
    #     rezd = {"id": doc.id}
    #     entities=[]
    #     relations=[]
    #     for entity in doc.entities:
    #         e = {
    #             "entity": entity.text,
    #             "category": entity.category,
    #             "subcategory": entity.subcategory,
    #             "offset": entity.offset,
    #             "score": entity.confidence_score,
    #         }
    #         entities.append(e)
    #
    #     for relation in doc.relations:
    #         r = {
    #             "source": relation.source.text,
    #             "target": relation.target.text,
    #             "type": relation.relation_type,
    #             "is_bidirectional": relation.is_bidirectional
    #         }
    #         relations.append(r)
    #     rezd["entities"] = entities
    #     rezd["relations"] = relations
    #     rez.append(rezd)
    #
    # # write output
    # outputFile = os.path.join(os.curdir, "dumps", "out.json")
    # print("Writing output file [{}}.".format(outputFile))
    # with open(outputFile, 'w') as out:
    #     json.dump(rez, out)

if __name__ == '__main__':
    with open("config.yaml","r") as yamlfile:
        cfg = yaml.safe_load(yamlfile)
    main(cfg)