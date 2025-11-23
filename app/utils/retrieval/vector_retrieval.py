import logging


def retrieve_information(query_vector, milvus_client, collection_name: str):
    if collection_name not in milvus_client.list_collections():
        logging.error(f"Collection '{collection_name}' does not exist in Milvus.")
        return "Error: Collection does not exist."

    search_params = {
        "metric_type": "COSINE",
        "params": {"nprobe": 10}
    }

    results = milvus_client.search(
        collection_name=collection_name,
        data=[query_vector],
        anns_field="vector",
        limit=3,
        search_params=search_params,
        output_fields=["text"]
    )
    logging.debug(f"Milvus search results: {results}")
    retrieved_texts = [
        hit["entity"]["text"]
        for hit in results[0]
        if "entity" in hit and "text" in hit["entity"]
    ]
    return retrieved_texts