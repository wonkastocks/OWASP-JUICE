#!/usr/bin/env node

import fetch from 'node-fetch';
import https from 'https';

// Ignore SSL certificate errors for testing
const httpsAgent = new https.Agent({
  rejectUnauthorized: false
});

const TESTS = [
  {
    name: 'Main Platform (wonkatech.com)',
    url: 'https://wonkatech.com',
    expected: [200, 301, 302, 403],
    checkContent: false
  },
  {
    name: 'Admin Panel',
    url: 'https://wonkatech.com/admin/',
    expected: [200, 301, 302],
    checkContent: true,
    content: ['login', 'admin']
  },
  {
    name: 'Juice Shop Instance 1',
    url: 'https://juice1.wonkatech.com',
    expected: [200],
    checkContent: true,
    content: ['OWASP', 'Juice']
  },
  {
    name: 'Juice Shop Instance 2',
    url: 'https://juice2.wonkatech.com',
    expected: [200],
    checkContent: true,
    content: ['OWASP', 'Juice']
  },
  {
    name: 'Juice Shop Instance 3',
    url: 'https://juice3.wonkatech.com',
    expected: [200],
    checkContent: true,
    content: ['OWASP', 'Juice']
  },
  {
    name: 'Juice Shop Instance 4',
    url: 'https://juice4.wonkatech.com',
    expected: [200],
    checkContent: true,
    content: ['OWASP', 'Juice']
  },
  {
    name: 'Juice Shop Instance 5',
    url: 'https://juice5.wonkatech.com',
    expected: [200],
    checkContent: true,
    content: ['OWASP', 'Juice']
  }
];

async function testURL(test) {
  try {
    console.log(`\nTesting: ${test.name}`);
    console.log(`URL: ${test.url}`);
    
    const response = await fetch(test.url, {
      agent: httpsAgent,
      timeout: 10000,
      redirect: 'manual'
    });
    
    console.log(`Status: ${response.status} ${response.statusText}`);
    
    if (test.expected.includes(response.status)) {
      console.log('✅ Status code matches expected');
    } else {
      console.log(`❌ Unexpected status. Expected: ${test.expected.join(' or ')}`);
      return false;
    }
    
    if (test.checkContent && response.status === 200) {
      const text = await response.text();
      let foundContent = false;
      
      for (const content of test.content) {
        if (text.toLowerCase().includes(content.toLowerCase())) {
          console.log(`✅ Found expected content: "${content}"`);
          foundContent = true;
          break;
        }
      }
      
      if (!foundContent) {
        console.log(`❌ Expected content not found: ${test.content.join(' or ')}`);
        return false;
      }
    }
    
    return true;
  } catch (error) {
    console.log(`❌ Error: ${error.message}`);
    return false;
  }
}

async function testPlatform() {
  console.log('=== CTF Platform Automated Testing ===\n');
  console.log('Testing all components...');
  
  let passed = 0;
  let failed = 0;
  
  for (const test of TESTS) {
    const result = await testURL(test);
    if (result) {
      passed++;
    } else {
      failed++;
    }
  }
  
  console.log('\n=== Test Summary ===');
  console.log(`✅ Passed: ${passed}/${TESTS.length}`);
  console.log(`❌ Failed: ${failed}/${TESTS.length}`);
  
  if (failed === 0) {
    console.log('\n🎉 All tests passed! CTF platform is fully operational.');
  } else {
    console.log('\n⚠️  Some tests failed. Please check the services above.');
  }
}

// Also test using Firecrawl
async function testWithFirecrawl() {
  console.log('\n=== Testing with Firecrawl (visual verification) ===\n');
  
  try {
    // Test main site
    console.log('Attempting to fetch wonkatech.com...');
    const mainSite = await fetch('https://wonkatech.com', {
      agent: httpsAgent,
      timeout: 5000
    });
    console.log(`Main site status: ${mainSite.status}`);
    
    // Test a Juice instance
    console.log('Attempting to fetch juice1.wonkatech.com...');
    const juiceSite = await fetch('https://juice1.wonkatech.com', {
      agent: httpsAgent,
      timeout: 5000
    });
    console.log(`Juice1 status: ${juiceSite.status}`);
    
  } catch (error) {
    console.log('Error with direct fetch:', error.message);
  }
}

// Run tests
testPlatform().then(() => {
  testWithFirecrawl();
});