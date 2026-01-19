#!/usr/bin/env node

/**
 * Kongtze Project
 * Main entry point
 */

console.log('🚀 Kongtze Project Starting...');

// Load environment variables
import { config } from 'dotenv';
config();

const PORT = process.env.PORT || 3000;
const NODE_ENV = process.env.NODE_ENV || 'development';

console.log(`📊 Environment: ${NODE_ENV}`);
console.log(`🌐 Port: ${PORT}`);

// Your application logic goes here
async function main() {
  try {
    console.log('✨ Application initialized successfully!');

    // Add your startup logic here

  } catch (error) {
    console.error('❌ Failed to initialize application:', error);
    process.exit(1);
  }
}

// Start the application
main();

// Handle graceful shutdown
process.on('SIGINT', () => {
  console.log('\n👋 Shutting down gracefully...');
  process.exit(0);
});

process.on('SIGTERM', () => {
  console.log('\n👋 Shutting down gracefully...');
  process.exit(0);
});
