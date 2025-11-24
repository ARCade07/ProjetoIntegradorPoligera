const mongoose = require('mongoose');
const userSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true,
    },
    email: {
        type: String,
        required: true,
        lowercase: true,
    },
    password: {
        type: String,
        required: true,
    },
    role: {
        type: String,
        enum: ["admin", "user"],
        default: "user"
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