document.addEventListener('DOMContentLoaded', function() {
    // Initialize Tom Select for all select fields
    const selects = document.querySelectorAll('.tom-select');
    let tomSelectInstances = {};
    
    selects.forEach(function(select) {
        tomSelectInstances[select.id] = new TomSelect(select, {
            plugins: ['remove_button', 'clear_button'],
            create: false,
            sortField: {
                field: "text",
                direction: "asc"
            },
            searchField: ['text'],
            placeholder: select.getAttribute('placeholder') || 'Search and select...',
            maxOptions: null,
            closeAfterSelect: !select.hasAttribute('multiple')
        });
    });

    // ISBN lookup functionality
    const isbnField = document.getElementById('isbn');
    const titleField = document.getElementById('title');
    const descriptionField = document.getElementById('description');
    const coverUrlField = document.getElementById('cover_url');
    let debounceTimer;

    isbnField.addEventListener('input', function() {
        clearTimeout(debounceTimer);
        const isbn = this.value.replace(/[-\s]/g, ''); // Remove hyphens and spaces
        
        if (isbn.length >= 10) {
            debounceTimer = setTimeout(() => fetchBookData(isbn), 500);
        }
    });

    async function fetchBookData(isbn) {
        try {
            showLoadingState(true);
            
            // Use your Flask route for server-side lookup
            const response = await fetch(`/api/isbn-lookup/${isbn}`);
            const data = await response.json();
            
            if (data.success) {
                autofillForm(data);
            } else {
                showMessage(`No book found for ISBN: ${isbn}`, 'warning');
            }
        } catch (error) {
            console.error('Error fetching book data:', error);
            showMessage('Error looking up ISBN. Please try again.', 'danger');
        } finally {
            showLoadingState(false);
        }
    }

    function autofillForm(bookData) {
        // Fill title if empty
        if (bookData.title && !titleField.value) {
            titleField.value = bookData.title;
        }

        // Fill description if empty
        if (bookData.description && !descriptionField.value) {
            descriptionField.value = bookData.description;
        }

        // Fill cover URL if empty
        if (bookData.cover_url && !coverUrlField.value) {
            coverUrlField.value = bookData.cover_url;
        }

        // Handle authors - try to match existing authors or suggest creation
        if (bookData.authors && bookData.authors.length > 0) {
            handleAuthors(bookData.authors);
        }

        // Handle categories as tags
        if (bookData.categories && bookData.categories.length > 0) {
            handleTags(bookData.categories);
        }

        // Show success message
        showMessage('Book information loaded from ISBN!', 'success');
    }

    function handleAuthors(bookAuthors) {
        const authorsSelect = tomSelectInstances['authors'];
        if (!authorsSelect) return;

        const existingOptions = authorsSelect.options;
        const matchedAuthors = [];

        bookAuthors.forEach(authorName => {
            // Try to find matching author in existing options
            const match = Object.values(existingOptions).find(option => 
                option.text.toLowerCase().includes(authorName.toLowerCase()) ||
                authorName.toLowerCase().includes(option.text.toLowerCase())
            );
            
            if (match) {
                matchedAuthors.push(match.value);
            }
        });

        if (matchedAuthors.length > 0) {
            authorsSelect.setValue(matchedAuthors);
        } else {
            // Show message about unmatched authors
            showMessage(`Authors found: ${bookAuthors.join(', ')}. You may need to add them first.`, 'info');
        }
    }

    function handleTags(categories) {
        const tagsSelect = tomSelectInstances['tags'];
        if (!tagsSelect) return;

        const existingOptions = tagsSelect.options;
        const matchedTags = [];

        categories.forEach(category => {
            // Try to find matching tag in existing options
            const match = Object.values(existingOptions).find(option => 
                option.text.toLowerCase().includes(category.toLowerCase()) ||
                category.toLowerCase().includes(option.text.toLowerCase())
            );
            
            if (match) {
                matchedTags.push(match.value);
            }
        });

        if (matchedTags.length > 0) {
            tagsSelect.setValue(matchedTags);
        }
    }

    function showLoadingState(isLoading) {
        const isbnField = document.getElementById('isbn');
        if (isLoading) {
            isbnField.style.background = 'linear-gradient(90deg, #f8f9fa 25%, transparent 25%, transparent 50%, #f8f9fa 50%, #f8f9fa 75%, transparent 75%, transparent) repeat-x';
            isbnField.style.backgroundSize = '20px 20px';
            isbnField.style.animation = 'loading 1s linear infinite';
        } else {
            isbnField.style.background = '';
            isbnField.style.animation = '';
        }
    }

    function showMessage(message, type = 'info') {
        // Create or update message div
        let messageDiv = document.getElementById('isbn-message');
        if (!messageDiv) {
            messageDiv = document.createElement('div');
            messageDiv.id = 'isbn-message';
            messageDiv.className = 'mt-2 p-2 rounded';
            isbnField.parentNode.appendChild(messageDiv);
        }
        
        messageDiv.className = `mt-2 p-2 rounded alert alert-${type === 'success' ? 'success' : type === 'info' ? 'info' : 'warning'}`;
        messageDiv.textContent = message;
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            if (messageDiv.parentNode) {
                messageDiv.parentNode.removeChild(messageDiv);
            }
        }, 5000);
    }
});

// Add CSS for loading animation
const style = document.createElement('style');
style.textContent = `
    @keyframes loading {
        0% { background-position: 0 0; }
        100% { background-position: 20px 0; }
    }
`;
document.head.appendChild(style);