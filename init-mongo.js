db.createUser({
    user: 'bitcoin_service',
    pwd: 'sdve2m3kn23r',
    roles: [{
        role: 'readWrite',
        db: 'bitcoin_service'
    }]
})

db.getSiblingDB('bitcoin_service')

db.createCollection('bitcoin')

db.bitcoin.insert({
    'price': 100.00,
    'updated_at': new Date().toJSON()
})
