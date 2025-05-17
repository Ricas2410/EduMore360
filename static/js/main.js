/**
 * EduMore360 Main JavaScript
 * 
 * This file contains the main JavaScript functionality for the EduMore360 platform.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize mobile menu
    initMobileMenu();
    
    // Initialize dropdowns
    initDropdowns();
    
    // Initialize modals
    initModals();
    
    // Initialize tooltips
    initTooltips();
    
    // Initialize tabs
    initTabs();
    
    // Initialize notifications
    initNotifications();
    
    // Initialize search
    initSearch();
    
    // Initialize theme switcher
    initThemeSwitcher();
    
    // Initialize save content functionality
    initSaveContent();
    
    // Initialize content sharing
    initContentSharing();
});

/**
 * Initialize mobile menu
 */
function initMobileMenu() {
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (!mobileMenuButton || !mobileMenu) return;
    
    mobileMenuButton.addEventListener('click', function() {
        mobileMenu.classList.toggle('hidden');
    });
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', function(event) {
        if (!mobileMenu.contains(event.target) && !mobileMenuButton.contains(event.target)) {
            mobileMenu.classList.add('hidden');
        }
    });
}

/**
 * Initialize dropdowns
 */
function initDropdowns() {
    const dropdownButtons = document.querySelectorAll('.dropdown-button');
    
    dropdownButtons.forEach(button => {
        const dropdown = button.nextElementSibling;
        if (!dropdown) return;
        
        button.addEventListener('click', function(event) {
            event.stopPropagation();
            dropdown.classList.toggle('hidden');
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', function(event) {
            if (!dropdown.contains(event.target) && !button.contains(event.target)) {
                dropdown.classList.add('hidden');
            }
        });
    });
}

/**
 * Initialize modals
 */
function initModals() {
    const modalButtons = document.querySelectorAll('[data-modal-target]');
    const closeModalButtons = document.querySelectorAll('[data-close-modal]');
    
    modalButtons.forEach(button => {
        const modalId = button.dataset.modalTarget;
        const modal = document.getElementById(modalId);
        
        if (!modal) return;
        
        button.addEventListener('click', function() {
            modal.classList.add('modal-open');
        });
    });
    
    closeModalButtons.forEach(button => {
        const modal = button.closest('.modal');
        
        if (!modal) return;
        
        button.addEventListener('click', function() {
            modal.classList.remove('modal-open');
        });
    });
    
    // Close modal when clicking on the backdrop
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', function(event) {
            if (event.target === modal) {
                modal.classList.remove('modal-open');
            }
        });
    });
    
    // Close modal with Escape key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            document.querySelectorAll('.modal.modal-open').forEach(modal => {
                modal.classList.remove('modal-open');
            });
        }
    });
}

/**
 * Initialize tooltips
 */
function initTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    
    tooltips.forEach(tooltip => {
        const tooltipText = tooltip.dataset.tooltip;
        
        // Create tooltip element
        const tooltipElement = document.createElement('div');
        tooltipElement.classList.add('tooltip');
        tooltipElement.textContent = tooltipText;
        
        // Add tooltip on hover
        tooltip.addEventListener('mouseenter', function() {
            document.body.appendChild(tooltipElement);
            
            // Position the tooltip
            const rect = tooltip.getBoundingClientRect();
            tooltipElement.style.top = `${rect.top - tooltipElement.offsetHeight - 10}px`;
            tooltipElement.style.left = `${rect.left + (rect.width / 2) - (tooltipElement.offsetWidth / 2)}px`;
            
            // Show the tooltip
            tooltipElement.classList.add('tooltip-visible');
        });
        
        // Remove tooltip on mouse leave
        tooltip.addEventListener('mouseleave', function() {
            tooltipElement.classList.remove('tooltip-visible');
            document.body.removeChild(tooltipElement);
        });
    });
}

/**
 * Initialize tabs
 */
