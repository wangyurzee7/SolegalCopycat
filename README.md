# SolegalCopycat

Coursework of Search Engine Technology and Practice.

Author : Dingyuan Cao, Yuzhong Wang

Fronted : https://github.com/Mockingjay1316/SolegalCopycat-frontend

## Requirements

We use Mongodb as database, so you should install `mongodb` first.

Python3 is used in this project. You can see requirements for python in `requirements.txt`, and use `pip3` to install them.

## How to Run?

Two terminals are required, one for hanging up Mongodb, and another for other works.

### Terminal 1

Run
```
./run_mongodb.sh
```
, and hang it up.

### Terminal 2

First, you need to build the database. Assume that your source data is at `${path}`, and all of them are unziped. Then you can:

```
cd database
./build.sh
```

It will take a very very long time, so please be patient.

Next, you can execute the following command to run your website:

```
@cdy
```

## Report

See `report.pdf`.

## Acknowledgement

N/A
