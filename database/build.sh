# It will take a very very long time.
python3 build/main.py --path $1 --output data/

# Ensure your mongod is hanging up.
python3 build/put_into_mongodb.py --path data/