function initTabs() {
    const tabGroups = document.querySelectorAll('.tabs');
    
    tabGroups.forEach(tabGroup => {
        const tabs = tabGroup.querySelectorAll('.tab');
        const tabContents = document.querySelectorAll(`.tab-content[data-tab-group="${tabGroup.dataset.tabGroup}"]`);
        
        tabs.forEach(tab => {
            tab.addEventListener('click', function() {
                // Remove active class from all tabs
                tabs.forEach(t => {
                    t.classList.remove('tab-active');
                });
                
                // Add active class to clicked tab
                this.classList.add('tab-active');
                
                // Show the corresponding tab content
                const tabId = this.dataset.tabId;
                
                tabContents.forEach(content => {
                    if (content.dataset.tabId === tabId) {
                        content.classList.remove('hidden');
                    } else {
                        content.classList.add('hidden');
                    }
                });
            });
        });
    });
}

/**
 * Initialize notifications
 */
function initNotifications() {
    const notificationButton = document.getElementById('notification-button');
    const notificationDropdown = document.getElementById('notification-dropdown');
    
    if (!notificationButton || !notificationDropdown) return;
    
    // Toggle notification dropdown
    notificationButton.addEventListener('click', function(event) {
        event.stopPropagation();
        notificationDropdown.classList.toggle('hidden');
        
        // Mark notifications as read when opening the dropdown
        if (!notificationDropdown.classList.contains('hidden')) {
            markNotificationsAsRead();
        }
    });
    
    // Close notification dropdown when clicking outside
    document.addEventListener('click', function(event) {
        if (!notificationDropdown.contains(event.target) && !notificationButton.contains(event.target)) {
            notificationDropdown.classList.add('hidden');
        }
    });
    
    // Mark notifications as read
    function markNotificationsAsRead() {
        const unreadNotifications = document.querySelectorAll('.notification-item.unread');
        if (unreadNotifications.length === 0) return;
        
        // Get notification IDs
        const notificationIds = Array.from(unreadNotifications).map(notification => notification.dataset.notificationId);
        
        // Send request to mark notifications as read
        fetch('/notifications/mark-as-read/', {
            method: 'POST',
            body: JSON.stringify({ notification_ids: notificationIds }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update UI
                unreadNotifications.forEach(notification => {
                    notification.classList.remove('unread');
                });
                
                // Update notification count
                const notificationCount = document.getElementById('notification-count');
                if (notificationCount) {
                    notificationCount.textContent = '0';
                    notificationCount.classList.add('hidden');
                }
            }
        })
        .catch(error => {
            console.error('Error marking notifications as read:', error);
        });
    }
}

/**
 * Initialize search
 */
