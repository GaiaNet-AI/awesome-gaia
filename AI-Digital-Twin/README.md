# ai
In this repository, the configuration file `config.json` is already prepared. Follow the steps below to achieve a digital twin of the renowned Chinese philosopher Confucius:

1. Run the Gaianet node.
2. Convert the specified dataset `confucius.txt` into a snapshot and configure it within the Gaianet node.

After completing these steps, you will be able to utilize the data within the Gaianet node to simulate a digital representation embodying the thoughts and knowledge of Confucius.



## Run Gaianet Node

1. Initialize the node

```
gaianet init
```

2. Start the gaianet node. So you can chat with it.

```
gaianet start
```

## Creating Embeddings Using the Tool

Once your Gaia node is running smoothly, you can update the snapshot without stopping the node.

```
cd gaianet
```

Next, we wil use the following command line to create embeddings, generate and replace the snapshot.

```
python3 toqdrant.py confucius.txt
```

Once the process is complete, test your node by asking it a question to verify that the snapshot has been successfully updated. It's better that you can update the system prompt based on your new snapshots.

```
http://localhost:8080/chatbot-ui/index.html
```

