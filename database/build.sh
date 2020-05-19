# It will take a very very long time.
python3 build_json.py --path $1 --output data/

# Ensure your mongod is hanging up.
python3 put_into_mongodb.py --path data/