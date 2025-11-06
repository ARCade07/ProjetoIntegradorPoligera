const mongoose = require('mongoose');
const userSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true,
        unique: true
    },
    email: {
        type: String,
        required: true,
    },
    password: {
        type: String,
        required: true,
    },
    resetTokenHash: {
        type: String
    },
    resetTokenExpires: {
        type: Date
    }
})
const User = mongoose.model('User', userSchema);

module.exports = User;