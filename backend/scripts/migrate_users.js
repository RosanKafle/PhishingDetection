#!/usr/bin/env node
/**
 * Migration script to import dev_users.json into MongoDB
 */
const mongoose = require('mongoose');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

// User schema (matching the existing user model)
const userSchema = new mongoose.Schema({
  username: { type: String, required: true, unique: true },
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true },
  createdAt: { type: Date, default: Date.now }
});

const User = mongoose.model('User', userSchema);

async function migrateUsers() {
  try {
    // Connect to MongoDB
    const MONGO_URI = process.env.MONGO_URI || 'mongodb://127.0.0.1:27017/phishing';
    await mongoose.connect(MONGO_URI, { 
      useNewUrlParser: true, 
      useUnifiedTopology: true 
    });
    console.log('Connected to MongoDB');

    // Read dev_users.json
    const devUsersPath = path.join(__dirname, '..', 'data', 'dev_users.json');
    if (!fs.existsSync(devUsersPath)) {
      console.log('dev_users.json not found, skipping migration');
      return;
    }

    const devUsers = JSON.parse(fs.readFileSync(devUsersPath, 'utf8'));
    console.log(`Found ${devUsers.length} users to migrate`);

    // Migrate each user
    let migrated = 0;
    let skipped = 0;

    for (const devUser of devUsers) {
      try {
        // Check if user already exists
        const existing = await User.findOne({ 
          $or: [
            { username: devUser.username },
            { email: devUser.email }
          ]
        });

        if (existing) {
          console.log(`User ${devUser.username} already exists, skipping`);
          skipped++;
          continue;
        }

        // Create new user
        const newUser = new User({
          username: devUser.username,
          email: devUser.email,
          password: devUser.password, // Already hashed
          createdAt: devUser.createdAt ? new Date(devUser.createdAt) : new Date()
        });

        await newUser.save();
        console.log(`Migrated user: ${devUser.username}`);
        migrated++;

      } catch (error) {
        console.error(`Error migrating user ${devUser.username}:`, error.message);
      }
    }

    console.log(`Migration completed: ${migrated} migrated, ${skipped} skipped`);

  } catch (error) {
    console.error('Migration failed:', error);
  } finally {
    await mongoose.disconnect();
  }
}

// Run migration
if (require.main === module) {
  migrateUsers();
}

module.exports = { migrateUsers };