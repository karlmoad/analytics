import mars_formatter
import mars_reader
import yaml
import os
import json
import sys
import datetime
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

def mars(config, argv):

    if len(argv) < 4:
        print("Invalid inputs")
        return

    dtStart = datetime.datetime.utcnow()
    apiTime=[]

    directory = argv[1]
    inputFile = argv[2]
    outputDir = argv[3]

    endpoint = config["azure"]["endpoint"]
    key = config["azure"]["key"]
    client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
        api_version="v3.1-preview.3")

    # load sample documents from docs folder
    path = os.path.join(directory, inputFile)

    print("Input File: {}".format(path))

    reader = mars_reader.MarsReader(path)
    data = reader.process()

    print("Documents read: {}".format(len(data)))

    # temp take only a small part of total
    data = data[100:200]

    # --------------------------------------------------------------------
    # per Microsoft documentation concerning document size a data limits
    # [https://docs.microsoft.com/en-us/azure/cognitive-services/text-analytics/concepts/data-limits?tabs=version-3]
    # size of individual document can not exceed 5,120 characters and
    #   the max number of docs to send per request is 10/1000 web vs container
    # to accommodate larger documents and adhere to the request batch size each documents will be sent individually
    #    with larger documents being broken into multiple sub documents
    # Note: Larger documents will utilize an a split at 4500 characters per block adn will seek to
    #   identify end of current sentence contexts within the same block
    # --------------------------------------------------------------------
    formatter = mars_formatter.MarsFormatter(limit=4500, noexceed=5100)

    for d in data:
        print("Document: {} -- processing".format(d["id"]))
        batch = formatter.prepare(d)

        chunks = []
        offset = 0

        # save chunking offsets so that positional findings in results can be re-attributed to orig
        for item in batch:
            chunk = {"id": item["id"], "start": offset, "length": len(item["text"])}
            offset += len(item["text"])
            chunks.append(chunk)
        d["chunks"] = chunks

        try:
            dtApiStart = datetime.datetime.utcnow()
            poller = client.begin_analyze_healthcare(batch, show_stats=True)
            result = poller.result()
            dtApiEnd = datetime.datetime.utcnow()

            ttr = {"start": dtApiStart, "end": dtApiEnd, "seconds": (dtApiEnd-dtApiStart).total_seconds()}
            apiTime.append(ttr)

            rez = []
            results = [r for r in result if not r.is_error]
            for idx, r in enumerate(results):
                rezd = {"id": r.id}
                entities = []
                relations = []
                for entity in r.entities:
                    e = {
                        "entity": entity.text,
                        "category": entity.category,
                        "subcategory": entity.subcategory,
                        "offset": entity.offset,
                        "score": entity.confidence_score,
                        "links": [],
                    }
                    if entity.links is not None:
                        links=[]
                        for link in entity.links:
                            l = {"id": link.id, "source": link.data_source}
                            links.append(l)
                        e["links"] = links

                    entities.append(e)

                for relation in r.relations:
                    r = {
                        "source": relation.source.text,
                        "target": relation.target.text,
                        "type": relation.relation_type,
                        "is_bidirectional": relation.is_bidirectional
                    }
                    relations.append(r)
                rezd["entities"] = entities
                rezd["relations"] = relations
                rez.append(rezd)
            d["results"] = rez
            d["error"] = False
        except:
            d["error"] = True
        finally:
            print("Document: {} --- complete".format(d["id"]))

    dt = datetime.datetime.utcnow()

    print("Process complete, Total run time {} seconds".format((dt-dtStart).total_seconds()))

    eo = datetime.datetime(1970, 1, 1)
    epoch = (dt - eo).total_seconds()

    outputFile = os.path.join(directory, outputDir, "output_{}.json".format(epoch))
    print("Writing output file [{}].".format(outputFile))
    with open(outputFile, 'w+') as out:
        json.dump(data, out)

    apiMetricsFile = os.path.join(directory, outputDir, "metrics_{}.json".format(epoch))
    with open(apiMetricsFile, 'w+') as out:
        json.dump(apiTime, out)

if __name__ == "__main__":
    with open("config.yaml","r") as yamlfile:
        cfg = yaml.safe_load(yamlfile)
    mars(cfg, sys.argv)
