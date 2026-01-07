// Popup script for Chrome extension
document.addEventListener('DOMContentLoaded', function() {
    const analyzeBtn = document.getElementById('analyzeBtn');
    const apiUrlInput = document.getElementById('apiUrl');
    const statusDiv = document.getElementById('status');
    const resultDiv = document.getElementById('result');
    
    // Load saved API URL
    chrome.storage.sync.get(['apiUrl'], function(result) {
        if (result.apiUrl) {
            apiUrlInput.value = result.apiUrl;
        }
    });
    
    // Save API URL when changed
    apiUrlInput.addEventListener('change', function() {
        chrome.storage.sync.set({apiUrl: apiUrlInput.value});
    });
    
    analyzeBtn.addEventListener('click', async function() {
        // Get current tab URL
        const [tab] = await chrome.tabs.query({active: true, currentWindow: true});
        const currentUrl = tab.url;
        
        if (!currentUrl.startsWith('http')) {
            showStatus('Please navigate to a web page first', 'error');
            return;
        }
        
        const apiUrl = apiUrlInput.value || 'http://localhost:5000';
        
        // Disable button and show loading
        analyzeBtn.disabled = true;
        showStatus('Analyzing article...', 'loading');
        hideResult();
        
        try {
            // Call the API
            const response = await fetch(`${apiUrl}/api/process`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({url: currentUrl})
            });
            
            const data = await response.json();
            
            if (response.ok) {
                showStatus('Analysis complete!', 'success');
                showResult(data);
                setTimeout(() => hideStatus(), 2000);
            } else {
                showStatus(data.error || 'Error processing article', 'error');
            }
            
        } catch (error) {
            console.error('Error:', error);
            showStatus('Failed to connect to API server. Make sure it\'s running.', 'error');
        } finally {
            analyzeBtn.disabled = false;
        }
    });
    
    function showStatus(message, type) {
        statusDiv.textContent = message;
        statusDiv.className = `status ${type}`;
    }
    
    function hideStatus() {
        statusDiv.className = 'status';
    }
    
    function showResult(data) {
        const title = data.title || 'No title';
        const category = data.classification?.top_label || 'Unknown';
        const confidence = data.classification?.top_score || 0;
        const summary = data.summary || 'No summary available';
        
        document.getElementById('resultTitle').textContent = title;
        document.getElementById('resultCategory').textContent = category.toUpperCase();
        document.getElementById('resultConfidence').textContent = `(${(confidence * 100).toFixed(1)}%)`;
        document.getElementById('resultSummary').textContent = summary;
        
        resultDiv.classList.add('show');
    }
    
    function hideResult() {
        resultDiv.classList.remove('show');
    }
});
