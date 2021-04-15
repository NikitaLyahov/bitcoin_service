db.createUser({
    user: process.env.MONGO_INITDB_ROOT_USERNAME,
    pwd: process.env.MONGO_INITDB_ROOT_PASSWORD,
    roles: [{
        role: 'readWrite',
        db: process.env.MONGO_INITDB_DATABASE
    }]
})

db.getSiblingDB('mongo_database')

db.createCollection('bitcoin')

db.bitcoin.insert({
    'price': 100,
    'updated_at': new Date().toJSON()
})