function initSearch() {
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    
    if (!searchForm || !searchInput || !searchResults) return;
    
    // Show search results when typing
    searchInput.addEventListener('input', function() {
        const query = this.value.trim();
        
        if (query.length < 3) {
            searchResults.classList.add('hidden');
            return;
        }
        
        // Send search request
        fetch(`/search/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            // Clear previous results
            searchResults.innerHTML = '';
            
            if (data.results.length === 0) {
                searchResults.innerHTML = `
                    <div class="p-4 text-center">
                        <p>No results found for "${query}"</p>
                    </div>
                `;
            } else {
                // Group results by type
                const groupedResults = {};
                
                data.results.forEach(result => {
                    if (!groupedResults[result.type]) {
                        groupedResults[result.type] = [];
                    }
                    
                    groupedResults[result.type].push(result);
                });
                
                // Create result groups
                for (const type in groupedResults) {
                    const results = groupedResults[type];
                    
                    const resultGroup = document.createElement('div');
                    resultGroup.classList.add('p-2');
                    
                    resultGroup.innerHTML = `
                        <h3 class="text-sm font-bold text-gray-500 uppercase mb-2">${type}</h3>
                        <ul class="space-y-2">
                            ${results.map(result => `
                                <li>
                                    <a href="${result.url}" class="block p-2 hover:bg-base-200 rounded-lg">
                                        <div class="font-medium">${result.title}</div>
                                        <div class="text-sm text-gray-600">${result.description}</div>
                                    </a>
                                </li>
                            `).join('')}
                        </ul>
                    `;
                    
                    searchResults.appendChild(resultGroup);
                }
                
                // Add "View all results" link
                const viewAllLink = document.createElement('div');
                viewAllLink.classList.add('p-2', 'text-center', 'border-t', 'border-base-300', 'mt-2', 'pt-2');
                viewAllLink.innerHTML = `
                    <a href="/search/?q=${encodeURIComponent(query)}" class="text-primary hover:underline">
                        View all results
                    </a>
                `;
                
                searchResults.appendChild(viewAllLink);
            }
            
            // Show results
            searchResults.classList.remove('hidden');
        })
        .catch(error => {
            console.error('Error searching:', error);
        });
    });
    
    // Hide search results when clicking outside
    document.addEventListener('click', function(event) {
        if (!searchForm.contains(event.target)) {
            searchResults.classList.add('hidden');
        }
    });
    
    // Prevent form submission
    searchForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        const query = searchInput.value.trim();
        
        if (query.length > 0) {
            window.location.href = `/search/?q=${encodeURIComponent(query)}`;
        }
    });
}

/**
 * Initialize theme switcher
 */
function initThemeSwitcher() {
    const themeSwitcher = document.getElementById('theme-switcher');
    if (!themeSwitcher) return;
    
    themeSwitcher.addEventListener('change', function() {
        const theme = this.checked ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', theme);
        
        // Save theme preference
        localStorage.setItem('theme', theme);
    });
    
    // Set initial theme
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
        themeSwitcher.checked = savedTheme === 'dark';
    }
}

/**
 * Initialize save content functionality
 */
function initSaveContent() {
    const saveButtons = document.querySelectorAll('.save-content-button');
    
    saveButtons.forEach(button => {
        const contentType = button.dataset.contentType;
        const contentId = button.dataset.contentId;
        
        if (!contentType || !contentId) return;
        
        button.addEventListener('click', function() {
            // Toggle saved state
            const isSaved = button.classList.contains('saved');
            
            // Send request to save/unsave content
            fetch('/content/save/', {
                method: 'POST',
                body: JSON.stringify({
                    content_type: contentType,
                    content_id: contentId,
                    action: isSaved ? 'unsave' : 'save'
                }),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update UI
                    if (isSaved) {
                        button.classList.remove('saved');
                        button.innerHTML = `
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                            </svg>
                            <span>Save</span>
                        `;
                    } else {
                        button.classList.add('saved');
                        button.innerHTML = `
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24" stroke="none">
                                <path d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                            </svg>
                            <span>Saved</span>
                        `;
                    }
                }
            })
            .catch(error => {
                console.error('Error saving content:', error);
            });
        });
    });
}

/**
 * Initialize content sharing
 */
function initContentSharing() {
    const shareButtons = document.querySelectorAll('.share-content-button');
    
    shareButtons.forEach(button => {
        button.addEventListener('click', function() {
            const shareUrl = button.dataset.shareUrl || window.location.href;
            const shareTitle = button.dataset.shareTitle || document.title;
            
            // Check if Web Share API is supported
            if (navigator.share) {
                navigator.share({
                    title: shareTitle,
                    url: shareUrl
                })
                .catch(error => {
                    console.error('Error sharing content:', error);
                });
            } else {
                // Fallback to clipboard
                navigator.clipboard.writeText(shareUrl)
                .then(() => {
                    // Show success message
                    const toast = document.createElement('div');
                    toast.classList.add('toast', 'toast-success');
                    toast.innerHTML = `
                        <div class="alert alert-success">
                            <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                            <span>Link copied to clipboard!</span>
                        </div>
                    `;
                    
                    document.body.appendChild(toast);
                    
                    // Remove toast after 3 seconds
                    setTimeout(() => {
                        document.body.removeChild(toast);
                    }, 3000);
                })
                .catch(error => {
                    console.error('Error copying to clipboard:', error);
                });
            }
        });
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
