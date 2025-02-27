// Dashboard drawer and navigation functionality
document.addEventListener('DOMContentLoaded', function() {
    // Toggle button rotation
    const drawer = document.getElementById('dashboard-drawer');
    const toggleBtn = document.getElementById('drawer-toggle-btn');
    
    if (drawer && toggleBtn) {
        drawer.addEventListener('change', function() {
            if (this.checked) {
                toggleBtn.querySelector('svg').style.transform = 'rotate(180deg)';
            } else {
                toggleBtn.querySelector('svg').style.transform = 'rotate(0)';
            }
        });
        
        // Handle sidebar link clicks
        const sidebarLinks = document.querySelectorAll('.sidebar-link');
        const contentSections = document.querySelectorAll('.content-section');
        
        sidebarLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                // Hide all content sections
                contentSections.forEach(section => {
                    section.classList.add('hidden');
                });
                
                // Show the target content section
                const targetId = this.getAttribute('data-target');
                document.getElementById(targetId).classList.remove('hidden');
                
                // On mobile, close the drawer after selection
                if (window.innerWidth < 1024) {
                    drawer.checked = false;
                    toggleBtn.querySelector('svg').style.transform = 'rotate(0)';
                }
            });
        });
    }
}); 