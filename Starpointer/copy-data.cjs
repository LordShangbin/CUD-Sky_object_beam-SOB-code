const fs = require('fs');
const path = require('path');

const source = path.join(__dirname, '..', 'hip_main.dat');
const dest = path.join(__dirname, 'public', 'hip_main.dat');

try {
  fs.copyFileSync(source, dest);
  console.log('✓ Copied hip_main.dat to public folder');
} catch (error) {
  console.error('✗ Failed to copy hip_main.dat:', error.message);
  process.exit(1);
}
