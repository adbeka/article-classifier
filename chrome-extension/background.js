// Background script for Chrome extension
chrome.runtime.onInstalled.addListener(() => {
    console.log('Article Classifier & Summarizer extension installed');
});

// Listen for messages from popup or content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'processArticle') {
        // Handle article processing requests
        console.log('Processing article:', request.url);
        sendResponse({status: 'processing'});
    }
    return true;
});
