/**
 * Shared Components Loader for Mongoose.OS
 * Loads hamburger menu, terminals, and other shared UI components on any page
 */

(function() {
  'use strict';

  // Helper function to safely load component HTML
  function loadComponent(url, containerId) {
    return fetch(url)
      .then(response => {
        if (!response.ok) {
          console.warn(`Failed to load ${url}: ${response.status}`);
          return '';
        }
        return response.text();
      })
      .then(html => {
        if (!html) return;
        
        const container = document.getElementById(containerId);
        if (!container) {
          console.warn(`Container ${containerId} not found`);
          return;
        }
        
        container.innerHTML = html;
        
        // Execute scripts in the loaded HTML
        const scripts = container.getElementsByTagName('script');
        Array.from(scripts).forEach(oldScript => {
          const newScript = document.createElement('script');
          if (oldScript.src) {
            newScript.src = oldScript.src;
          } else {
            newScript.textContent = oldScript.textContent;
          }
          document.body.appendChild(newScript);
        });
      })
      .catch(error => console.warn(`Failed to load ${url}:`, error.message));
  }

  // Initialize shared components when DOM is ready
  function initializeSharedComponents() {
    // Create containers if they don't exist
    const containers = [
      { id: 'hamburgerMenuContainer', order: 1 },
      { id: 'iTerminalContainer', order: 2 },
      { id: 'jTerminalContainer', order: 3 },
      { id: 'versionViewerContainer', order: 4 }
    ];

    containers.forEach(({ id }) => {
      if (!document.getElementById(id)) {
        const div = document.createElement('div');
        div.id = id;
        document.body.appendChild(div);
      }
    });

    // Load all components
    loadComponent('/navigation/hamburger-menu.html', 'hamburgerMenuContainer');
    loadComponent('/terminals/i-terminal.html', 'iTerminalContainer');
    loadComponent('/terminals/j-terminal.html', 'jTerminalContainer');
  }

  // Wait for DOM to be ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeSharedComponents);
  } else {
    initializeSharedComponents();
  }

  // Export initialization function for manual use
  window.MongooseSharedComponents = {
    init: initializeSharedComponents,
    loadComponent: loadComponent
  };
})();
