import os
import sys
import http.client
import json

# QDRANT
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))


def deleteVectorDB(DBName):
    conn = http.client.HTTPConnection(QDRANT_HOST, QDRANT_PORT)
    __url = f"/collections/{DBName}"
    conn.request("DELETE", __url)
    response = conn.getresponse()
    data = response.read().decode("utf-8")
    print(data)
    conn.close()
    return data


def checkVectorDB(DBName):
    conn = http.client.HTTPConnection(QDRANT_HOST, QDRANT_PORT)
    __url = f"/collections/{DBName}"
    conn.request("GET", __url)
    response = conn.getresponse()
    data = response.read().decode("utf-8")
    conn.close()
    
    rsJson = json.loads(data)
    result = rsJson.get("result", {})
    vectors_count = result.get("vectors_count", 0)
    return vectors_count


def createVectorDB(DBName, size=384, distance="Cosine"):
    conn = http.client.HTTPConnection(QDRANT_HOST, QDRANT_PORT)
    __url = f"/collections/{DBName}"
    __headers = {"Content-Type": "application/json"}
    __data = {"vectors": {"size": size, "distance": distance, "on_disk": True}}
    
    conn.request("PUT", __url, body=json.dumps(__data), headers=__headers)
    response = conn.getresponse()
    data = response.read().decode("utf-8")
    print(data)
    conn.close()
    return data


def createEmbeddings(DBName, model_name, size, filepath):
    command = f"wasmedge --dir .:. --nn-preload default:GGML:AUTO:{model_name} create_embeddings.wasm default {DBName} {size} {filepath} "
    print(command)
    os.system(command)


def text2qdrant(filepath, db_name="default"):
    deleteVectorDB(db_name)
    createVectorDB(db_name, 768, "Cosine")
    createEmbeddings(db_name, "nomic-embed-text-v1.5.f16.gguf", 768, filepath)

    checkVectorDB(db_name)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python toqdrant.py filepath")
        sys.exit(1)
    text2qdrant(sys.argv[1])
