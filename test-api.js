#!/usr/bin/env node
/**
 * Test LinkedIn Voyager API
 */

import { readFileSync } from 'fs';

const cookies = JSON.parse(readFileSync('/tmp/li_cookies.json', 'utf-8'));
const cookieString = Object.entries(cookies).map(([k, v]) => `${k}=${v}`).join('; ');
const csrfToken = (cookies.JSESSIONID || '').replace(/^"|"$/g, '');

const VOYAGER_BASE = 'https://www.linkedin.com/voyager/api';
const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36';

async function testSearch() {
  // Try the search endpoint with different formats
  const keywords = 'energy storage';
  
  // Format 1: Standard search clusters
  const url1 = `${VOYAGER_BASE}/search/dash/clusters?` + new URLSearchParams({
    decorationId: 'com.linkedin.voyager.dash.deco.search.SearchClusterCollection-175',
    count: '10',
    q: 'all',
    query: `(keywords:${encodeURIComponent(keywords)},resultType:PEOPLE)`,
    start: '0',
  });
  
  console.log('Testing URL 1 (search/dash/clusters):');
  console.log(url1);
  
  try {
    const resp = await fetch(url1, {
      headers: {
        'user-agent': USER_AGENT,
        'accept': 'application/vnd.linkedin.normalized+json+2.1',
        'accept-language': 'en-US,en;q=0.9',
        'x-li-lang': 'en_US',
        'x-restli-protocol-version': '2.0.0',
        'csrf-token': csrfToken,
        'cookie': cookieString,
      },
    });
    console.log(`Status: ${resp.status}`);
    const text = await resp.text();
    console.log('Response:', text.slice(0, 500));
  } catch (err) {
    console.error('Error:', err.message);
  }
  
  // Format 2: graphQL search
  console.log('\n\nTesting URL 2 (graphql search):');
  const graphqlUrl = 'https://www.linkedin.com/voyager/api/graphql?variables=(start:0,origin:GLOBAL_SEARCH_HEADER,query:(keywords:energy%20storage,flagshipSearchIntent:SEARCH_SRP,queryParameters:List((key:resultType,value:List(PEOPLE))),includeFiltersInResponse:false))&queryId=voyagerSearchDashClusters.42d1f tried';
  
  try {
    const resp = await fetch(graphqlUrl, {
      headers: {
        'user-agent': USER_AGENT,
        'accept': 'application/vnd.linkedin.normalized+json+2.1',
        'accept-language': 'en-US,en;q=0.9',
        'x-li-lang': 'en_US',
        'x-restli-protocol-version': '2.0.0',
        'csrf-token': csrfToken,
        'cookie': cookieString,
      },
    });
    console.log(`Status: ${resp.status}`);
    const text = await resp.text();
    console.log('Response:', text.slice(0, 500));
  } catch (err) {
    console.error('Error:', err.message);
  }
  
  // Format 3: Try typeahead
  console.log('\n\nTesting URL 3 (typeahead):');
  const typeaheadUrl = `${VOYAGER_BASE}/typeahead/hits?` + new URLSearchParams({
    q: 'federated',
    query: keywords,
    type: 'PROFILE',
    count: '10',
  });
  
  try {
    const resp = await fetch(typeaheadUrl, {
      headers: {
        'user-agent': USER_AGENT,
        'accept': 'application/vnd.linkedin.normalized+json+2.1',
        'x-restli-protocol-version': '2.0.0',
        'csrf-token': csrfToken,
        'cookie': cookieString,
      },
    });
    console.log(`Status: ${resp.status}`);
    const text = await resp.text();
    console.log('Response:', text.slice(0, 1000));
  } catch (err) {
    console.error('Error:', err.message);
  }
}

testSearch().catch(console.error);
