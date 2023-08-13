# Retail Sync Kafka Mode

Following distributed data path fixing method using Kafka

Plan:

    Send data to kafka topic with predefined number suffix 
    Assign process iid such that it will take data from that topic only

Notice:
    
    If need arises increase number of workers and topic by same amount. 