# It will take a very very long time.
python3 build_tools/main.py --path $1 --output data/

# Ensure your mongod is hanging up.
python3 build_tools/put_into_mongodb.py --path data/