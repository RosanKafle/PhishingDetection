const mongoose = require('mongoose');
const User = require('../models/user');

const MONGO_URI = process.env.MONGO_URI || 'mongodb://127.0.0.1:27017/phishing';

async function main(){
  try{
    await mongoose.connect(MONGO_URI);
    const users = await User.find().limit(50).lean();
    console.log(JSON.stringify(users, null, 2));
    await mongoose.disconnect();
  }catch(err){
    console.error('listUsers error', err);
    process.exit(1);
  }
}

main();
