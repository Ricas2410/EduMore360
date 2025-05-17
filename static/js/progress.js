/**
 * EduMore360 Progress Tracking Functionality
 * 
 * This file contains the JavaScript functionality for tracking user progress.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Track content views
    trackContentViews();
    
    // Initialize progress charts
    initProgressCharts();
    
    // Track time spent on content
    trackTimeSpent();
});

/**
 * Track content views
 */
function trackContentViews() {
    // Check if we're on a content page
    const contentElement = document.querySelector('[data-content-type]');
    if (!contentElement) return;
    
    const contentType = contentElement.dataset.contentType;
    const contentId = contentElement.dataset.contentId;
    
    if (!contentType || !contentId) return;
    
    // Record the content view
    recordContentView(contentType, contentId);
    
    // Mark content as viewed in the sidebar
    markContentAsViewed(contentType, contentId);
}

/**
 * Record a content view on the server
 * 
 * @param {string} contentType - The type of content (topic, subtopic, note, etc.)
 * @param {string} contentId - The ID of the content
 */
function recordContentView(contentType, contentId) {
    const formData = new FormData();
    formData.append('content_type', contentType);
    formData.append('content_id', contentId);
    
    fetch('/progress/record-view/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    }).catch(error => {
        console.error('Error recording content view:', error);
    });
}

/**
 * Mark content as viewed in the sidebar
 * 
 * @param {string} contentType - The type of content (topic, subtopic, note, etc.)
 * @param {string} contentId - The ID of the content
 */
function markContentAsViewed(contentType, contentId) {
    const sidebarItem = document.querySelector(`.sidebar-item[data-content-type="${contentType}"][data-content-id="${contentId}"]`);
    if (sidebarItem) {
        sidebarItem.classList.add('viewed');
        
        // Add a checkmark icon
        const checkmark = document.createElement('span');
        checkmark.classList.add('text-success', 'ml-2');
        checkmark.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>';
        
        // Only add if it doesn't already have a checkmark
        if (!sidebarItem.querySelector('.text-success')) {
            sidebarItem.appendChild(checkmark);
        }
    }
    
    // Update progress indicators
    updateProgressIndicators(contentType, contentId);
}

/**
 * Update progress indicators
 * 
 * @param {string} contentType - The type of content (topic, subtopic, note, etc.)
 * @param {string} contentId - The ID of the content
 */
function updateProgressIndicators(contentType, contentId) {
    // Get all progress indicators
    const progressIndicators = document.querySelectorAll('.progress-indicator');
    
    // Update each indicator
    progressIndicators.forEach(indicator => {
        const parentType = indicator.dataset.parentType;
        const parentId = indicator.dataset.parentId;
        
        // Only update indicators for the parent of this content
        if (parentType && parentId) {
            // Get the total and viewed counts
            const totalItems = parseInt(indicator.dataset.totalItems || 0, 10);
            let viewedItems = parseInt(indicator.dataset.viewedItems || 0, 10);
            
            // Increment viewed items if this is a new view
            if (contentType === indicator.dataset.childType && !indicator.dataset.viewedIds?.includes(contentId)) {
                viewedItems++;
                
                // Update the viewed IDs
                let viewedIds = indicator.dataset.viewedIds ? indicator.dataset.viewedIds.split(',') : [];
                viewedIds.push(contentId);
                indicator.dataset.viewedIds = viewedIds.join(',');
                indicator.dataset.viewedItems = viewedItems;
                
                // Update the progress bar
                const progressBar = indicator.querySelector('.progress-bar');
                if (progressBar && totalItems > 0) {
                    const percentage = (viewedItems / totalItems) * 100;
                    progressBar.style.width = `${percentage}%`;
                    
                    // Update the text
                    const progressText = indicator.querySelector('.progress-text');
                    if (progressText) {
                        progressText.textContent = `${viewedItems}/${totalItems}`;
                    }
                    
                    // Update completion status
                    if (viewedItems === totalItems) {
                        indicator.classList.add('completed');
                        
                        // Show completion message
                        const completionMessage = document.createElement('div');
                        completionMessage.classList.add('alert', 'alert-success', 'mt-4');
                        completionMessage.innerHTML = `
                            <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                            <span>Congratulations! You've completed this ${parentType}.</span>
                        `;
                        
                        // Add the message after the indicator
                        indicator.parentNode.insertBefore(completionMessage, indicator.nextSibling);
                    }
                }
            }
        }
    });
}

/**
 * Initialize progress charts
 */
function initProgressCharts() {
    const progressCharts = document.querySelectorAll('.progress-chart');
    if (progressCharts.length === 0) return;
    
    // Check if Chart.js is loaded
    if (typeof Chart === 'undefined') {
        console.error('Chart.js is not loaded. Progress charts will not be displayed.');
        return;
    }
    
    progressCharts.forEach(chartElement => {
        const chartType = chartElement.dataset.chartType || 'doughnut';
        const chartData = JSON.parse(chartElement.dataset.chartData || '{}');
        const chartOptions = JSON.parse(chartElement.dataset.chartOptions || '{}');
        
        // Create the chart
        new Chart(chartElement, {
            type: chartType,
            data: chartData,
            options: chartOptions
        });
    });
}

/**
 * Track time spent on content
 */
function trackTimeSpent() {
    // Check if we're on a content page
    const contentElement = document.querySelector('[data-content-type]');
    if (!contentElement) return;
    
    const contentType = contentElement.dataset.contentType;
    const contentId = contentElement.dataset.contentId;
    
    if (!contentType || !contentId) return;
    
    let startTime = Date.now();
    let timeSpent = 0;
    let isActive = true;
    
    // Update time spent every 5 seconds
    const timeInterval = setInterval(() => {
        if (isActive) {
            timeSpent += 5;
            
            // Record time spent every minute
            if (timeSpent % 60 === 0) {
                recordTimeSpent(contentType, contentId, timeSpent);
            }
        }
    }, 5000);
    
    // Track user activity
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            isActive = false;
            
            // Record time spent when user leaves the page
            recordTimeSpent(contentType, contentId, timeSpent);
        } else {
            isActive = true;
            startTime = Date.now();
        }
    });
    
    // Record time spent when user leaves the page
    window.addEventListener('beforeunload', () => {
        recordTimeSpent(contentType, contentId, timeSpent);
        clearInterval(timeInterval);
    });
}

/**
 * Record time spent on content
 * 
 * @param {string} contentType - The type of content (topic, subtopic, note, etc.)
 * @param {string} contentId - The ID of the content
 * @param {number} seconds - The time spent in seconds
 */
function recordTimeSpent(contentType, contentId, seconds) {
    const formData = new FormData();
    formData.append('content_type', contentType);
    formData.append('content_id', contentId);
    formData.append('seconds', seconds);
    
    fetch('/progress/record-time/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    }).catch(error => {
        console.error('Error recording time spent:', error);
    });
}

/**
 * Get CSRF token from cookies
 * 
 * @param {string} name - The name of the cookie
 * @returns {string} The cookie value
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
