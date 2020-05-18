mkdir database/mongodb
mkdir database/mongodb/db
mongod --port=11382 --dbpath database/mongodb/db/ --logpath=database/mongodb/mongodb.log --logappend --journal