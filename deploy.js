#!/usr/bin/env node
/**
 * LOG JAM — 1-CLICK DEPLOYMENT PIPELINE
 * Mirrors the Wings of Fire deployment workflow:
 * 1. Prepares dist/ (index.html, 200.html, CNAME)
 * 2. Syncs local desktop copy (C:\Users\DELL\logjam.html)
 * 3. Pushes to Xperia Phone via ADB WiFi (192.168.1.200:5555)
 * 4. Deploys to Surge CDN (https://logjam.surge.sh)
 * 5. Commits and pushes changes to GitHub
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const ROOT_DIR = __dirname;
const SRC_INDEX = path.join(ROOT_DIR, 'index.html');
const DIST_DIR = path.join(ROOT_DIR, 'dist');
const TARGET_LOCAL = 'C:\\Users\\DELL\\logjam.html';
const PHONE_IP = '192.168.1.200:5555';

console.log('\n🪵 ===================================================');
console.log('   LOG JAM — AUTOMATED DEPLOYMENT PIPELINE');
console.log('===================================================');

// 1. Prepare dist/
if (!fs.existsSync(DIST_DIR)) fs.mkdirSync(DIST_DIR, { recursive: true });
fs.copyFileSync(SRC_INDEX, path.join(DIST_DIR, 'index.html'));
fs.copyFileSync(SRC_INDEX, path.join(DIST_DIR, '200.html'));
fs.writeFileSync(path.join(DIST_DIR, 'CNAME'), 'logjam.surge.sh\n');
console.log('   ✓ Prepared dist/ bundle (index.html, 200.html, CNAME)');

// 2. Sync local copy
try {
    fs.copyFileSync(SRC_INDEX, TARGET_LOCAL);
    console.log(`   ✓ Local copy updated: ${TARGET_LOCAL}`);
} catch (e) {
    console.warn(`   ⚠ Local copy warning: ${e.message}`);
}

// 3. Push to Xperia phone over ADB
try {
    const devices = execSync('adb devices', { encoding: 'utf8' });
    if (devices.includes(PHONE_IP)) {
        console.log(`\n📱 Pushing to Xperia Phone over ADB WiFi (${PHONE_IP})...`);
        execSync(`adb -s ${PHONE_IP} push "${SRC_INDEX}" /data/local/tmp/logjam.html`, { stdio: 'inherit' });
        execSync(`adb -s ${PHONE_IP} push "${path.join(ROOT_DIR, 'logjam_db.py')}" /data/local/tmp/logjam_db.py`, { stdio: 'inherit' });
        execSync(`adb -s ${PHONE_IP} shell "run-as com.termux cp /data/local/tmp/logjam.html /data/data/com.termux/files/home/logjam.html && run-as com.termux cp /data/local/tmp/logjam_db.py /data/data/com.termux/files/home/logjam_db.py"`, { stdio: 'inherit' });
        console.log('   ✓ Phone logjam.html and logjam_db.py updated!');
    } else {
        console.log(`\n📱 Phone (${PHONE_IP}) not in adb devices, skipping phone push.`);
    }
} catch (e) {
    console.warn(`   ⚠ ADB phone push warning: ${e.message}`);
}

// 4. Deploy to Surge CDN
try {
    console.log('\n☁️  Deploying to Surge CDN (https://logjam.surge.sh)...');
    execSync(`npx --registry=https://registry.npmjs.org/ -y surge "${DIST_DIR}" logjam.surge.sh`, { stdio: 'inherit' });
    console.log('   ✓ Surge CDN deployed live at https://logjam.surge.sh !');
} catch (e) {
    console.warn(`   ⚠ Surge deploy warning: ${e.message}`);
}

// 5. Git Commit & Push
try {
    console.log('\n🐙 Syncing with GitHub...');
    execSync('git add .', { stdio: 'inherit' });
    try {
        execSync('git commit -m "deploy: update live game build"', { stdio: 'inherit' });
    } catch (_) {}
    execSync('git push origin main', { stdio: 'inherit' });
    console.log('   ✓ Pushed to GitHub repository!');
} catch (e) {
    console.warn(`   ⚠ Git push warning: ${e.message}`);
}

console.log('\n🎉 ALL DEPLOYMENTS COMPLETE!\n');

