const mongoose = require('mongoose');
const User = moongoose.model('User', {
    name: String,
    email: String, 
    password: String
});

module.exports = User;